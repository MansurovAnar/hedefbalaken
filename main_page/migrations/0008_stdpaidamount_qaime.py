# Generated by Django 3.1.7 on 2022-09-06 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0007_auto_20220817_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='stdpaidamount',
            name='qaime',
            field=models.FileField(default='/qaime.pdf', upload_to='pdf/'),
        ),
    ]
