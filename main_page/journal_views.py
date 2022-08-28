from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_protect

from .decorators import allowed_users
from main_page.models.all_models import TeacherProfile, Course
from main_page.models.journal_models import StAttendance
from .forms import StudentAttendanceForm
from .models.ticket_models import TicketSeller
from django.forms import formset_factory
import datetime

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def attendance_groups(request):
    current_user = request.user
    user_groups = current_user.groups.all()

    for rol in user_groups:
        if rol.name == "teacher":
            teacher = TeacherProfile.objects.filter(user=current_user)

            context = {'teacher': teacher[0]}
            return render(request, 'main_page/dashboard/attendance_management/JournalGroupsForTeacher.html',
                          context=context)
        elif rol.name == "controller":
            course_groups = Course.objects.all()

            context = {'groups': course_groups}
            return render(request, 'main_page/dashboard/attendance_management/JournalGroupsForController.html',
                          context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def show_student_attendances_for_controller(request, group_id):
    group = get_object_or_404(Course, c_id=group_id)
    group_students = group.students.all()
    group_teacher = group.teachers.all()

    students = {}
    group_dates = []
    qaibs = {}
    flag = 0

    for std in group_students:
        sum_of_unattendances = 0
        student_attendances = StAttendance.objects.filter(student=std)
        print(student_attendances)
        for student in student_attendances:
            sum_of_unattendances += student.get_unattendance_count()
            if not flag:
                group_dates.append(student.attendance_date)
        qaibs[str(std.student.first_name) + ' ' + str(std.student.last_name)] = sum_of_unattendances

        flag = 1
        # Dictionary-i key unique olmaya bilər aşağıdakı şəkildə qalarsa. İrəli üçün optimallaşdırmaq lazım
        students[str(std.student.first_name) + ' ' + str(std.student.last_name)] = student_attendances
    print(qaibs)
    context = {'group': group, 'students': students,
               'teacher': group_teacher,
               'group_dates': group_dates,
               'qaibs': qaibs}
    return render(request, 'main_page/dashboard/attendance_management/studentAttendanceListForController.html',
                  context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller', 'teacher'])
def check_student_attendance(request, group_id):
    group = get_object_or_404(Course, c_id=group_id)
    group_students = group.students.all()
    student_count = group_students.count()

    formset = formset_factory(StudentAttendanceForm, extra=student_count)

    if request.method == "GET":
        attendance_form = formset(request.GET or None)
    elif request.method == "POST":
        attendance_form = formset(request.POST)
        # attendance_form.student = group_students
        print("OKAY1")
        if attendance_form.is_valid():
            print("OKAY2")
            for count, form in enumerate(attendance_form):
                print("OKAY3")
                attendance_instance = form.save(commit=False)
                attendance_instance.student = group_students[count]
                attendance_instance.save()

            return HttpResponseRedirect(
                reverse('journal_groups')
            )
        else:
            print("Attendance formset Errors ", formset.__dict__)
            print("Attendance  NON formset Errors ", formset.non_form_errors.__dict__)


    # formsett = zip(attendance_form, group_students)
    context = {'formset': attendance_form, 'students': group_students,
               'group': group, 'current_date': datetime.date.today()}
    return render(request, 'main_page/dashboard/attendance_management/studentAttendance.html', context=context)



def attendance_journal(request):
    return render(request, 'main_page/dashboard/attendance_management/AttendanceJournal.html')


def ticket_seller(request, seller_name):
    if request.method == 'GET':
        seller = TicketSeller.objects.get(pk=seller_name)
        form_url = seller.gform_url

    return HttpResponseRedirect(form_url)

