from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

from .decorators import allowed_users
from .forms import (RegisterForm, LoginUser,
                    CourseCreate, TeacherProfileForm,
                    StudentProfileForm,
                    QuestionForm, AnswerForm,
                    QuizForm,
                    StudentIDNumberForm
                    )
from .forms import RegisterUser, CustomAnswerInlineFormset
from main_page.models.all_models import (Course, TeacherProfile,
                                 StudentProfile, Quiz,
                                 Question, Answer, Result, FrontPageData,
                                 TeamMember, FrontMenuNames
                                 )
from main_page.models.payment_models import StdPaymentAmount2
from .queries import (QuizData, QuizDataForTeacher)
from django.http import FileResponse
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
import datetime

def index(request):
    front_data = FrontPageData.objects.all()
    menu_names = FrontMenuNames.objects.all()
    context = {"front_data": front_data, "menu_name": menu_names}
    return render(request, 'main_page/index.html', context)


def about(request):
    team_members = TeamMember.objects.all()
    front_data = FrontPageData.objects.all()
    context = {"team_members": team_members, "front_data": front_data}
    return render(request, 'main_page/about.html', context)


@csrf_protect
def register(request):
    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        print(reg_form)
        if reg_form.is_valid():
            print(reg_form)
            reg_form.save()
    else:
        reg_form = RegisterForm()
    context = {'reg_form': reg_form}
    return render(request, 'main_page/Registration.html', context)


######################################################################################
@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'reception'])
def registeruser(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)

        if form.is_valid():
            the_user = form.save()
            assigned_group = form.cleaned_data['groups'].values('id')
            the_user.groups.add(assigned_group)
            messages.success(request, "Istifad????i profili yarad??ld??")
        else:
            messages.error(request, "D??z??li??l??r laz??md??r")
    else:
        form = RegisterUser()
    context = {'form_reg': form}
    return render(request, "main_page/accounts/register.html", context)


