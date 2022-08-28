from typing import List, Any

from django.core.exceptions import RequestAborted
from django.shortcuts import get_object_or_404

from .models import *


# Get Quiz data for student
class QuizData:
    def __init__(self, request):
        self.user_result = []
        self.user_request = request
        self.results = Result.objects.all().order_by('-quiz_work_date')

    def get_results(self):
        for result in self.results:
            if str(self.user_request.user) == str(result.std_user):
                self.user_result.append(result)
        return self.user_result


class QuizDataForTeacher:
    def __init__(self, request):
        self.tcr_request = request
        self.user_result_for_tcr = []
        self.teacher_students = []
        self.teacher_courses = []
        self.user_groups = request.user.groups.all()
        self.students = StudentProfile.objects.all()
        self.std_results = Result.objects.all().order_by('-quiz_work_date')

    def get_results_for_teacher(self):
        try:
            for rol in self.user_groups:
                if rol.name == "teacher":
                    teacher = get_object_or_404(TeacherProfile, user=self.tcr_request.user)
                    print("Teacher: ", teacher)
                    if teacher.courses.all():
                        print("Teacher's courses: ", teacher.courses.all())
                        for crs in teacher.courses.all():
                            if self.students:
                                for std in self.students:
                                    print("Student: ", std)
                                    if std.coursess.filter(c_name=crs):
                                        print("STudent's courses: ", std.coursess.filter(c_name=crs))
                                        for result in self.std_results:
                                            print("Result: ", result)
                                            print("result.std_user: ", result.std_user)
                                            print("std: ", std)
                                            if result.std_user == std:
                                                print("result.std_user: ", result.std_user)
                                                self.user_result_for_tcr.append(result.score)
                                        print("Queries.py-da: ", self.user_result_for_tcr)
            return self.user_result_for_tcr

        except RequestAborted:
            # log_info function will be called here
            pass
