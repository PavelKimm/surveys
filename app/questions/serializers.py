from rest_framework import serializers

from questions.models import Survey, Question, TakenSurvey, QuestionAnswer


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TakenSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenSurvey
        fields = '__all__'


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'
