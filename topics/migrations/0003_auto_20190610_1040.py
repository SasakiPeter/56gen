# Generated by Django 2.2.2 on 2019-06-10 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0002_auto_20190610_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='contribute_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='voter',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='投票者'),
        ),
    ]
