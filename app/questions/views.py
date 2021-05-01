from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.views import APIView

from questions.models import Survey, Question, TakenSurvey, QuestionAnswer
from questions.serializers import SurveySerializer, QuestionListSerializer, TakenSurveySerializer, \
    QuestionAnswerSerializer, QuestionDetailSerializer, QuestionAnswerDetailSerializer


class SurveyListView(generics.ListCreateAPIView):
    serializer_class = SurveySerializer

    def get_queryset(self):
        queryset = Survey.objects.all()

        filter_ = self.request.query_params.get('filter')
        if filter_ == 'actual':
            queryset = Survey.objects.exclude(finished__lte=timezone.now())
        elif filter_ == 'finished':
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
    serializer_class = QuestionListSerializer

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
    serializer_class = QuestionDetailSerializer
    queryset = Question.objects.all()

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Use PATCH instead"}, status=HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=HTTP_403_FORBIDDEN)
        answer_type = request.data.get('answer_type')
        obj = Question.objects.filter(pk=kwargs['pk']).first()
        if answer_type and obj and obj.answers.count() and obj.answer_type != answer_type:
            return Response({"detail": "This question already has answers, you can't change its answer_type"},
                            status=HTTP_400_BAD_REQUEST)
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
    serializer_class = QuestionAnswerDetailSerializer
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
        anonymously = request.data.get('anonymously')
        if not survey_id:
            return Response({"detail": "survey_id wasn't provided"}, status=HTTP_400_BAD_REQUEST)
        survey = Survey.objects.filter(pk=survey_id).exclude(finished__lte=timezone.now()).first()
        if not survey:
            return Response({"detail": "Actual survey wasn't found"}, status=HTTP_404_NOT_FOUND)
        if not anonymously:
            anonymously = False
        taken_survey = TakenSurvey.objects.create(user=user, survey=survey, anonymously=anonymously)
        return Response(self.serializer_class(taken_survey).data, status=HTTP_201_CREATED)


class TakenSurveyListAdminView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = TakenSurveySerializer

    def get_queryset(self):
        queryset = TakenSurvey.objects.all()
        user_id = self.request.query_params.get('user-id')
        survey_id = self.request.query_params.get('survey-id')
        if user_id:
            queryset = queryset.filter(user_id=user_id, anonymously=False)
        if survey_id:
            queryset = queryset.filter(survey_id=survey_id)
        return queryset


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

        try:
            taken_survey = TakenSurvey.objects.get(pk=taken_survey_id, user=user)
            question = Question.objects.get(pk=question_id, survey=taken_survey.survey)
        except TakenSurvey.DoesNotExist:
            return Response({"detail": "Taken survey wasn't found"}, status=HTTP_404_NOT_FOUND)
        except Question.DoesNotExist:
            return Response({"detail": "Question wasn't found"}, status=HTTP_404_NOT_FOUND)

        if question.answer_type == Question.FREE_TEXT:
            question_answer = QuestionAnswer.objects.create(question=question, answer_text=question_answer)
            taken_survey.answers.add(question_answer)

        elif question.answer_type == Question.SINGLE_CHOICE:
            try:
                question_answer = QuestionAnswer.objects.get(pk=question_answer, question=question)
            except QuestionAnswer.DoesNotExist:
                return Response({"detail": "Question answer wasn't found"}, status=HTTP_404_NOT_FOUND)
            taken_survey.answers.add(question_answer)

        elif question.answer_type == Question.MULTIPLE_CHOICE:
            for answer in question_answer:
                try:
                    question_answer = QuestionAnswer.objects.get(pk=answer, question=question)
                except QuestionAnswer.DoesNotExist:
                    return Response({"detail": "Question answer wasn't found"}, status=HTTP_404_NOT_FOUND)
                taken_survey.answers.add(question_answer)

        return Response({"message": "ok"}, status=HTTP_200_OK)
