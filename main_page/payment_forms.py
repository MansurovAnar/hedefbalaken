from main_page.models.payment_models import StdPaymentAmount2, StdPaidAmount
from main_page.models.all_models import Course, StudentProfile
from django import forms
import datetime

this_year = datetime.date.today().year
YEARS = [x for x in range(2022, this_year + 1)]

class StudentPaidAmountForm(forms.ModelForm):
    # paymnt = forms.ModelChoiceField(queryset=StdPaymentAmount2.objects.all())
    paidAmount = forms.IntegerField(required=True)
    paidDate = forms.DateField(required=True,
                                widget=forms.SelectDateWidget(years=YEARS,
                                                              attrs={
                                                                  'class': 'form-control-lg col-md-1.5'
                                                              }
                                                              )
                                )
    class Meta:
        model = StdPaidAmount
        fields = ('paidAmount', 'paidDate')

class StudentPaymentForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Course.objects.all())
    student = forms.ModelChoiceField(queryset=StudentProfile.objects.all())
    monthlyAmount = forms.IntegerField(required=True)
    startDate = forms.DateField(required=True,
                                widget=forms.SelectDateWidget(years=YEARS,
                                                              attrs={
                                                                  'class': 'form-control-lg col-md-1.5'
                                                              }
                                                              )
                                )
    class Meta:
        model = StdPaymentAmount2
        fields = ('group', 'student', 'monthlyAmount', 'startDate')