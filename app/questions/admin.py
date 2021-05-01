from django.contrib import admin

from questions.models import Survey, Question, QuestionAnswer, TakenSurvey


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'started')
    list_display = ('__str__', 'description', 'started', 'finished')
    fields = ('id', 'name', 'description', 'started', 'finished')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('__str__', 'survey', 'answer_type')
    fields = ('id', 'survey', 'question_text', 'answer_type')


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('__str__', 'question')
    fields = ('id', 'question', 'answer_text')


@admin.register(TakenSurvey)
class TakenSurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('__str__', 'user', 'anonymously')
    fields = ('id', 'survey', 'user', 'anonymously')
