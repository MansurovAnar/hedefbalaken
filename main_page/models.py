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

    def __str__(self):
        return self.user.username

    def get_groups(self):
        return self.courses.all()


class StudentProfile(models.Model):
    """ docstring for Student model"""

    student = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="usrr")
    image = models.ImageField(upload_to="profile_pics/", blank=True, default="/user.png")
    phone_regex = RegexValidator(regex=r'^\d{7}$', message="Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567")
    phone_prefix = models.CharField(max_length=5, choices=PHONE_PREFIXES, default='Nar1')
    phone_number = models.CharField(validators=[phone_regex], max_length=7, blank=True)
    birthdate = models.DateField()

    def __str__(self):
        return self.student.username

    def get_groups(self):
        return self.coursess.all()

# Create your models here.
class Course(models.Model):
    """docstring for Course Model"""
    c_id = models.CharField("Course_ID", max_length=4, default="NON")
    c_name = models.CharField("Course_name", max_length=20, default="")
    c_status = models.BooleanField(default=True)
    c_description = models.TextField(blank=True)
    c_photo = models.ImageField(upload_to="Courses/", default="")
    # c_cost = models.CharField("Cost of course", max_length=8, blank=True)
    teachers = models.ManyToManyField(TeacherProfile, related_name="courses", blank=True)
    students = models.ManyToManyField(StudentProfile, related_name="coursess", blank=True)

    def __str__(self):
        return self.c_name


class user(models.Model):
    """docstring for User model"""

    # Creating a tuble of Courses with PK (first three letters of a Course) from DB
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # if Course.objects.all():
    #     course_l = []
    #     course_list = Course.objects.all()
    #     count = course_list.count()
    #
    #     for i in range(count):
    #         course_l.append((course_list[i].c_id, course_list[i].c_name))
    #     COURSE_CHOICES = tuple(course_l)
    # else:
    #     COURSE_CHOICES = (
    #         ('Yox1', 'Kurs yoxdur'),
    #     )

    COURSE_CHOICES = (
        ('Yox1', 'Kurs yoxdur'),
        ('Eng', 'English')
    )

    u_shx_pin = models.CharField("User's ID card pin", max_length=7, primary_key=True)
    u_name = models.CharField("User's name", max_length=20, validators=[check_name, ])
    u_sname = models.CharField("User's surname", max_length=20)

    phone_regex = RegexValidator(regex=r'^\d{7}$', message="Mobil nömrə 7 rəqəmli olmalıdır. Məs: 1234567")
    u_phonenumberprefix = models.CharField("User Phone prefix", max_length=5, choices=PHONE_PREFIXES, default='Nar1')
    u_phonenumber = models.CharField(validators=[phone_regex], max_length=7, blank=True)
    u_birthdate = models.DateField("User's birthdate", auto_now=False)
    u_course = models.CharField("User's course", max_length=20, choices=COURSE_CHOICES, default='Rus')
    u_regis_date = models.DateTimeField("User's registration date", default=timezone.now)

    def __str__(self):
        full_name = self.u_name + " " + self.u_sname
        return full_name


class MediaAccounts(models.Model):
    media_name = models.CharField("Social Media Name", max_length=25)
    media_url = models.URLField("The URL of Account", max_length=300)

    def __str__(self):
        return self.MediaName


class CompanyContacts(models.Model):
    contact_name = models.CharField("Contact Form", max_length=25)
    contact_data = models.CharField("Contact Info", max_length=20)

    def __str__(self):
        return self.contact_name


class Branches(models.Model):
    branch_name = models.CharField("Branch name", max_length=50)
    branch_short_desc = models.CharField("Short desciption - 300 characters", max_length=300)
    branch_details = models.TextField("Large information - 2000 characters", max_length=2000)
    branch_contact = models.ForeignKey(CompanyContacts, on_delete=models.CASCADE)
    branch_location = models.URLField("Google Map location", max_length=300)

    def __str__(self):
        return self.branch_name


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


class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

    def get_queryset(self):
        return super().get_queryset().filter(self.question == Question.id)


class Result(models.Model):
    """This model saves the results which student has done"""
    std_user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField()
    quiz_work_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        result = self.std_user.first_name + ' ' + self.std_user.last_name + ', ' + self.quiz.name
        return str(result)
