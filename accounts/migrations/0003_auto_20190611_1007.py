# Generated by Django 2.2.2 on 2019-06-11 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190610_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.FileField(upload_to='', verbose_name='icon'),
        ),
    ]
