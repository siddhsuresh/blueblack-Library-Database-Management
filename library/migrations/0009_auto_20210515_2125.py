# Generated by Django 3.2 on 2021-05-15 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_auto_20210515_1623'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookindividual',
            options={'ordering': ['edition']},
        ),
        migrations.RemoveField(
            model_name='book',
            name='available_books',
        ),
        migrations.RemoveField(
            model_name='book',
            name='total_book',
        ),
    ]
