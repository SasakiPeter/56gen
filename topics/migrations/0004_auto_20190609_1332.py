# Generated by Django 2.2.2 on 2019-06-09 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20190608_2251'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AlterField(
            model_name='topic',
            name='tags',
            field=models.ManyToManyField(to='tags.Tag', verbose_name='タグ'),
        ),
    ]
