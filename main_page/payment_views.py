from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.http import FileResponse
from django.core.files import File

from .decorators import allowed_users
from main_page.models.payment_models import StdPaymentAmount2, StdPaidAmount
from main_page.payment_forms import StudentPaidAmountForm, StudentPaymentForm
from django.contrib import messages
from django.db.models import Q
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

@login_required(login_url='login')
@allowed_users(allowed_roles=['controller'])
def student_payment_list(request):
    students_payment = StdPaymentAmount2.objects.all().order_by('-status', '-student__status', '-group__c_status')
    # for pay in students_payment:
    #     print("TEST: ", pay.paidamounts())
    students_paid = StdPaidAmount.objects.all()
    # print("Payments: ", students_payment)
    # print("Paids: ", students_paid)

    context = {"payments": students_payment, 'paids': students_paid}
    return render(request, 'main_page/dashboard/student_payment/student_payment_list.html',
                  context=context)

def fill_qaime(form):
    day = form.paidDate.strftime("%d")
    month = form.paidDate.strftime("%B")
    student_fullname = str(form.paymnt.student.student.first_name) + " " + str(form.paymnt.student.student.last_name)
    group_id = form.paymnt.group.c_id
    group_name = form.paymnt.group.c_name
    amount = str(form.paidAmount)
    write_source = r"{}"

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # 1ci qaime uchun melumatlar
    can.drawString(205, 695, day)
    can.drawString(270, 695, month)
    can.drawString(230, 665, student_fullname)
    can.drawString(115, 525, group_id)
    can.drawString(195, 525, group_name)
    can.drawString(340, 525, amount)

    # 2ci qaime uchun melumatlar
    can.drawString(205, 320, day)
    can.drawString(270, 320, month)
    can.drawString(230, 290, student_fullname)
    can.drawString(115, 150, group_id)
    can.drawString(195, 150, group_name)
    can.drawString(340, 150, amount)
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(r"media/pdf/qaime.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # finally, write "output" to a real file
    pdf_name = str(form.paymnt.student.student.username) + "_" + group_id + "_" + str(form.paidDate)
    outputStream = open(write_source.format("%s.pdf" % pdf_name), "wb")

    output.write(outputStream)
    outputStream.close()

    qaime_pdf = open(write_source.format("%s.pdf" % pdf_name), 'rb')
    qaime_file = File(qaime_pdf)
    form.qaime = qaime_file

    form.save()
    qaime_pdf.close()
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
            fill_qaime(form=form)

            messages.success(request, '"' + "Ödəniş edildi.")

            # source_of_file = write_source.format("%s.pdf" % pdf_name)
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
        # print("FORM: ", payment_form)
        if payment_form.is_valid():
            payment_form.save()

            # print("ALL RIGHT")
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
    lookup = StdPaymentAmount2.objects.filter(Q(group__c_name__icontains=query) |
                                           Q(student__student__first_name__icontains=query) |
                                           Q(student__student__last_name__icontains=query) |
                                           Q(student__student__username__icontains=query)).order_by('-status', '-student__status', '-group__c_status')
    print("LOOKUP FIND: ", lookup)
    return render(request, 'main_page/dashboard/student_payment/student_search_in_payment_list.html',
                  context={'search_result': lookup

    })