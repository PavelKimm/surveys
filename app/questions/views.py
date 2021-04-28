from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from questions.models import Survey, Question, TakenSurvey, QuestionAnswer
from questions.serializers import SurveySerializer, QuestionSerializer, TakenSurveySerializer, QuestionAnswerSerializer


class SurveyListView(generics.ListCreateAPIView):
    serializer_class = SurveySerializer

    def get_queryset(self):
        queryset = Survey.objects.exclude(finished__lte=timezone.now())

        filter_ = self.request.query_params.get('filter')
        if filter_ == 'finished':
            queryset = Survey.objects.filter(finished__lte=timezone.now())
        return queryset

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)


class SurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)


class QuestionListView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        survey_id = self.request.query_params.get('survey-id')
        if survey_id:
            queryset = queryset.filter(survey_id=survey_id)
        return queryset

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)


class QuestionAnswerListView(generics.ListCreateAPIView):
    serializer_class = QuestionAnswerSerializer

    def get_queryset(self):
        queryset = QuestionAnswer.objects.all()
        question_id = self.request.query_params.get('question-id')
        if question_id:
            queryset = queryset.filter(question_id=question_id)
        return queryset

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            print(request.user)
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.create(request, *args, **kwargs)


class QuestionAnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionAnswerSerializer
    queryset = QuestionAnswer.objects.all()

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)


class TakenSurveyListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TakenSurveySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = TakenSurvey.objects.filter(user=user)
        survey_id = self.request.query_params.get('survey-id')
        if survey_id:
            queryset = queryset.filter(survey_id=survey_id)
        return queryset

    def post(self, request, *args, **kwargs):
        user = request.user
        survey_id = request.data.get('survey_id')
        if not survey_id:
            return Response({"detail": "survey_id wasn't provided"}, status=HTTP_400_BAD_REQUEST)
        taken_survey = TakenSurvey.objects.create(user=user, survey_id=survey_id)
        return Response(self.serializer_class(taken_survey).data, status=HTTP_201_CREATED)


class TakenSurveyDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TakenSurveySerializer
    queryset = Question.objects.all()


class AnswerQuestionView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        taken_survey_id = request.data.get('taken_survey_id')
        question_id = request.data.get('question_id')
        question_answer = request.data.get('question_answer')

        if not taken_survey_id:
            return Response({"detail": "taken_survey_id wasn't provided"}, status=HTTP_400_BAD_REQUEST)
        if not question_id:
            return Response({"detail": "question_id wasn't provided"}, status=HTTP_400_BAD_REQUEST)
        if not question_answer:
            return Response({"detail": "question_answer wasn't provided"}, status=HTTP_400_BAD_REQUEST)

        taken_survey = TakenSurvey.objects.get(pk=taken_survey_id)
        question = Question.objects.get(pk=question_id)
        if question.answer_type == Question.FREE_TEXT:
            question_answer = QuestionAnswer.objects.create(question=question, answer_text=question_answer)
            taken_survey.answers.add(question_answer)

        elif question.answer_type == Question.SINGLE_CHOICE:
            question_answer = QuestionAnswer.objects.get(pk=question_answer)
            taken_survey.answers.add(question_answer)

        elif question.answer_type == Question.MULTIPLE_CHOICE:
            for answer in question_answer:
                question_answer = QuestionAnswer.objects.get(pk=answer)
                taken_survey.answers.add(question_answer)

        return Response({"message": "ok"}, status=HTTP_200_OK)
