from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from django import forms

PHONE_PREFIXES = (
    ('Aze1', '050'),
    ('Aze2', '051'),
    ('Bak1', '055'),
    ('Bak2', '099'),
    ('Nar1', '070'),
    ('Nar2', '077'),
)


def check_name(value):
    if len(value) < 3:
        raise forms.ValidationError("Ad minimum 3 simvol olmalıdır")


# Below function not Working yet
def validate_hash(value):
    reg = re.compile('^[0-9]{7,7}$')
    if not reg.match(value):
        raise ValidationError(u'%s must be 7 ' % value)


class TeacherProfile(models.Model):
    """ docstring for Teacher model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="usr")
    image = models.ImageField(upload_to="profile_pics/", blank=True, default="/user.png")
    phone_regex = RegexValidator(regex=r'^\d{7}$', message="Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567")
    phone_prefix = models.CharField(max_length=5, choices=PHONE_PREFIXES, default='Nar1')
    phone_number = models.CharField(validators=[phone_regex], max_length=7, blank=True)
    birthdate = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        full_name = self.user.first_name + " " + self.user.last_name
        return full_name

    def get_groups(self):
        return self.courses.all()

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__teacherprofile"
        app_label = "main_page"

class StudentProfile(models.Model):
    """ docstring for Student model"""

    student = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="usrr")
    image = models.ImageField(upload_to="profile_pics/", blank=True, default="/user.png")
    phone_regex = RegexValidator(regex=r'^\d{7}$', message="Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567")
    phone_prefix = models.CharField(max_length=5, choices=PHONE_PREFIXES, default='Nar1')
    phone_number = models.CharField(validators=[phone_regex], max_length=7, blank=True)
    birthdate = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        full_name = self.student.first_name + " " + self.student.last_name
        return full_name

    def get_groups(self):
        return self.coursess.all()

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__studentprofile"
        app_label = "main_page"

# Create your models here.
class Course(models.Model):
    """docstring for Course Model"""
    c_id = models.CharField("Course_ID", max_length=4, default="NON", unique=True)
    c_name = models.CharField("Course_name", max_length=20, default="")
    c_status = models.BooleanField(default=True)
    c_description = models.TextField(blank=True)
    c_photo = models.ImageField(upload_to="Courses/", default="")
    # c_cost = models.CharField("Cost of course", max_length=8, blank=True, default="0")
    teachers = models.ManyToManyField(TeacherProfile, related_name="courses", blank=True)
    students = models.ManyToManyField(StudentProfile, related_name="coursess", blank=True)

    def __str__(self):
        return self.c_name


class user(models.Model):
    """docstring for User model"""

    # Creating a tuble of Courses with PK (first three letters of a Course) from DB
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    COURSE_CHOICES = (
        ('5', '5-ci sinif'),
        ('6', '6-cı sinif'),
        ('7', '7-ci sinif'),
        ('8', '8-ci sinif')
    )

    u_shx_pin = models.CharField("User's ID card pin", max_length=7, primary_key=True)
    # u_exam_id = models.CharField("Exam ID", max_length=10, primary_key=True)
    u_name = models.CharField("User's name", max_length=20, validators=[check_name, ])
    u_sname = models.CharField("User's surname", max_length=20)

    phone_regex = RegexValidator(regex=r'^\d{7}$', message="Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567")
    u_phonenumberprefix = models.CharField("User Phone prefix", max_length=5, choices=PHONE_PREFIXES, default='Nar1')
    u_phonenumber = models.CharField(validators=[phone_regex], max_length=7, blank=True)
    # u_birthdate = models.DateField("User's birthdate", auto_now=False)
    u_class = models.CharField("User's class", max_length=20, choices=COURSE_CHOICES, default='Rus')
    u_regis_date = models.DateTimeField("User's registration date", default=timezone.now)
    u_school = models.CharField("School", max_length=20, validators=[check_name, ])

    def __str__(self):
        full_name = self.u_name + " " + self.u_sname
        return full_name

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__user"
        app_label = "main_page"

class MediaAccounts(models.Model):
    media_name = models.CharField("Social Media Name", max_length=25)
    media_url = models.URLField("The URL of Account", max_length=300)

    def __str__(self):
        return self.MediaName

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__mediaaccounts"
        app_label = "main_page"


class CompanyContacts(models.Model):
    contact_name = models.CharField("Contact Form", max_length=25)
    contact_data = models.CharField("Contact Info", max_length=20)

    def __str__(self):
        return self.contact_name

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__companycontacts"
        app_label = "main_page"


class Branches(models.Model):
    branch_name = models.CharField("Branch name", max_length=50)
    branch_short_desc = models.CharField("Short desciption - 300 characters", max_length=300)
    branch_details = models.TextField("Large information - 2000 characters", max_length=2000)
    branch_contact = models.ForeignKey(CompanyContacts, on_delete=models.CASCADE)
    branch_location = models.URLField("Google Map location", max_length=300)

    def __str__(self):
        return self.branch_name

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__branches"
        app_label = "main_page"

# ~~~~~~~~~~~~~~~~ Quiz models ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Quiz(models.Model):
    name = models.CharField(max_length=120)
    number_of_questions = models.IntegerField(help_text="Number of Quiz's questions")
    time = models.IntegerField(help_text="Duration of quiz in minutes", blank=True, null=True)
    status = models.BooleanField("Akitv|Deaktiv", null=False)
    group = models.ManyToManyField(Course, related_name="quiz_group")
    quiz_creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def get_questions(self):
        return self.question_set.all()

    def get_question_count(self):
        return self.question_set.count()

    class Meta:
        verbose_name_plural = "Quizes"
        # db_table = "main_paige__quizes"
        app_label = "main_page"

class Question(models.Model):
    text = models.CharField(max_length=200)
    image = models.ImageField(null=True,
                              blank=True, upload_to="questions/")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def get_answers(self):
        return self.answer_set.all()

    def get_variants_count(self):
        return self.answer_set.count()

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__question"
        app_label = "main_page"


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

    def get_queryset(self):
        return super().get_queryset().filter(self.question == Question.id)

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__answer"
        app_label = "main_page"


class Result(models.Model):
    """This model saves the results which student has done"""
    std_user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    quiz_work_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        result = self.std_user.first_name + ' ' + self.std_user.last_name + ', ' + self.quiz.name
        return str(result)

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__result"
        app_label = "main_page"


class FrontPageData(models.Model):
    announcement = models.ImageField(upload_to="exam_pics/", blank=True)
    slogan = models.CharField(max_length=50)
    description_header = models.CharField(max_length=50)
    description = models.TextField()
    subscription_header = models.CharField(max_length=50)
    subscription_text = models.CharField(max_length=100)
    subscription_form_header = models.TextField(max_length=100)
    our_specialities_header = models.CharField(max_length=50)
    our_specialities_desc = models.TextField()
    our_specialities_1 = models.CharField(max_length=50)
    our_specialities_1_desc = models.TextField()
    our_specialities_2 = models.CharField(max_length=50)
    our_specialities_2_desc = models.TextField()
    our_specialities_3 = models.CharField(max_length=50)
    our_specialities_3_desc = models.TextField()
    our_specialities_4 = models.CharField(max_length=50)
    our_specialities_4_desc = models.TextField()
    exam_dates_1 = models.ImageField(upload_to="exam_pics/", blank=True)
    exam_dates_2 = models.ImageField(upload_to="exam_pics/", blank=True)
    summativ_note = models.TextField()
    exam_details = models.TextField()

    def __str__(self):
        f_page = "Ana seh detallari"
        return f_page

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__frontpagedata"
        app_label = "main_page"


class TeamMember(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    image = models.ImageField(upload_to="team_member/", blank=True)
    member_detail = models.CharField(max_length=100)
    member_role = models.CharField(max_length=60, default="")
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    email = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "Komanda üzvü - " + str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__teammember"
        app_label = "main_page"


class FrontMenuNames(models.Model):
    courses_exams = models.CharField(max_length=30)
    about_us = models.CharField(max_length=30)
    contacts = models.CharField(max_length=30)

    def __str__(self):
        return str("Menu Names")

    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        # db_table = "main_paige__frontmenunames"
        app_label = "main_page"