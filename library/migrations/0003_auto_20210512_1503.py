# Generated by Django 3.2.2 on 2021-05-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_issuebook_borrowed_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.CharField(default=' ', max_length=1000),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='student',
            name='roll_no',
            field=models.CharField(max_length=10),
        ),
    ]
