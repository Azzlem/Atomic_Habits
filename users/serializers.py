from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['username', 'pk', 'email', 'last_name', 'first_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        obj = super().create(validated_data)
        obj.set_password(validated_data['password'])
        obj.save()
        return obj

    def update(self, instance, validated_data):
        """Обновляет пользователя входящими данными и устанавливает ему пароль"""

        obj = super().update(instance, validated_data)
        if validated_data.get('password'):
            obj.set_password(validated_data['password'])
        obj.save()
        return obj
