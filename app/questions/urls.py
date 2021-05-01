from django.urls import path

from questions.views import (
    SurveyListView, SurveyDetailView, QuestionListView, QuestionDetailView, TakenSurveyListView, AnswerQuestionView,
    QuestionAnswerListView, QuestionAnswerDetailView, TakenSurveyListAdminView
)

urlpatterns = [
    path('surveys/', SurveyListView.as_view(), name='survey-list'),
    path('surveys/<int:pk>/', SurveyDetailView.as_view(), name='survey-detail'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('question-answers/', QuestionAnswerListView.as_view(), name='question-answers-list'),
    path('question-answers/<int:pk>/', QuestionAnswerDetailView.as_view(), name='question-answers-detail'),
    path('taken-surveys/', TakenSurveyListView.as_view(), name='taken-survey-list'),
    path('taken-surveys-admin/', TakenSurveyListAdminView.as_view(), name='taken-survey-admin-list'),
    path('taken-surveys/answer-question/', AnswerQuestionView.as_view(), name='answer-question'),
]
