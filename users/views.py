from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(operation_summary="создание пользователя")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


















# class UserList(generics.ListCreateAPIView):
#     """ Вывод списка пользователей """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     @swagger_auto_schema(operation_summary="Список пользователей")
#     def get(self, request, *args, **kwargs):
#         return super(UserList, self).get(request, *args, **kwargs)
#
#
# class UserCreateView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#
#     @swagger_auto_schema(operation_summary="Создание пользователя")
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
