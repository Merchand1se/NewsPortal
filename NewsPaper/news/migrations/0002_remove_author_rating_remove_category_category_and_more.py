# Generated by Django 4.2.10 on 2024-02-26 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='Rating',
        ),
        migrations.RemoveField(
            model_name='category',
            name='Category',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='Rating',
        ),
        migrations.RemoveField(
            model_name='post',
            name='Rating',
        ),
        migrations.AddField(
            model_name='author',
            name='autUser',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='author',
            name='ratingAut',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=None, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
