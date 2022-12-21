import graphene
from graphene_django import DjangoObjectType
from todoapp.models import Todo, Project
from authapp.models import User


# создание типов данных на основе модели:
class TodoType(DjangoObjectType):

    class Meta:
        model = Todo  # DjangoObjectType автоматом создаст нужные типы полей для указанной модели
        fields = '__all__'


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class Query(graphene.ObjectType):
    all_todos = graphene.List(TodoType)

    def resolve_all_todos(root, info):  # self
        return Todo.objects.all()


schema = graphene.Schema(query=Query)  # создали схему данных

# GraphQL-запрос: {allTodos {name, id, byUser{username}, byProject{name}}}
# all from snake_case to CamelCase!
# на http://127.0.0.1:8000/graphql/
