from django.conf.urls import include, url
from django.urls import path
from . import views

urlpatterns = [

    url(r'^$', views.index, name='mainpage'),
    url(r'^mainpage/$', views.index, name='mainpage'),  # inside dirnaqs:
    url(r'^register/$', views.register, name='register'),
    url(r'^about/$', views.about, name='about'),
    url(r'^whatsapp/$', views.whatsapp_redirect, name='whatsapp'),
    url(r'^courses/$', views.courses, name='courses'),
    url(r'^login/$', views.loginUser, name='login'),
    url('logout/', views.logoutUser, name='logout'),

    url(r'^password_reset/$', views.password_reset, name='pass_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='pass_reset_done'),

    url(r'^registeruser/$', views.registeruser, name='registeruser'),

    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^tables$', views.tables, name='tables'),
    url(r'^dashboard/courses$', views.courses_in_dashboard, name='dashboardcourses'),
    url(r'^notifications$', views.notifications, name='notifications'),

    url(r'^course/create$', views.create_course, name='createcourse'),

    url(r'^course/update/(?P<pk>[-\w]+)/$', views.update_course, name='updatecourse'),
    url(r'^course/detail/(?P<cid>[-\w]+)/$', views.course_detail, name='coursedetail'),
    url(r'^course/delete/(?P<pk>[-\w]+)/$', views.delete_course, name='deletecourse'),

    url(r'^teacher/create$', views.create_teacher, name='createteacher'),
    url(r'^teacher/detail/(?P<pk>[-\w]+)/$', views.teacher_detail, name='teacherdetail'),
    url(r'^profile$', views.my_profile, name='myprofile'),

    url(r'^student/create$', views.create_student, name='createstudent'),

    #~~~~~~~~~~~~~~~~~ Quiz teacher Side -----
    url(r'^quiz/add$', views.add_quiz, name='createquiz'),
    url(r'^question/add/(?P<id>[-\w]+)/$', views.add_question, name='addquestion'),
    url(r'^question/(?P<id>[-\w]+)/add/variant/$', views.add_variants, name='addvariants'),

    url(r'^quiz/update/(?P<quiz_id>[-\w]+)/$', views.update_quiz, name='updatequiz'),
    url(r'^question/update/(?P<quiz_id>[-\w]+)/(?P<question_id>[-\w]+)/$', views.update_question, name='updatequestion'),
    url(r'^variant/update/(?P<q_id>[-\w]+)/(?P<v_id>[-\w]+)/$', views.update_variant, name='updatevariant'),

    url(r'^variant/delete/(?P<id>[-\w]+)/$', views.delete_variant, name='deletevariant'),
    url(r'^question/delete/(?P<id>[-\w]+)/$', views.delete_question, name='deletequestion'),
    url(r'^quiz/delete/(?P<id>[-\w]+)/$', views.delete_quiz, name='deletequiz'),

    url(r'^quiz/work/$', views.quiz_work, name='quizwork'),
    url(r'^quiz/work/(?P<quiz_id>[-\w]+)/$', views.quiz_view, name='quizview'),
    url(r'^quiz/work/(?P<quiz_id>[-\w]+)/data/$', views.question_work, name='questionwork'),
    url(r'^quiz/work/(?P<quiz_id>[-\w]+)/save/$', views.save_quiz_view, name='savequizview'),

]
