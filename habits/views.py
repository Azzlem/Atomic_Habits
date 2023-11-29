from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from habits.models import Habits
from habits.serializers import HabitsSerializer


class HabitsViewSet(viewsets.ModelViewSet):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer, send_message_create=None):
        """ Сохраняет авторизованного пользователя в привычку """
        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()

    @swagger_auto_schema(operation_summary="Удаление привычки")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)