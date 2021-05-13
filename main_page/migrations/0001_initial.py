# Generated by Django 3.1.7 on 2021-05-10 13:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main_page.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyContacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=25, verbose_name='Contact Form')),
                ('contact_data', models.CharField(max_length=20, verbose_name='Contact Info')),
            ],
        ),
        migrations.CreateModel(
            name='MediaAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_name', models.CharField(max_length=25, verbose_name='Social Media Name')),
                ('media_url', models.URLField(max_length=300, verbose_name='The URL of Account')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('number_of_questions', models.IntegerField(help_text="Number of Quiz's questions")),
                ('time', models.IntegerField(blank=True, help_text='Duration of quiz in minutes', null=True)),
                ('status', models.BooleanField(verbose_name='Akitv|Deaktiv')),
            ],
            options={
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.CreateModel(
            name='QuizName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_name', models.TextField(max_length=8000, verbose_name='Quiz name')),
                ('archive_quiz', models.BooleanField(blank=True, null=True, verbose_name='Quiz archived')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='usrr', serialize=False, to='auth.user')),
                ('image', models.ImageField(blank=True, default='/user.png', upload_to='profile_pics/')),
                ('phone_prefix', models.CharField(choices=[('Aze1', '050'), ('Aze2', '051'), ('Bak1', '055'), ('Bak2', '099'), ('Nar1', '070'), ('Nar2', '077')], default='Nar1', max_length=5)),
                ('phone_number', models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(message='Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567', regex='^\\d{7}$')])),
                ('birthdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='usr', serialize=False, to='auth.user')),
                ('image', models.ImageField(blank=True, default='/user.png', upload_to='profile_pics/')),
                ('phone_prefix', models.CharField(choices=[('Aze1', '050'), ('Aze2', '051'), ('Bak1', '055'), ('Bak2', '099'), ('Nar1', '070'), ('Nar2', '077')], default='Nar1', max_length=5)),
                ('phone_number', models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(message='Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567', regex='^\\d{7}$')])),
                ('birthdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('u_shx_pin', models.CharField(max_length=7, primary_key=True, serialize=False, verbose_name="User's ID card pin")),
                ('u_name', models.CharField(max_length=20, validators=[main_page.models.check_name], verbose_name="User's name")),
                ('u_sname', models.CharField(max_length=20, verbose_name="User's surname")),
                ('u_phonenumberprefix', models.CharField(choices=[('Aze1', '050'), ('Aze2', '051'), ('Bak1', '055'), ('Bak2', '099'), ('Nar1', '070'), ('Nar2', '077')], default='Nar1', max_length=5, verbose_name='User Phone prefix')),
                ('u_phonenumber', models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(message='Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567', regex='^\\d{7}$')])),
                ('u_birthdate', models.DateField(verbose_name="User's birthdate")),
                ('u_course', models.CharField(choices=[('Yox1', 'Kurs yoxdur'), ('Eng', 'English')], default='Rus', max_length=20, verbose_name="User's course")),
                ('u_regis_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name="User's registration date")),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.quiz')),
                ('std_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizVariants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_image', models.ImageField(blank=True, null=True, upload_to='questions/', verbose_name='If question is image question, ADD it: ')),
                ('question_description', models.TextField(max_length=500, verbose_name='Question: ')),
                ('variantA', models.TextField(max_length=250, verbose_name='Varaint A:')),
                ('variantB', models.TextField(max_length=250, verbose_name='Varinat B:')),
                ('variantC', models.TextField(max_length=250, verbose_name='Varinat C:')),
                ('variantD', models.TextField(max_length=250, verbose_name='Variant D')),
                ('teacher_answer', models.TextField(max_length=250, verbose_name='Right Answer:')),
                ('student_answer', models.TextField(blank=True, null=True, verbose_name='Student Answer:')),
                ('quiz_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='main_page.quizname')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='questions/')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.CharField(max_length=4, verbose_name='Course_ID')),
                ('c_name', models.CharField(max_length=20, verbose_name='Course_name')),
                ('c_status', models.BooleanField(default=True)),
                ('c_description', models.TextField(blank=True)),
                ('c_photo', models.ImageField(default='', upload_to='Courses/')),
                ('students', models.ManyToManyField(blank=True, related_name='coursess', to='main_page.StudentProfile')),
                ('teachers', models.ManyToManyField(blank=True, related_name='courses', to='main_page.TeacherProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=50, verbose_name='Branch name')),
                ('branch_short_desc', models.CharField(max_length=300, verbose_name='Short desciption - 300 characters')),
                ('branch_details', models.TextField(max_length=2000, verbose_name='Large information - 2000 characters')),
                ('branch_location', models.URLField(max_length=300, verbose_name='Google Map location')),
                ('branch_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.companycontacts')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.question')),
            ],
        ),
    ]
