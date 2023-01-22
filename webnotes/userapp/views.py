from rest_framework import generics
from authapp.models import User
from authapp.serializers import UserModelSerializer, UserSerializerStaffInfo
from .serializers import UserSerializer, UserSerializerWithFullName


class UserListAPIViewGen(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.version == '0.2':
            return UserSerializerWithFullName
        return UserSerializer

