from rest_framework import serializers
from habits.models import Habits, Action, Place
from habits.validators import RewardValidator, TimeToCompleteValidator, PleasureHabitValidator, IsPleasureValidator, \
    PeriodicityValidator, patch_validator


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = "__all__"
        validators = [
            RewardValidator(fields_list=['pleasure_habit', 'reward']),
            TimeToCompleteValidator(field='execution_time'),
            PleasureHabitValidator(field='pleasure_habit'),
            IsPleasureValidator(field='is_pleasure'),
            PeriodicityValidator(field='periodicity')
        ]

    def update(self, instance, validated_data):
        """ Валидирует поля 'is_pleasure', 'reward' и 'pleasure_habit' при методе patch. """

        patch_validator(instance, validated_data)
        return super().update(instance, validated_data)


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"
