# Generated by Django 3.1.7 on 2021-07-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0002_auto_20210601_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='group',
            field=models.ManyToManyField(related_name='quiz_group', to='main_page.Course'),
        ),
    ]