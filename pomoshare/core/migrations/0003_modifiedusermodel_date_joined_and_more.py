# Generated by Django 4.0 on 2022-04-19 08:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_modifiedusermodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='modifiedusermodel',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='modifiedusermodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='modifiedusermodel',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='modifiedusermodel',
            name='email',
            field=models.CharField(max_length=100, unique=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='modifiedusermodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='modifiedusermodel',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='modifiedusermodel',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='modifiedusermodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
