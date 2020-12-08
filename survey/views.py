from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from .serializers import *
from .models import *


class CheckAdminPermission(permissions.AllowAny):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.is_staff


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all().order_by('-date_start')
    serializer_class = SurveySerializer
    pagination_class = None
    permission_classes = (CheckAdminPermission,)

    @swagger_auto_schema(
        operation_summary="Пройти опрос",
        methods=["POST"],
        request_body=SurveyCompleteSerializer,
        responses={201: SurveySerializer}
    )
    @action(detail=True, methods=["POST"])
    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        context = self.get_serializer_context()
        serializer = SurveyCompleteSerializer(instance=instance, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.data)
        print(SurveySerializer(instance, context=context).data)
        return Response(SurveySerializer(instance, context=context).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Получить список всех ответов пользователя",
        methods=["GET",],
        query_serializer=CompletedSurveysSerializer,
        responses={200: CompletedSurveysSerializer(many=True)}
    )
    @action(detail=False, methods=["GET"])
    def completed(self, request, *args, **kwargs):
        if request.query_params.get('user_id') is None:
            raise serializers.ValidationError('Must provide user_id in GET parameters')

        queryset = self.filter_queryset(self.get_queryset())
        context = self.get_serializer_context()
        serializer = CompletedSurveysSerializer(data=request.query_params, instance=queryset, context=context, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)




