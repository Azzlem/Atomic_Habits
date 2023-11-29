from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    """ Вывод списка пользователей """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Список пользователей")
    def get(self, request, *args, **kwargs):
        return super(UserList, self).get(request, *args, **kwargs)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Создание пользователя")
    def post(self, request, *args, **kwargs):
        return super(UserCreateView, self).create(request, *args, **kwargs)