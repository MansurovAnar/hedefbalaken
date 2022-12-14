import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from main_page.models.all_models import (TeacherProfile, StudentProfile,
                                 Course,
                                 Quiz, Question, Answer)
from main_page.models.journal_models import StAttendance
from django.contrib.auth.models import User

from main_page.models.all_models import user
# from .models import user, Course

from django.core.validators import RegexValidator
import datetime

from django.forms import formset_factory
from django.forms import BaseInlineFormSet

from django.utils.translation import ugettext_lazy as _

# Custom error messages test
# from django.forms import Field
# from django.utils.translation import ugettext_lazy
# Field.default_error_messages = {
#     'required': ugettext_lazy("Hello")
# }


this_year = datetime.date.today().year
YEARS = [x for x in range(1940, this_year + 1)]  # automaticaly takes from 1940 to current year

# Validator for phonenumber

phone_validator = RegexValidator(r"^[0-9]{7,7}$", message="Mobil nömrə 7 rəqəmdən ibarət olmalıdır")
PHONE_PREFIXES = (
    ('Aze1', '050'),
    ('Aze2', '051'),
    ('Bak1', '055'),
    ('Bak2', '099'),
    ('Nar1', '070'),
    ('Nar2', '077'),
)
# Course choices
# Creating a tuble of Courses with PK (first three letters of a Course) from DB
"""course_l = []
if Course:
    course_list = Course.objects.all()
else:
    course_list = []
count = 0
if course_list:
    if len(course_list) > 0:
        count = course_list.count()

    if count > 0:
        for i in range(count):
            course_l.append((course_list[i].c_id, course_list[i].c_name))

if course_l:
    COURSE_CHOICES = tuple(course_l)
else:
    COURSE_CHOICES = (
        ('YOX', 'Kurs yoxdur'),
    )"""
COURSE_CHOICES = (
    ('5', '5-ci sinif'),
    ('6', '6-cı sinif'),
    ('7', '7-ci sinif'),
    ('8', '8-ci sinif')
)

# END Course choices

def check_name(value):
    if len(value) < 3:
        raise forms.ValidationError("Ad minimum 3 hərfdən ibarət ola bilər")
    if not value.isalpha():
        raise forms.ValidationError("Ad ancaq böyük və kiçik hərflərdən ibarət ola bilər")


def check_surname(value):
    if len(value) < 3:
        raise forms.ValidationError("Soyad minimum 3 hərfdən ibarət ola bilər")
    if not value.isalpha():
        raise forms.ValidationError("Soyad ancaq böyük və kiçik hərflərdən ibarət ola bilər")


def check_fincode(value):
    pattern = re.compile("[A-Za-z0-9]+")
    if not pattern.fullmatch(value):
        raise forms.ValidationError("FİN kod ancaq hərf və rəqəmdən ibarət ola bilər")
    elif len(value) < 5 or len(value) == 6 or len(value) > 7:
        raise forms.ValidationError("FİN kodun uzunluğu 5 və ya 7 simvol ola bilər")


class RegisterForm(forms.ModelForm):
    """docstring - registeration from for users - new coming students"""
    error_css_class = 'error'
    required_css_class = 'required'

    u_shx_pin = forms.CharField(required=True, max_length=7, validators=[check_fincode, ],
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control-lg col-md-5',
                                        'placeholder': 'Şəxsiyyət vəsiqəsi FİN nömrəsi'
                                    }
                                )
                                )

    u_name = forms.CharField(required=True, validators=[check_name, ],
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control-lg col-md-5',
                                     'placeholder': 'Adınız',
                                 }
                             )
                             )

    u_sname = forms.CharField(required=True, validators=[check_surname, ],
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control-lg col-md-5',
                                      'placeholder': 'Soyadınız'
                                  }
                              )
                              )

    u_phonenumberprefix = forms.ChoiceField(choices=PHONE_PREFIXES, required=True,
                                            widget=forms.Select(attrs={'class': 'form-control-lg col-md-1'})
                                            )

    u_phonenumber = forms.CharField(
        label="Test field",
        required=True,  # Note: validators are not run against empty fields
        validators=[phone_validator],
        max_length=7,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-lg col-md-4',
                'placeholder': 'Mobil nömrə (e.g 1234567) '
            }
        )
    )

    u_class = forms.ChoiceField(choices=COURSE_CHOICES, required=True,
                                 widget=forms.Select(attrs={
                                     'class': 'form-control-lg col-md-5',
                                     'placeholder': 'Sinif'
                                 })
                                 )

    u_school = forms.CharField(required=True, validators=[check_name, ],
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control-lg col-md-5',
                                     'placeholder': 'Mətkəb adı',
                                 }
                             )
                             )

    class Meta(object):
        """docstring for Meta"""
        model = user
        fields = ['u_shx_pin', 'u_name', 'u_sname', 'u_phonenumberprefix', 'u_phonenumber', 'u_class', 'u_school']


class LoginUser(forms.Form):
    """ docstring - for Loggin all the users in the system"""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterUser(UserCreationForm):
    """ docsxtring - for Creating Dashboard users by the controller """
    username = forms.CharField(max_length=15,
                               required=True,
                               widget=forms.TextInput(attrs={
                                                            'class': 'form-control-lg col-md-5',
                                                            })
                               )
    first_name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control-lg col-md-5',
        }))
    last_name = forms.CharField(max_length=25, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control-lg col-md-5',
        }))
    email = forms.EmailField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control-lg col-md-5',
        }))

    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    # groups = forms.ChoiceField(required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', "password1", "password2", "groups")


