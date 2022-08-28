from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .decorators import allowed_users
from main_page.models.payment_models import StdPaymentAmount2, StdPaidAmount
from main_page.payment_forms import StudentPaidAmountForm, StudentPaymentForm
from django.contrib import messages
from django.db.models import Q

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def student_payment_list(request):
    students_payment = StdPaymentAmount2.objects.all().order_by('-student__status')
    # for pay in students_payment:
    #     print("TEST: ", pay.paidamounts())
    students_paid = StdPaidAmount.objects.all()
    # print("Payments: ", students_payment)
    # print("Paids: ", students_paid)

    context = {"payments": students_payment, 'paids': students_paid}
    return render(request, 'main_page/dashboard/student_payment/student_payment_list.html',
                  context=context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def student_paid(request, payment_id):
    student_payment = get_object_or_404(StdPaymentAmount2, pk=payment_id)
    if request.method == 'POST':
        paidForm = StudentPaidAmountForm(data=request.POST)
        # print("Just FORM: ", paidForm)
        if paidForm.is_valid():
            form = paidForm.save(commit=False)
            form.paymnt = student_payment
            form.save()

            # print("Form VALID: ", paidForm)
            messages.success(request, '"' + "Ödəniş edildi.")

            return redirect('studentpaymentlist')
        else:
            print("Paid Form ERROR: ", paidForm.errors)
    else:
        paidForm = StudentPaidAmountForm()
        context = {'paidForm': paidForm, 'group': student_payment.group, 'student': student_payment.student}

        return render(request, 'main_page/dashboard/student_payment/student_paid_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def create_student_payment(request):
    if request.method == 'POST':
        payment_form = StudentPaymentForm(data=request.POST)
        print("FORM: ", payment_form)
        if payment_form.is_valid():
            payment_form.save()

            print("ALL RIGHT")
            return redirect('studentpaymentlist')
        else:
            print("[ERROR] ", payment_form.errors)
    else:
        payment_form = StudentPaymentForm()
        context = {'paymentForm': payment_form}
        return render(request, 'main_page/dashboard/student_payment/student_payment_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def update_student_payment(request, payment_id):
    context = {}
    payment = get_object_or_404(StdPaymentAmount2, id=payment_id)
    paymentForm = StudentPaymentForm(request.POST or None, instance=payment)

    if paymentForm.is_valid():
        paymentForm.save()
        messages.success(request, '"' + "Ödəniş yeniləndi.")

        return redirect('studentpaymentlist')

    context['paymentForm'] = paymentForm
    return render(request, 'main_page/dashboard/student_payment/student_payment_form.html', context)

@csrf_protect
@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def search_student_in_payment_list(request):
    query = request.GET.get('q')
    lookup = StdPaymentAmount2.objects.filter(Q(group__c_name__contains=query) |
                                           Q(student__student__first_name__contains=query) |
                                           Q(student__student__last_name__contains=query) |
                                           Q(student__student__username__contains=query)).order_by('-startDate')
    print("LOOKUP FIND: ", lookup)
    return render(request, 'main_page/dashboard/student_payment/student_search_in_payment_list.html',
                  context={'search_result': lookup

    })