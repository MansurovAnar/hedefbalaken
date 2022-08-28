from django.conf.urls import url, include
from . import payment_views

urlpatterns = [
    url(r'students/payment/list$', payment_views.student_payment_list, name='studentpaymentlist'),
    url(r'student/paid/(?P<payment_id>[-\w]+)/$$', payment_views.student_paid, name='addstudentpaidamount'),
    url(r'create/student/payment$', payment_views.create_student_payment, name='createstudentpayment'),
    url(r'update/student/payment/(?P<payment_id>[-\w]+)/$$', payment_views.update_student_payment, name='updatestudentpayment'),
    url(r'search/student/in-payment/list$', payment_views.search_student_in_payment_list, name='searchstudentinpaymentlist'),
]