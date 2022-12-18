from rest_framework import generics
from authapp.models import User
from .serializers import UserSerializer, UserSerializerWithFullName


class UserListAPIViewGen(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.version == '0.2':
            return UserSerializerWithFullName
        return UserSerializer