class TeacherProfileForm(forms.ModelForm):
    # image = forms.ImageField()
    phone_prefix = forms.ChoiceField(choices=PHONE_PREFIXES, required=True,
                                     widget=forms.Select(attrs={'class': 'form-control-lg col-md-1'})
                                     )
    phone_number = forms.CharField(
        required=True,  # Note: validators are not run against empty fields
        validators=[phone_validator],
        max_length=7,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-lg col-md-4',
                'placeholder': 'Mobil nömrə (e.g 1234567) '
            }
        )
    )
    birthdate = forms.DateField(required=True,
                                widget=forms.SelectDateWidget(years=YEARS,
                                                              attrs={
                                                                  'class': 'form-control-lg col-md-1.5'
                                                              }
                                                              )
                                )
    status = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = TeacherProfile
        fields = ('image', 'phone_prefix', 'phone_number', 'birthdate', 'status')


class StudentProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    phone_prefix = forms.ChoiceField(choices=PHONE_PREFIXES, required=True,
                                     widget=forms.Select(attrs={'class': 'form-control-lg col-md-1'})
                                     )
    phone_number = forms.CharField(
        required=True,  # Note: validators are not run against empty fields
        validators=[phone_validator],
        max_length=7,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-lg col-md-4',
                'placeholder': 'Mobil nömrə (e.g 1234567) '
            }
        )
    )
    birthdate = forms.DateField(required=True,
                                widget=forms.SelectDateWidget(years=YEARS,
                                                              attrs={
                                                                  'class': 'form-control-lg col-md-1.5'
                                                              }
                                                              )
                                )
    status = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = StudentProfile
        fields = ('image', 'phone_prefix', 'phone_number', 'birthdate','status')


class CourseCreate(forms.ModelForm):
    """ docstring - for Creating Course, new course"""

    c_id = forms.CharField(required=True, max_length=4, error_messages={"unique": "Id unique olmalidir"})
    c_name = forms.CharField(required=True, max_length=20)
    c_status = forms.BooleanField(initial=True, required=False)
    c_description = forms.CharField(max_length=200, required=False, widget=forms.Textarea)
    c_photo = forms.ImageField()
    teachers = forms.ModelMultipleChoiceField(
        required=False,
        queryset=TeacherProfile.objects.filter(status=True),
        widget=forms.CheckboxSelectMultiple
    )
    students = forms.ModelMultipleChoiceField(
        required=False,
        queryset=StudentProfile.objects.filter(status=True),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Course
        fields = ('c_id', 'c_name', 'c_status', 'c_description', 'c_photo', 'teachers', 'students')


# ~~~~~~~~ Quiz Forms ~~~~~~~~~~```

class QuizForm(forms.ModelForm):
    number_of_questions = forms.IntegerField(required=False, initial=0)
    group = forms.ModelMultipleChoiceField(
        required=False,
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Quiz
        fields = ('name', 'number_of_questions', 'time', 'status', 'group')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(QuizForm, self).__init__(*args, **kwargs)

        if self.request:
            current_user_group = self.request.user.groups.all()
            for group in current_user_group:
                if group.name == "controller":
                    self.fields["group"].queryset = Course.objects.all()
                elif group.name == "teacher":
                    self.fields["group"].queryset = Course.objects.filter(
                        teachers__in=TeacherProfile.objects.filter(
                            user=self.request.user
                        )
                    )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'image')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', 'correct')

        labels = {
            'text': "",
            'correct': _('Doğrudur '),
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Variantı daxil edin', 'style': "align:left;color:#3299a8;border-radius:10px; width: 90%; margin: 30px;"}),
            'correct': forms.CheckboxInput(attrs={'title': 'Doğrudursa kliklə'})
        }

class CustomAnswerInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomAnswerInlineFormset, self).__init__(*args, **kwargs)
        # self.forms.widget.attrs.update({'placeholder': 'User Name'})

        for form in self.forms:
            print("\n\n")
            for field in form.fields:
                print(field)
                form.fields['text'].widget.attrs.update({'class': 'form-control',
                                                         'placeholder': 'Variantı daxil edin',
                                                         'style': "align:left;color:#3299a8;border-radius:10px; width: 90%; margin: 30px;"})
                form.fields['text'].label = "Variant"
                # form.fields['correct'].widget.attrs.update({'style': "margin-botton:30%; margin-top:20px;"})
                form.fields['correct'].label = "Doğru"
                # form.fields['DELETE'].widget.attrs.update({'style': "padding:30%;margin-top:20%;"})
                form.fields['DELETE'].label = "Sil"

class CustomInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            print("Inside CUSTOM INLINE FORMSET- FORM \n: ", form)

class StudentIDNumberForm(forms.Form):
    id_number = forms.CharField(required=True,
                                max_length=7,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control-lg col-md-4',
                                        'placeholder': 'İş nömrəsi (e.g 7212222) '
                                    }
                                )
                                )

class StudentAttendanceForm(forms.ModelForm):
    first_hour = forms.BooleanField(required=False)
    second_hour = forms.BooleanField(required=False)
    student = forms.CharField(required=False)
    class Meta:
        model = StAttendance
        fields = ('student', 'first_hour', 'second_hour',)