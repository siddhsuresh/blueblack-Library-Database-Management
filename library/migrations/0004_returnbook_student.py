# Generated by Django 3.2 on 2021-05-13 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20210512_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnbook',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='library.student'),
            preserve_default=False,
        ),
    ]
