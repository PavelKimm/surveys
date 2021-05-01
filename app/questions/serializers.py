from rest_framework import serializers

from questions.models import Survey, Question, TakenSurvey, QuestionAnswer


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class QuestionListSerializer(serializers.ModelSerializer):
    answer_type = ChoiceField(Question.QUESTION_TYPE_CHOICES)

    class Meta:
        model = Question
        fields = '__all__'


class QuestionDetailSerializer(QuestionListSerializer):
    answers = serializers.SerializerMethodField()
    survey = serializers.IntegerField(source='survey.id', read_only=True)

    @staticmethod
    def get_answers(obj):
        answers = [{
            'id': answer.id,
            'answer_text': answer.answer_text
        } for answer in obj.answers.all()]
        return answers


class TakenSurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = TakenSurvey
        exclude = ('answers',)

    @staticmethod
    def get_user(obj):
        if obj.anonymously:
            return None
        else:
            return obj.user.id

    @staticmethod
    def get_questions(obj):
        questions = obj.answers.all().values_list('question', flat=True).distinct()
        if not questions:
            return None

        question_answers = {}
        for question_answer in obj.answers.all():
            if question_answers.get(question_answer.question.id):
                question_answers[question_answer.question.id].append(question_answer.id)
            else:
                question_answers[question_answer.question.id] = [question_answer.id]

        result = [{
            'id': question_id,
            'question_text': Question.objects.get(pk=question_id).question_text,
            'answers': [{
                'id': answer_id,
                'answer_text': QuestionAnswer.objects.get(pk=answer_id).answer_text
            } for answer_id in answers]
        } for question_id, answers in question_answers.items()]
        return result


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class QuestionAnswerDetailSerializer(QuestionAnswerSerializer):
    question = serializers.IntegerField(source='question.id', read_only=True)
