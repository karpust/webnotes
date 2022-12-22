from rest_framework import generics
from authapp.models import User
from authapp.serializers import UserModelSerializer, UserSerializerStaffInfo
from todoapp.models import Todo
from todoapp.serializers import TodoModelSerializer


class UserListAPIViewGen(generics.ListAPIView):
    queryset = User.objects.all()
    # serializer_class = UserSerializerStaffInfo

    def get_serializer_class(self):
        if self.request.version == '2.0':
            return UserSerializerStaffInfo  # + is_superuser, is_staff
        return UserModelSerializer


# class TodoListAPIViewGen(generics.ListAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer

