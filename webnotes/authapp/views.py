from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserModelSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.http import Http404


# class UserModelViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer


class UserListApiView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    """
    only get
    http_method_names = ["get","post","put","patch","delete","head","options","trace"]
    """

    @staticmethod
    def get(request):  # называем как метод http-запроса
        users = User.objects.all()
        serializer = UserModelSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailApiView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    """
    retrieve, update, partial_update.
    http_method_names = ["get","post","put","patch","delete","head","options","trace"]
    """
    @staticmethod
    def get_object(pk):
        """get_object_or_404 for class"""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):  # называем как метод http-запроса
        user = self.get_object(pk)
        serializer = UserModelSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):  # Media type: application/json
        user = self.get_object(pk)
        serializer = UserModelSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserModelSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

