from django.contrib import admin
from .models import (user, Course,
                     TeacherProfile, StudentProfile,
                     Quiz, Question, Answer, Result,
                     FrontPageData, TeamMember, FrontMenuNames)

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
