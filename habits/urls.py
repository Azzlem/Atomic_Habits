from django.urls import path

from habits.apps import HabitsConfig
from rest_framework.routers import DefaultRouter
from habits.views import  ActionViewSet, PlaceViewSet, HabitListAPIView, HabitPublicListAPIView, \
    HabitCreateAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'action', ActionViewSet, basename='action')
router.register(r'place', PlaceViewSet, basename='place')

urlpatterns = [
                  path('habits/', HabitListAPIView.as_view(), name='habits_list'),
                  path('habits/public/', HabitPublicListAPIView.as_view(), name='habit_public_list'),
                  path('habit/create/', HabitCreateAPIView.as_view(), name='habits_list'),
                  path('habit/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit'),
                  path('habit/update/<int:pk>', HabitUpdateAPIView.as_view(), name='habit_update'),
                  path('habit/delete/<int:pk>', HabitDestroyAPIView.as_view(), name='habit_delete'),
              ] + router.urls
