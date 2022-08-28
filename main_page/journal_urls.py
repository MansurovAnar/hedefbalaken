from django.conf.urls import url, include
from . import journal_views

urlpatterns = [
    url(r'journal_groups/$', journal_views.attendance_groups, name='journal_groups'),
    url(r'journal_page/$', journal_views.attendance_journal, name='attendance_journal'),
    url(r'^(?P<seller_name>[-\w]+)/$', journal_views.ticket_seller, name='ticket_seller'),
    url(r'^students/attendance/(?P<group_id>[-\w]+)/$', journal_views.check_student_attendance, name='checkstdattendance'),
    url(r'^student/attendances/(?P<group_id>[-\w]+)/$', journal_views.show_student_attendances_for_controller, name='showstdattendance'),
]