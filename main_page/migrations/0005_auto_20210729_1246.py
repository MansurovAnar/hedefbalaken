# Generated by Django 3.1.7 on 2021-07-29 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0004_auto_20210729_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='courses', to='main_page.TeacherProfile'),
        ),
    ]
