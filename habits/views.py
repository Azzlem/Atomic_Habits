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

    def perform_create(self, serializer, **kwargs):
        """
        Сохраняет авторизованного пользователя в объекте привычки,
        создает периодическую задачу если привычка не является приятной.
        """

        new_habit = serializer.save()
        new_habit.user = self.request.user
        new_habit.save()

        make_task(new_habit)


class HabitListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = HabitsSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        """ Получает только привычки владельца. """

        queryset = Habits.objects.filter(user=self.request.user)
        return queryset


class HabitPublicListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Habits.objects.filter(is_public=True)
    serializer_class = HabitsSerializer
    pagination_class = HabitPaginator


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrStaff,)
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer


class HabitUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrStaff,)
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer

    def perform_update(self, serializer):
        """ Удаляет и создает периодическую задачу с новыми данными. """

        habit = serializer.save()
        delete_task(habit_pk=habit.pk)
        make_task(habit)


class HabitDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrStaff,)
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer

    def perform_destroy(self, instance):
        """ Удаляет периодическую задачу. """

        delete_task(habit_pk=instance.pk)
        super().perform_destroy(instance)
