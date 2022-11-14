from rest_framework import serializers
from authapp.serializers import UserModelSerializer
from .models import Project, Todo


# class ProjectModelSerializer(serializers.ModelSerializer):
class ProjectModelSerializer(serializers.HyperlinkedModelSerializer):
    # users = serializers.StringRelatedField(many=True)
    # M*M отобразится списком, для сериализации удобно,
    # но для CRUD нужно будет переопределять методы

    class Meta:
        model = Project
        fields = '__all__'


class TodoModelSerializer(serializers.ModelSerializer):
    by_user = UserModelSerializer()  # если бы не указали, был бы взят id модели User

    class Meta:
        model = Todo
        fields = ['name', 'content', 'publication_date', 'by_user', 'by_project', 'status']  # '__all__'
