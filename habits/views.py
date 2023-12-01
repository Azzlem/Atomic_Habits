from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from habits.models import Habits, Action, Place
from habits.paginator import HabitPaginator, PlacePaginator, ActionPaginator
from habits.permissions import IsOwnerOrStaff
from habits.serializers import HabitsSerializer, ActionSerializer, PlaceSerializer
from habits.services import make_task, delete_task


class PlaceViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = PlacePaginator


class ActionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    pagination_class = ActionPaginator


class HabitCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitsSerializer

    @swagger_auto_schema(operation_summary="Создание привычки")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer, **kwargs):
        """
        Сохраняет авторизованного пользователя в привычку, создает периодическую задачу.
        """

        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()

        make_task(new_habit)


class HabitListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitsSerializer
    pagination_class = HabitPaginator

    @swagger_auto_schema(operation_summary="Список привычек")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """ Получает привычки юзера. """

        queryset = Habits.objects.filter(user=self.request.user)
        return queryset


class HabitPublicListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Habits.objects.filter(is_public=True)
    serializer_class = HabitsSerializer
    pagination_class = HabitPaginator

    @swagger_auto_schema(operation_summary="Список публичных привычек")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrStaff,)
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer

    @swagger_auto_schema(operation_summary="Выбранная привычка")
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class HabitUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrStaff,)
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer

    @swagger_auto_schema(operation_summary="Изменение привычки")
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Изменение привычки")
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        """ Удаляет и создает периодическую задачу с новыми данными. """

        habit = serializer.save()
        delete_task(habit_pk=habit.pk)
        make_task(habit)


class HabitDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrStaff,)
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer

    @swagger_auto_schema(operation_summary="Удаление привычки")
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """ Удаляет периодическую задачу. """

        delete_task(habit_pk=instance.pk)
        super().perform_destroy(instance)