@csrf_protect
def loginUser(request):
    if request.user.is_authenticated:
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = LoginUser(request.POST)

            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=cd['username'],
                                    password=cd['password'])

                if user is not None:
                    login(request, user)
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('dashboard')
                else:
                    messages.info(request, 'Istifad????i ad?? v?? ya parol s??hvdir')
        else:
            form = LoginUser()

        context = {'form': form}
        return render(request, 'main_page/accounts/index_login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def password_reset(request):
    return render(request, 'main_page/accounts/password_reset.html')


def password_reset_done(request):
    return render(request, 'main_page/accounts/password_reset_done.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


###########################################################################################

def courses(request):
    course_list = Course.objects.all()
    menu_names = FrontMenuNames.objects.all()
    args = {'courses': course_list, "menu_name": menu_names}
    return render(request, 'main_page/courses.html', args)


def whatsapp_redirect(request):
    return HttpResponseRedirect('https://wa.me/00994505242346')


##########################################################################

@xframe_options_sameorigin
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'main_page/dashboard/dashboard.html')


@login_required(login_url='login')
def notifications(request):
    return render(request, 'main_page/dashboard/notifications.html')


@login_required(login_url='login')
def tables(request):
    return render(request, 'main_page/dashboard/tables.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def students_table(request):
    students_info = StudentProfile.objects.all().order_by('-status')

    context = {
                'students_info': students_info,
                'previous_page': request.META.get('HTTP_REFERER'),
               }
    return render(request, 'main_page/dashboard/students_table.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def students_table_for_teacher(request):
    students_info = StudentProfile.objects.all()
    teacher_info = TeacherProfile.objects.all()
    teachers_student_detail = {}
    quizData = QuizDataForTeacher(request)

    for tcr in teacher_info:
        teacher_students = []
        for grp in tcr.get_groups():
            for std in students_info:
                if std.status:
                    for std_grp in std.get_groups():
                        if std_grp == grp:
                            if not (std in teacher_students):
                                teacher_students.append(std)
        teachers_student_detail[str(tcr)] = teacher_students

    std_results_for_tcr = quizData.get_results_for_teacher()
    print("Student results:", std_results_for_tcr)

    context = {'students_info': students_info, 'teacher_students': teachers_student_detail,
               'std_results': std_results_for_tcr
               }
    return render(request, 'main_page/dashboard/students_table_for_teacher.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def teachers_table(request):
    teacher_info = TeacherProfile.objects.all().order_by('-status')
    teacher_info_detail = {}
    students = StudentProfile.objects.all()
    teachers_student_detail = {}

    for teacher in teacher_info:
        teacher_groups = []
        if teacher.get_groups():
            for group in teacher.get_groups():
                teacher_groups.append(group)
            teacher_info_detail[str(teacher)] = teacher_groups

    for tcr in teacher_info:
        teacher_students = []
        for grp in tcr.get_groups():
            for std in students:
                for std_grp in std.get_groups():
                    if std_grp == grp:
                        if not (std in teacher_students):
                            teacher_students.append(std)
        teachers_student_detail[str(tcr)] = teacher_students

    context = {'teacher_info': teacher_info,
               'teacher_info_detail': teacher_info_detail,
               'teachers_students': teachers_student_detail}
    return render(request, 'main_page/dashboard/teachers_table.html', context)


@login_required(login_url='login')
def courses_in_dashboard(request):
    courses_list = Course.objects.all().order_by('-c_status')
    context = {'courses': courses_list}
    return render(request, 'main_page/dashboard/course_tables.html', context)


@login_required(login_url='login')
def create_course(request):
    context = {}
    if request.method == 'POST':
        courseForm = CourseCreate(request.POST, request.FILES)

        if courseForm.is_valid():
            crs = courseForm.save(commit=False)

            crs.save()
            courseForm.save_m2m()

            # sechilmish telebeler Payment cedveline elave edilir
            selected_students = courseForm.cleaned_data['students']
            added_students = list(set(selected_students))
            if added_students:
                for added_student in added_students:
                    StdPaymentAmount2.objects.create(group=crs, student=added_student,
                                                     monthlyAmount=0, startDate=datetime.date.today(),
                                                     status=True)

            courseForm = CourseCreate()
            context['courseForm'] = courseForm
            context['success'] = True
            context['created_course'] = crs
            messages.success(request, '"' + str(crs) + '"' + " qrupu yarad??ld??.")
            return render(request, 'main_page/dashboard/course_form.html', context)
        else:
            error_context = """
                Qrup ID unique olmal??d??r.
            """
            messages.error(request, error_context)
    else:
        courseForm = CourseCreate()
    context['courseForm'] = courseForm
    context['success'] = False
    return render(request, 'main_page/dashboard/course_form.html', context)


@login_required(login_url='login')
def update_course(request, pk):
    context = {}
    course = get_object_or_404(Course, pk=pk)
    previous_students = course.students.all()
    courseForm = CourseCreate(request.POST or None, instance=course)

    if courseForm.is_valid():
        course_form = courseForm.save(commit=False)
        if 'c_photo' in request.FILES:
            print('Found it')
            course_form.c_photo = request.FILES['c_photo']
        current_students = courseForm.cleaned_data['students']

        added_students = list(set(current_students) - set(previous_students))
        deleted_students = list(set(previous_students) - set(current_students))
        if added_students:
            for added_student in added_students:
                StdPaymentAmount2.objects.update_or_create(group=course_form,
                                                           student=added_student,
                                                           monthlyAmount=0, startDate=datetime.date.today(),
                                                           defaults={"status": True})

        if deleted_students:
            for deleted_student in deleted_students:
                StdPaymentAmount2.objects.filter(student=deleted_student).update(status=False)

        course_form.save()
        courseForm.save_m2m()

        messages.success(request, '"' + str(course_form) + '"' + " qrupu haqq??nda m??lumat yenil??ndi.")

        return redirect('dashboardcourses')

    context['courseForm'] = courseForm

    return render(request, 'main_page/dashboard/course_form.html', context)


@login_required(login_url='login')
def course_detail(request, cid):
    crs = Course.objects.get(c_id=cid)
    context = {"crs_detail": crs}

    return render(request, 'main_page/dashboard/course_detail.html', context)

@login_required(login_url='login')
def delete_course(request, pk):
    crs = Course.objects.get(pk=pk)
    crs.delete()

    return redirect("dashboardcourses")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TEACHER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def create_teacher(request):
    if request.method == 'POST':
        user_form = RegisterUser(data=request.POST)
        teacher_form = TeacherProfileForm(data=request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            my_group = Group.objects.get(name='teacher')
            user = user_form.save()
            my_group.user_set.add(user.id)
            user.save()

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            if 'image' in request.FILES:
                print('Found it')
                teacher.image = request.FILES['image']

            teacher.save()

            messages.success(request, '"' + str(teacher) + '"' + " istifad????i adl?? m????llim yarad??ld??.")

            user_form = RegisterUser()
            teacher_form = TeacherProfileForm()

            contextt = {"userForm": user_form, "teacherForm": teacher_form,
                        "success": True, "created_teacher": str(teacher),
                        }
            return render(request, 'main_page/dashboard/teacher_form.html', contextt)
        else:
            print(user_form.errors, teacher_form.errors)
    else:
        user_form = RegisterUser()
        teacher_form = TeacherProfileForm()
    context = {"userForm": user_form, "teacherForm": teacher_form,
               }
    return render(request, 'main_page/dashboard/teacher_form.html', context)

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def update_teacher(request, id):
    context = {}
    teacher = get_object_or_404(TeacherProfile, pk=id)

    teacherForm = TeacherProfileForm(request.POST or None, instance=teacher)

    if teacherForm.is_valid():
        teacher_form = teacherForm.save(commit=False)
        if 'image' in request.FILES:
            teacher_form.image = request.FILES['image']
        teacher_form.save()

        messages.success(request, '"' + str(teacher_form) + '"' + " m????llimi haqq??nda m??lumat yenil??ndi.")
        return redirect('teachers')
    context['teacherForm'] = teacherForm
    context['teacher'] = teacher
    return render(request, 'main_page/dashboard/teacher_update_form.html', context)

@login_required(login_url='login')
def teacher_detail(request, pk):
    teachers_student = []
    teacher = get_object_or_404(TeacherProfile, pk=pk)
    students = StudentProfile.objects.all()

    for crs in teacher.courses.all():
        for std in students:
            if std.coursess.filter(c_name=crs):
                teachers_student.append(std)
    #             print("Student- {}, course- {} ".format(std, std.coursess.filter(c_name=crs)))
    # print("Teacher's students", teachers_student)
    context = {"teacher_detail": teacher, "teachers_student": teachers_student}

    return render(request, 'main_page/dashboard/teacher_detail.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher', 'student', 'controller'])
def my_profile(request):
    html_file = ""
    context = {}
    PHONE_PREFIXES = (
        ('Aze1', '050'),
        ('Aze2', '051'),
        ('Bak1', '055'),
        ('Bak2', '099'),
        ('Nar1', '070'),
        ('Nar2', '077'),
    )
    current_user = request.user
    user_groups = current_user.groups.all()
    for rol in user_groups:
        if rol.name == "teacher":
            html_file = "teacher_profile.html"
            teacher_students = []
            teacher_courses = []
            teacher = get_object_or_404(TeacherProfile, pk=current_user.pk)

            if teacher.courses.all():
                students = StudentProfile.objects.all()
                for crs in teacher.courses.all():
                    teacher_courses.append(crs)
                    if students:
                        for std in students:
                            if std.coursess.filter(c_name=crs):
                                teacher_students.append(std)
                                # print("Student- {}, course- {} ".format(std, std.coursess.filter(c_name=crs)))
                    else:
                        teacher_students.append("Yoxdur")
            else:
                teacher_courses.append("Yoxdur")

            user_phonePrefix = dict(PHONE_PREFIXES).get(current_user.usr.phone_prefix)
            context = {"user": current_user, "user_groups": user_groups,
                       "prefix": user_phonePrefix, "students": teacher_students,
                       "courses": teacher_courses}
        elif rol.name == 'controller':
            html_file = "controller_profile.html"
            context = {"user": current_user, "user_groups": user_groups, }

        elif rol.name == "student":
            html_file = "student_profile.html"
            student_courses = []
            student_teachers = []
            student = get_object_or_404(StudentProfile, pk=current_user.pk)
            if student.coursess.all():
                teachers = TeacherProfile.objects.all()
                for crs in student.coursess.all():
                    student_courses.append(crs)
                    if teachers:
                        for tcr in teachers:
                            if tcr.courses.filter(c_name=crs):
                                student_teachers.append(tcr)
                                print("Teacher- {}, course- {} ".format(tcr, tcr.courses.filter(c_name=crs)))
                    else:
                        student_teachers.append("Yoxdur")

            else:
                student_courses.append("Yoxdur")

            user_phonePrefix = dict(PHONE_PREFIXES).get(current_user.usrr.phone_prefix)
            context = {"user": current_user, "user_groups": user_groups,
                       "prefix": user_phonePrefix, "teachers": student_teachers,
                       "courses": student_courses}

    return render(request, 'main_page/dashboard/{}'.format(html_file), context)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ END TEACHER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def create_student(request):
    if request.method == 'POST':
        user_form = RegisterUser(data=request.POST)
        student_form = StudentProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            my_group = Group.objects.get(name='student')
            user = user_form.save()
            my_group.user_set.add(user.id)
            user.save()

            stdnt = student_form.save(commit=False)
            stdnt.student = user
            if 'image' in request.FILES:
                stdnt.image = request.FILES['image']
            stdnt.save()
            # student_form.save_m2m()

            # print("[ INFO ] Student form SAVED")
            # Initial Payment for new student
            initial_group = Course.objects.get(c_id='TST')
            payment = StdPaymentAmount2.objects.create(
                group=initial_group, student=stdnt, monthlyAmount=0, startDate=datetime.date.today()
            )
            # print("PAYMENT: ", payment)
            messages.success(request, '"' + str(stdnt) + '"' + " istifad????i adl?? t??l??b?? yarad??ld??.")
            user_form = RegisterUser()
            student_form = StudentProfileForm()
            contextt = {"userForm": user_form, "studentForm": student_form,
                        # "success": True, "created_student": str(stdnt)
                        }
            return render(request, 'main_page/dashboard/student_form.html', contextt)
        else:
            messages.error(request, user_form.errors)
            messages.error(request, student_form.errors)
            print(user_form.errors, student_form.errors)
    else:
        user_form = RegisterUser()
        student_form = StudentProfileForm()
    context = {"userForm": user_form, "studentForm": student_form}
    return render(request, 'main_page/dashboard/student_form.html', context)

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def update_student(request, id):
    context = {}
    student = get_object_or_404(StudentProfile, pk=id)

    studentForm = StudentProfileForm(request.POST or None, instance=student)

    if studentForm.is_valid():
        student_form = studentForm.save(commit=False)
        if 'image' in request.FILES:
            student_form.image = request.FILES['image']
        student_form.save()
        messages.success(request, '"' + str(student_form) + '"' + " t??l??b??si haqq??nda m??lumat yenil??ndi.")
        return redirect('students')
    context['studentForm'] = studentForm
    context['student'] = student
    return render(request, 'main_page/dashboard/student_update_form.html', context)

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def student_detail(request, id):
    context = {}
    PHONE_PREFIXES = (
        ('Aze1', '050'),
        ('Aze2', '051'),
        ('Bak1', '055'),
        ('Bak2', '099'),
        ('Nar1', '070'),
        ('Nar2', '077'),
    )
    student = get_object_or_404(StudentProfile, pk=id)
    student_phonePrefix = dict(PHONE_PREFIXES).get(student.phone_prefix)

    context['student'] = student
    context['prefix'] = student_phonePrefix
    return render(request, 'main_page/dashboard/student_detail.html', context)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###########################  Yeni Quiz, Question, Answer modell??ri ??z??rind?? test viewlar #######################

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def add_quiz(request):
    """ This view is for TEACHERs and controllers - only teachers and controllers can create quizes"""
    quizes = Quiz.objects.all()
    if request.method == 'POST':
        quiz_form = QuizForm(data=request.POST, request=request)
        if quiz_form.is_valid():
            quiz_instance = quiz_form.save(commit=False)
            quiz_instance.number_of_questions = 0
            quiz_instance.save()
            quiz_form.save()

            messages.success(request, '"' + str(quiz_instance) + '"' + " imtahan?? yarad??ld??.")
            context = {"quiz": QuizForm(request=request), "quizes": quizes}
            return render(request, 'main_page/dashboard/quiz_app/add_quiz.html', context)
    else:
        quiz_form = QuizForm(request=request)
    context = {"quiz": quiz_form, "quizes": quizes}
    return render(request, 'main_page/dashboard/quiz_app/add_quiz.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def update_quiz(request, quiz_id):
    """ This view is for TEACHERs and controllers - only teachers and controllers can update quizes"""
    quizes = Quiz.objects.all()
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quizForm = QuizForm(request.POST or None, instance=quiz, request=request)

    if quizForm.is_valid():
        quiz_form = quizForm.save(commit=False)
        quiz_form.number_of_questions = quiz.get_question_count()
        quiz_form.save()
        quizForm.save()

        messages.success(request, '"' + str(quiz_form) + '"' + " imtahan?? haqq??nda m??lumat yenil??ndi.")

        return HttpResponseRedirect(
            reverse('createquiz')
        )
    else:
        print(quizForm.errors)

    context = {"quiz": quizForm, "quizes": quizes, "update": True}
    return render(request, 'main_page/dashboard/quiz_app/add_quiz.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def add_question(request, id):
    quiz = Quiz.objects.get(id=id)

    if request.method == 'POST':
        question_form = QuestionForm(data=request.POST)

        if question_form.is_valid():
            question_instance = question_form.save(commit=False)
            question_instance.quiz = Quiz.objects.get(id=int(id))

            if 'image' in request.FILES:
                question_instance.image = request.FILES['image']

            question_instance.save()
            question_form.save()

            return HttpResponseRedirect(
                reverse('addvariants', kwargs={'id': question_instance.id})
            )
        else:
            print(question_form.errors)

    questions = Question.objects.filter(quiz=Quiz.objects.get(id=int(id)))
    answers = Question.get_answers()
    context = {"quiz": quiz, "questions": questions, "answer": answers, "question_form": QuestionForm(),
               "answer": AnswerForm()}

    return render(request, 'main_page/dashboard/quiz_app/add_question.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def update_question(request, quiz_id, question_id):
    quiz = Quiz.objects.get(id=quiz_id)
    question = get_object_or_404(Question, id=question_id)
    questionForm = QuestionForm(request.POST or None, instance=question)

    if questionForm.is_valid():
        question_form = questionForm.save(commit=False)
        question_form.quiz = quiz
        if 'image' in request.FILES:
            question_form.image = request.FILES['image']
        question_form.save()
        questionForm.save()

        messages.success(request, '"' + str(question_form) + '"' + " sual?? haqq??nda m??lumat yenil??ndi.")
        questions = Question.objects.filter(quiz=Quiz.objects.get(id=quiz_id))

        # context = {"question_form": QuestionForm(), "quiz": quiz, "questions":questions}
        return HttpResponseRedirect(
            reverse('addquestion', kwargs={'id': question.quiz.id})
        )
        # return render(request, 'main_page/dashboard/quiz_app/add_question.html', context)

    questions = Question.objects.filter(quiz=Quiz.objects.get(id=quiz_id))
    context = {"question_form": questionForm, "quiz": quiz, "questions": questions, "answer": AnswerForm(),
               "update": True}
    return render(request, 'main_page/dashboard/quiz_app/add_question.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def add_variants(request, id):
    question = Question.objects.get(id=int(id))
    print("QUESTION Quiz ID: ", question.quiz.id)

    if request.method == 'POST':
        answer_form = AnswerForm(data=request.POST)

        if answer_form.is_valid():
            instance = answer_form.save(commit=False)
            instance.question = question

            instance.save()
            answer_form.save()

            messages.success(request, '"' + str(instance.text) + '"' + " variant?? ??lav?? edildi.")
            variants = Answer.objects.filter(question=question)

            context = {'form': AnswerForm(), 'question': question, 'variants': variants}
            return render(request, 'main_page/dashboard/quiz_app/add_variants.html', context)
        else:
            print(answer_form.errors)

    variants = Answer.objects.filter(question=question)

    context = {'form': AnswerForm(), 'question': question, 'variants': variants}
    return render(request, 'main_page/dashboard/quiz_app/add_variants.html', context)


# ~~~~~~~~~~~~~~~~ Question & Variant-i eyni formda add testi ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# bu view sadece sual ve 1 varianti eyni anda elave edir, front-da bundan istifade olunmayib
@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def add_question_variant(request, id):
    quiz = Quiz.objects.get(id=id)
    if request.method == 'POST':
        question_form = QuestionForm(data=request.POST, prefix="question_form")
        variant_form = AnswerForm(data=request.POST, prefix="variant_form")
        print("METHOD POST")

        if question_form.is_valid() and variant_form.is_valid():
            print("FORM-lar valid")
            # before, save question
            question_instance = question_form.save(commit=False)
            question_instance.quiz = quiz
            if 'image' in request.FILES:
                question_instance.image = request.FILES['image']

            question_instance.save()
            question_form.save()
            print("Question saved")

            # save answer
            answer_instance = variant_form.save(commit=False)
            answer_instance.question = question_instance
            print("QUestion instance: ", question_instance)
            print("QUestion form: ", question_form)

            answer_instance.save()
            variant_form.save()
            print("Answer saved")

            context = {'quiz': quiz, 'a_form': AnswerForm(prefix="variant_form"),
                       'q_form': QuestionForm(prefix="question_form")}
            return render(request, 'main_page/dashboard/quiz_app/add_question_answer.html', context)
        else:
            print("Form-lar valid deyil")
            print("Question form errror \n", question_form.errors)
            print("Answer form error \n", variant_form.errors)

    print("Nothing yet")
    context = {'quiz': quiz, 'a_form': AnswerForm(prefix="variant_form"),
               'q_form': QuestionForm(prefix="question_form")}

    return render(request, 'main_page/dashboard/quiz_app/add_question_answer.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def add_question_variant_formset(request, id):
    quiz = Quiz.objects.get(id=id)
    quests = Question.objects.filter(quiz=quiz)

    question_variants = {}
    AnswerFormset = formset_factory(AnswerForm, extra=1)

    for q in quests:
        if q.get_answers():
            answers_list = []
            variants_list = []
            for answr in q.get_answers():
                answers_list.append(answr)
            variants_list = answers_list
            # print("Answers list: ", variants_list)
            question_variants[str(q)] = variants_list
    # print(question_variants)
    if request.method == 'POST':
        print(request.POST)
    if request.method == 'GET':
        answer_formset = AnswerFormset(request.GET or None)
        question_form = QuestionForm()
    elif request.method == 'POST':
        answer_formset = AnswerFormset(request.POST)
        question_form = QuestionForm(request.POST)
        if question_form.is_valid() and answer_formset.is_valid():
            # print("FORM-lar valid")
            # before, save question
            question_instance = question_form.save(commit=False)
            question_instance.quiz = quiz
            if 'image' in request.FILES:
                question_instance.image = request.FILES['image']

            question_instance.save()
            question_form.save()
            # print("Question saved")

            for form in answer_formset:
                if form['text'].value():
                    # save answer
                    answer_instance = form.save(commit=False)
                    answer_instance.question = question_instance
                    # print("QUestion instance: ", question_instance)
                    # print("QUestion form: ", question_form)

                    answer_instance.save()
                    # form.save()
                    # print("Answer saved:answer_instance ", answer_instance)

            questions = Question.objects.filter(quiz=quiz)

            # Yeni sual??n variantlar??n?? g??rm??k ??????n
            # ( Kod t??krar olur - ir??lisi ??????n optimalla??d??rar??q-
            # Funksiya ????klind?? yazma??a ??al????d??m i??l??m??di niy??s?? :))
            for q in questions:
                if q.get_answers():
                    answers_list = []
                    variants_list = []
                    for answr in q.get_answers():
                        answers_list.append(answr)
                    variants_list = answers_list
                    # print("Answers list: ", variants_list)
                    question_variants[str(q)] = variants_list
            messages.success(request, '"' + str(question_instance.text) + '"' + " sual?? ??lav?? edildi.")
            context = {'quiz': quiz,
                       'questions': questions,
                       'question_variants': question_variants,
                       'formset': AnswerFormset(),
                       'question_form': QuestionForm()
                       }
            return render(request, 'main_page/dashboard/quiz_app/add_answer_formset.html',
                          context)

    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'main_page/dashboard/quiz_app/add_answer_formset.html',
                  {'quiz': quiz,
                   'questions': questions,
                   'question_variants': question_variants,
                   'formset': answer_formset,
                   'question_form': question_form})


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def update_question_variant_formset(request, quiz_id, question_id):
    quiz = Quiz.objects.get(id=quiz_id)
    question = get_object_or_404(Question, id=question_id)
    quests = Question.objects.filter(quiz=quiz)

    # Suallar??n variantlar??n?? g??rm??k ??????n
    question_variants = {}
    for q in quests:
        if q.get_answers():
            answers_list = []
            variants_list = []
            for answr in q.get_answers():
                answers_list.append(answr)
            variants_list = answers_list
            question_variants[str(q)] = variants_list

    AnswerInlineformset = inlineformset_factory(Question, Answer, formset=CustomAnswerInlineFormset, fields=('text', 'correct',),
                                                can_delete=True, max_num=6, extra=0)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        formset = AnswerInlineformset(request.POST, instance=question)

        if question_form.is_valid() and formset.is_valid():
            # before, save question
            question_instance = question_form.save(commit=False)
            question_instance.quiz = quiz
            if 'image' in request.FILES:
                question_instance.image = request.FILES['image']

            question_instance.save()
            question_form.save()


            for form in formset:
                if form['text'].value():
                    # print("DELETED? ", form['DELETE'].value())
                    # save answer
                    answer_instance = form.save(commit=False)
                    if form['DELETE'].value():
                        answer_instance.delete()
                    else:
                        answer_instance.question = question_instance
                        answer_instance.save()
                        # form.save()
            # print("FORMSET HAS CHANGED ", formset.has_changed())
            messages.success(request, '"' + str(question.text) + '"' + " sual??n??n variant(lar)?? yenil??ndi.")
        else:
            print("Question Form Errorrs", question_form.errors)
            print("ANswer formset Errors ", formset.errors)
            print("Answer NON formset Errors ", formset.non_form_errors)
        questions = Question.objects.filter(quiz=quiz)
        return HttpResponseRedirect(
            reverse('addquestion', kwargs={
                'id': quiz_id})
        )

    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'main_page/dashboard/quiz_app/update_answer_formset.html',
                  {'update': True,
                   'quiz': quiz,
                   'questions': questions,
                   'question_variants': question_variants,
                   'formset': AnswerInlineformset(instance=question),
                   'question_form': QuestionForm(instance=question)
                   })


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def update_variant(request, q_id, v_id):
    question = Question.objects.get(id=int(q_id))
    variant = get_object_or_404(Answer, id=v_id)
    print("QUESTION Quiz ID: ", question.quiz.id)

    answer_form = AnswerForm(request.POST or None, instance=variant)

    if answer_form.is_valid():
        instance = answer_form.save(commit=False)
        instance.question = question

        instance.save()
        answer_form.save()

        messages.success(request, "Variantda d??yi??iklik edildi.")

        # variants = Answer.objects.filter(question=question)

        return HttpResponseRedirect(
            reverse('addvariants', kwargs={'id': instance.question.id})
        )
    else:
        print(answer_form.errors)

    variants = Answer.objects.filter(question=question)

    context = {'form': answer_form, 'question': question, 'variants': variants, 'update': True}
    return render(request, 'main_page/dashboard/quiz_app/add_variants.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def delete_variant(request, id):
    variant = Answer.objects.get(id=id)
    variant.delete()

    messages.warning(request, '"' + str(variant.text) + '"' + " variant?? silindi.")

    return HttpResponseRedirect(
        reverse('addvariants', kwargs={'id': variant.question.id})
    )


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def delete_question(request, id):
    question = Question.objects.get(id=id)
    question.delete()

    messages.warning(request, '"' + str(question.text) + '"' + " sual?? silindi.")

    return HttpResponseRedirect(
        reverse('addquestion', kwargs={'id': question.quiz.id})
    )


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def delete_quiz(request, id):
    quiz = Quiz.objects.get(id=id)
    quiz.delete()

    messages.warning(request, '"' + str(quiz.name) + '"' + " quiz-i silindi.")

    return HttpResponseRedirect(
        reverse('createquiz')
    )


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'student'])
def quiz_work(request):
    quizes = Quiz.objects.all()
    course = Course.objects.all()
    quizData = QuizData(request)

    current_user = request.user
    user_courses = []
    user_quizes = []

    for c in course:
        if c.students.all():
            for std in c.students.all():
                if str(current_user) == str(std.student.username):
                    user_courses.append(c.c_name)
    # print("Current user-in kurslari: ", user_courses)

    for q in quizes:
        if q.group.all():
            for user_grup in user_courses:
                for grup in q.group.all():
                    if str(user_grup) == str(grup):
                        if not (q in user_quizes):
                            user_quizes.append(q)
    # print(str(current_user) + " -un quiz-leri: ", user_quizes)

    user_old_quiz = quizData.get_results()

    context = {"quiz_name": quizes,
               "group": course,
               "user_quizes": user_quizes,
               "user_result": user_old_quiz
               }
    return render(request, 'main_page/dashboard/quiz_app/quiz_work.html', context)


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'student'])
def question_work(request, quiz_id):
    quiz = Quiz.objects.get(id=int(quiz_id))

    questions = []
    image_urls = []
    for q in quiz.get_questions():
        answers = []
        if q.image:
            image_urls.append({str(q): q.image.url})
        else:
            image_urls.append({str(q): 0})
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): [image_urls, answers]})
    # print("Suallar ve shekli: ", image_urls)
    return JsonResponse({
        "data": questions,
    })


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'student'])
def quiz_view(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    print("QUIZ ID", quiz_id)
    return render(request, 'main_page/dashboard/quiz_app/question_work.html', {'obj': quiz})


@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'student'])
def save_quiz_view(request, quiz_id):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        quiz = Quiz.objects.get(id=quiz_id)
        results = []
        correct_answer = None
        score = 0
        multiplier = round(100 / quiz.get_question_count(), 2)

        for q in questions:
            answer_selected = request.POST.get(q.text)
            print("Question", q.image)

            if answer_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if answer_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q): {'correct_answer': correct_answer, 'answered': answer_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = multiplier * score
        Result.objects.create(std_user=request.user, quiz=quiz, score=score_)

        return JsonResponse({'results': results, 'score': score_})


def lesson_materials(request):
    return render(request, 'main_page/dashboard/lesson_materials/topics_and_materials.html')

# Imtahan n??tic??l??rini PDF ????klind?? g??rm??k ??????n
@csrf_exempt
def view_pdf(request):
    if request.method == 'POST':
        form = StudentIDNumberForm(request.POST)
        if form.is_valid():
            all_files = os.listdir("media/pdf")
            ish_nomre = form.cleaned_data["id_number"]
            pdf = str(ish_nomre) + '.pdf'
            if pdf in all_files:
                filepath = os.path.join("media/pdf", pdf)
                return HttpResponse(open(filepath, 'rb'), content_type='application/pdf')
                # return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
            else:
                messages.error(request, "???? n??mr??sini d??zg??n daxil edin")
    else:
        form = StudentIDNumberForm()
    return render(request, 'main_page/view_pdf_result.html', {'form': form})


@xframe_options_sameorigin
def lesson_table(request):
    return render(request, 'main_page/LessonTable.html')

@xframe_options_sameorigin
def lesson_table_file(request):
    return render(request, 'main_page/hedef_cdvl.html')

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def search_student(request):
    query = request.GET.get('q')
    lookup = StudentProfile.objects.filter(Q(student__first_name__icontains=query) |
                                           Q(student__last_name__icontains=query) |
                                           Q(student__username__icontains=query)).order_by('-status')

    return render(request, 'main_page/dashboard/student_search.html',
                  context={'search_result': lookup

    })

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def search_teacher(request):
    query = request.GET.get('q')
    lookup = TeacherProfile.objects.filter(Q(user__first_name__icontains=query) |
                                           Q(user__last_name__icontains=query) |
                                           Q(user__username__icontains=query)).order_by('-status')

    return render(request, 'main_page/dashboard/teacher_search.html',
                  context={'search_result': lookup

    })

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def search_group(request):
    query = request.GET.get('q')
    lookup = Course.objects.filter(Q(c_id__icontains=query) |
                                           Q(c_name__icontains=query) |
                                           Q(c_description__icontains=query) |
                                           Q(teachers__user__first_name__icontains=query) |
                                           Q(teachers__user__last_name__icontains=query) |
                                           Q(students__student__first_name__icontains=query) |
                                           Q(students__student__last_name__icontains=query)
                                        ).order_by('-c_status')
    print("Lookup: ", set(lookup))
    return render(request, 'main_page/dashboard/group_search.html',
                  context={'search_result': set(lookup)

    })