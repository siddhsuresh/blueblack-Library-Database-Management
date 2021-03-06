"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from library.views import *
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('history/', ReturnListView, name='history'),
    path('history/csv', History_view, name='csv'),
    path('allbooks/', all_books_view, name='allbooks'),
    path('search/', Search_View, name='search'),
    path('profile/', Profile_view, name='profile'),
    path('<int:pk>/author', Author_view,  name='author'),
    path('viewissued/', get_issued_view, name='all_issued'),
    path('<int:pk>/renew/', View_Renew_Issued, name='book_renew'),
    path('<int:pk>/return/', Book_Return_View, name='book_return'),
    path('<int:pk>/book/', Individual_books_view, name='book'),
    path('<uuid:pk>/issue/', Book_Issue_View, name='book_issue'),
    path('', View_Dashboard, name='dashboard'),
    path('staff/',View_Staff_Dashboard, name='staff_dashboard'),
    path('staff/allstudents', View_Staff_AllStudents, name='staff_allstudents'),
    path('staff/<int:pk>/student', View_Student,  name='staff_student'),
    path('staff/<int:pk>/book', View_Staff_Book,  name='staff_book'),
    path('staff/allbooks', View_Staff_AllBooks, name='staff_allbooks'),
    path('staff/allauthors', View_Staff_AllAuthors, name='staff_allauthors'),
    path('staff/<int:pk>/author',View_Staff_Author, name='staff_author'),
    path('staff/renewrequests',View_Staff_Renew,name='allrenew'),
    path('staff/<int:pk>/approve',View_Staff_Approve_Renew,name='approverenew'),
    path('staff/<int:pk>/deny',View_Staff_Deny_Renew,name='denyrenew'),
    url(r'^login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('__debug__/',include(debug_toolbar.urls)),
]
