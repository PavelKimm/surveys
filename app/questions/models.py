from django.contrib.auth import get_user_model
from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    started = models.DateField(auto_now_add=True)
    finished = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name[:30]


class Question(models.Model):
    FREE_TEXT = 0
    SINGLE_CHOICE = 1
    MULTIPLE_CHOICE = 2

    QUESTION_TYPE_CHOICES = (
        (FREE_TEXT, 'Text'),
        (SINGLE_CHOICE, 'Single Choice'),
        (MULTIPLE_CHOICE, 'Multiple Choice'),
    )

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=256)
    answer_type = models.PositiveSmallIntegerField(choices=QUESTION_TYPE_CHOICES, default=FREE_TEXT)

    def __str__(self):
        return self.question_text[:30]


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=256)

    def __str__(self):
        return self.answer_text[:30]


class TakenSurvey(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True,
                             related_name='taken_surveys')
    answers = models.ManyToManyField(QuestionAnswer)

    def __str__(self):
        return self.survey.name[:30]
