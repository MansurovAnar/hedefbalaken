# Generated by Django 3.1.7 on 2022-05-09 10:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import main_page.models.all_models


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
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_id', models.CharField(default='NON', max_length=4, verbose_name='Course_ID')),
                ('c_name', models.CharField(default='', max_length=20, verbose_name='Course_name')),
                ('c_status', models.BooleanField(default=True)),
                ('c_description', models.TextField(blank=True)),
                ('c_photo', models.ImageField(default='', upload_to='Courses/')),
            ],
        ),
        migrations.CreateModel(
            name='FrontMenuNames',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses_exams', models.CharField(max_length=30)),
                ('about_us', models.CharField(max_length=30)),
                ('contacts', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='FrontPageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement', models.ImageField(blank=True, upload_to='exam_pics/')),
                ('slogan', models.CharField(max_length=50)),
                ('description_header', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('subscription_header', models.CharField(max_length=50)),
                ('subscription_text', models.CharField(max_length=100)),
                ('subscription_form_header', models.TextField(max_length=100)),
                ('our_specialities_header', models.CharField(max_length=50)),
                ('our_specialities_desc', models.TextField()),
                ('our_specialities_1', models.CharField(max_length=50)),
                ('our_specialities_1_desc', models.TextField()),
                ('our_specialities_2', models.CharField(max_length=50)),
                ('our_specialities_2_desc', models.TextField()),
                ('our_specialities_3', models.CharField(max_length=50)),
                ('our_specialities_3_desc', models.TextField()),
                ('our_specialities_4', models.CharField(max_length=50)),
                ('our_specialities_4_desc', models.TextField()),
                ('exam_dates_1', models.ImageField(blank=True, upload_to='exam_pics/')),
                ('exam_dates_2', models.ImageField(blank=True, upload_to='exam_pics/')),
                ('summativ_note', models.TextField()),
                ('exam_details', models.TextField()),
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
                ('quiz_creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('group', models.ManyToManyField(related_name='quiz_group', to='main_page.Course')),
            ],
            options={
                'verbose_name_plural': 'Quizes',
            },
        ),
        migrations.CreateModel(
            name='StAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student', models.CharField(max_length=100)),
                ('first_hour', models.BooleanField(default=False)),
                ('second_hour', models.BooleanField(default=False)),
                ('attendance_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='usrr', serialize=False, to='auth.user')),
                ('image', models.ImageField(blank=True, default='/user.png', upload_to='profile_pics/')),
                ('phone_prefix', models.CharField(choices=[('Aze1', '050'), ('Aze2', '051'), ('Bak1', '055'), ('Bak2', '099'), ('Nar1', '070'), ('Nar2', '077')], default='Nar1', max_length=5)),
                ('phone_number', models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(message='Mobil n??mr?? 7 r??q??mli olmal??d??r. M??s: 1234567', regex='^\\d{7}$')])),
                ('birthdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='usr', serialize=False, to='auth.user')),
                ('image', models.ImageField(blank=True, default='/user.png', upload_to='profile_pics/')),
                ('phone_prefix', models.CharField(choices=[('Aze1', '050'), ('Aze2', '051'), ('Bak1', '055'), ('Bak2', '099'), ('Nar1', '070'), ('Nar2', '077')], default='Nar1', max_length=5)),
                ('phone_number', models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(message='Mobil n??mr?? 7 r??q??mli olmal??d??r. M??s: 1234567', regex='^\\d{7}$')])),
                ('birthdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=15)),
                ('last_name', models.CharField(max_length=15)),
                ('image', models.ImageField(blank=True, upload_to='team_member/')),
                ('member_detail', models.CharField(max_length=100)),
                ('member_role', models.CharField(default='', max_length=60)),
                ('facebook_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('email', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TicketSeller',
            fields=[
                ('seller_name', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('gform_url', models.URLField(db_column='Google Form url', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('u_shx_pin', models.CharField(max_length=7, primary_key=True, serialize=False, verbose_name="User's ID card pin")),
                ('u_name', models.CharField(max_length=20, validators=[main_page.models.all_models.check_name], verbose_name="User's name")),
                ('u_sname', models.CharField(max_length=20, verbose_name="User's surname")),
                ('u_phonenumberprefix', models.CharField(choices=[('Aze1', '050'), ('Aze2', '051'), ('Bak1', '055'), ('Bak2', '099'), ('Nar1', '070'), ('Nar2', '077')], default='Nar1', max_length=5, verbose_name='User Phone prefix')),
                ('u_phonenumber', models.CharField(blank=True, max_length=7, validators=[django.core.validators.RegexValidator(message='Mobil n??mr?? 7 r??q??mli olmal??d??r. M??s: 1234567', regex='^\\d{7}$')])),
                ('u_class', models.CharField(choices=[('5', '5-ci sinif'), ('6', '6-c?? sinif'), ('7', '7-ci sinif'), ('8', '8-ci sinif')], default='Rus', max_length=20, verbose_name="User's class")),
                ('u_regis_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name="User's registration date")),
                ('u_school', models.CharField(max_length=20, validators=[main_page.models.all_models.check_name], verbose_name='School')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attended', models.BooleanField(blank=True)),
                ('attendance_date', models.DateField(verbose_name=django.utils.timezone.now)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attended_teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentPaidAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paidAmount', models.FloatField(blank=True)),
                ('paidDate', models.DateField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='std_paid_amount', to='main_page.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StdPaymentAmount2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthlyAmount', models.FloatField(blank=True)),
                ('startDate', models.DateField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_payment_amount', to='main_page.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StdPaidAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paidAmount', models.FloatField(blank=True)),
                ('paidDate', models.DateField(auto_now=True)),
                ('paymnt', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_page.stdpaymentamount2')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('quiz_work_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_page.quiz')),
                ('std_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='coursess', to='main_page.StudentProfile'),
        ),
        migrations.AddField(
            model_name='course',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='courses', to='main_page.TeacherProfile'),
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
