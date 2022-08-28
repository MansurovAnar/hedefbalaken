from django.contrib import admin
from main_page.models.all_models import (user, Course, TeacherProfile, StudentProfile,
                                 Quiz, Question, Answer, Result,
                                 FrontPageData, TeamMember, FrontMenuNames)
from main_page.models.journal_models import TeacherAttendance, StAttendance
from main_page.models.ticket_models import TicketSeller
from main_page.models.payment_models import StdPaymentAmount2, StdPaidAmount

# Register your models here.

class AnswerInLine(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]

admin.site.register(Course)
admin.site.register(user)
# admin.site.register(team_member)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(FrontPageData)
admin.site.register(TeamMember)
admin.site.register(FrontMenuNames)
admin.site.register(StAttendance)
admin.site.register(TeacherAttendance)
admin.site.register(TicketSeller)
admin.site.register(StdPaymentAmount2)
admin.site.register(StdPaidAmount)