# Generated by Django 2.2 on 2019-04-07 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='タイトル')),
                ('text', models.TextField(verbose_name='詳細')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='投稿日時')),
                ('tags', models.ManyToManyField(to='topics.Tag', verbose_name='タグ')),
                ('user', models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='ゴロ')),
                ('desc', models.TextField(verbose_name='説明')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='回答日時')),
                ('votes', models.IntegerField(default=0)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.Topic')),
                ('user', models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='回答者')),
            ],
        ),
    ]
