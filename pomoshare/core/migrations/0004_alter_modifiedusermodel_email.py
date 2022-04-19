# Generated by Django 4.0 on 2022-04-19 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_modifiedusermodel_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modifiedusermodel',
            name='email',
            field=models.EmailField(max_length=100, unique=True, verbose_name='Email address'),
        ),
    ]