from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from main_page.models.all_models import TeacherProfile, StudentProfile, Course

class StdPaymentAmount2(models.Model):
    group = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='student_payment_amount')
    monthlyAmount = models.FloatField(blank=True)
    startDate = models.DateField(auto_now=False)

    def __str__(self):
        payment_info = str(self.student) + ": " + str(self.group) + "-" + \
                       str(self.startDate) + " " + str(self.monthlyAmount) + "AZN"
        return payment_info
    def paidamounts(self):
        return self.stdpaidamount_set.all()
    class Meta:
        app_label = "main_page"

class StdPaidAmount(models.Model):
    paymnt = models.ForeignKey(StdPaymentAmount2, on_delete=models.CASCADE, null=True)
    paidAmount = models.FloatField(blank=True)
    paidDate = models.DateField()

    def __str__(self):
        paid_amount = str(self.paidAmount) + "AZN" + "-" + str(self.paidDate)
        return paid_amount

    class Meta:
        app_label = "main_page"