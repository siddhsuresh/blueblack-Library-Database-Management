import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Genre(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey('PublishingHouse', on_delete=models.SET_NULL, null=True, blank=True)
    GEN = (('n',''),('m','Male'),('f','Female'),('o','Other'))
    gender = models.CharField(max_length=15, choices=GEN, default='n', blank=True)
    bio = models.CharField(max_length=1000, default=' ')
    nationality= models.CharField(max_length=50, default=' ')

    def __str__(self):
        return self.name

class PublishingHouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all())

    def num_books(self):
        return BookIndividual.objects.filter(book=self, status='a').count()

    def issued_books(self):
        return BookIndividual.objects.filter(book=self, status='o').count()

    def __str__(self):
        return self.title

class BookIndividual(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    edition = models.IntegerField(default=0)
    LOAN_STATUS = ( ('o', 'Not Available'), ('a', 'Available'))
    status = models.CharField( max_length=1, choices=LOAN_STATUS, blank=True, default='a', help_text='')

    class Meta:
        ordering = ['-edition']

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

    def availability(self):
        if self.status=='a':
            return True
        return False

class IssueBook(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    borrowed_book = models.ForeignKey('BookIndividual', on_delete = models.SET_NULL , null=True, blank=True)
    issue_date = models.DateTimeField(null=True,blank=True)
    expected_return_date = models.DateTimeField(null=True,blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name+" has been issued "+self.borrowed_book.book.title+" on "+str(self.issue_date)

    def overdue(self):
        time=self.expected_return_date-timezone.now()
        if time.total_seconds()<0:
            return True
        return False
    def can_renew(self):
        if RenewRequest.objects.filter(book__student__id=self.student.id, request='p').count()==0:
            return True
        return False

    def request_for_renew(self):
        r=RenewRequest.objects.get(book=self)
        if r.request=='p':
            return True
        return False

    def request_denied(self):
        r=RenewRequest.objects.get(book=self)
        if r.request=='d':
            return True
        return False

    def request_success(self):
        r=RenewRequest.objects.get(book=self)
        if r.request=='a':
            return True
        return False

class ReturnBook(models.Model):
    borrowed_book = models.OneToOneField('IssueBook', on_delete = models.CASCADE , null=True, blank=True)
    actual_return_date = models.DateTimeField(null=True,blank=True)
    is_fined = models.BooleanField(default=False)

    def __str__(self):
        return self.borrowed_book.student.name+" has returned "+self.borrowed_book.borrowed_book.book.title+" on "+str(self.actual_return_date)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    branch = models.CharField(max_length=3)
    DEPT = ( ('1', 'CSE'), ('2', 'ECE'), ('3','EEE'),('4','ME'))
    department = models.CharField(max_length=1, choices=DEPT, blank=True, default='1')
    BAT = (('1','2017'),('2','2018'),('3','2019'),('4','2020'))
    batch = models.CharField(max_length=1, choices=BAT, blank=True, default='4')
    SEM = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'))
    semester = models.CharField(max_length=1, choices=SEM, blank=True, default='1')
    fine = models.IntegerField(default=0)
    email=models.EmailField()

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return str(self.roll_no)

    def num_books(self):
        return IssueBook.objects.filter(student=self, is_returned=False).count()

    def num_return(self):
        return ReturnBook.objects.filter(borrowed_book__student=self).count()

    def frratio(self):
        fine = ReturnBook.objects.filter(borrowed_book__student=self,is_fined=True).count()
        ret = ReturnBook.objects.filter(borrowed_book__student=self).count()
        if ret==0:
            return "No Books Returned Yet"
        ratio = round(fine/ret*100)
        return ratio

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.roll_no)

class RenewRequest(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.OneToOneField('IssueBook',  on_delete = models.CASCADE , null=True, blank=True)
    REQUEST_STATUS = (('p', 'Pending'), ('a', 'Approved'),('d','Denied'))
    request = models.CharField(max_length=1, choices=REQUEST_STATUS, blank=True, default='p')
    date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.book.student.name +" has requested 1 day extension for the book "+self.book.borrowed_book.book.title

    def is_approv(self):
        if self.request=='a':
            return True
        return False

    def is_den(self):
        if self.request=='d':
            return True
        return False