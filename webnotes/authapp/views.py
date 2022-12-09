from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserModelSerializer
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.http import Http404
from todoapp.models import Project


# class UserModelViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserModelSerializer

# Cannot apply DjangoModelPermissionsOrAnonReadOnly on a view that
# does not set `.queryset` or have a `.get_queryset()` method
class UserListApiView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    """
    only get
    http_method_names = ["get","post","put","patch","delete","head","options","trace"]
    """

    def get_queryset(self):
        """
        + filter users by project id
        """
        project = self.request.query_params.get('project')
        users = User.objects.all()
        if project:
            users = users.filter(project=project)  # !
        return users

    def get(self, request):  # называем как метод http-запроса
        # users = User.objects.all()
        users = self.get_queryset()
        serializer = UserModelSerializer(users, many=True)
        return Response(serializer.data)

    # def post(self, request):  # а создавать нельзя по условию
    #     serializer = UserModelSerializer(User, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailApiView(APIView):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    """
    retrieve, update, partial_update.
    http_method_names = ["get","post","put","patch","delete","head","options","trace"]
    """

    def get_queryset(self):  # добавила get_queryset чтобы работала DjangoModelPermissionsOrAnonReadOnly
        return User.objects.all()

    def get_object(self, pk):
        """get_object_or_404 for class"""
        try:
            return self.get_queryset().get(pk=pk)
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):  # удалять нельзя по условию
    #     user = self.get_object(pk)
    #     data = {'is_active': 0}
    #     serializer = UserModelSerializer(User, data=data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

