# Generated by Django 3.1.7 on 2021-12-03 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0007_teammember'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='member_role',
            field=models.CharField(default='', max_length=60),
        ),
    ]