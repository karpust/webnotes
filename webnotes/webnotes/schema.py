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
    all_users = graphene.List(UserType)
    all_projects = graphene.List(ProjectType)

    def resolve_all_todos(root, info):  # self
        return Todo.objects.all()

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_projects(self, info):
        return Project.objects.all()


schema = graphene.Schema(query=Query)  # создали схему данных

# GraphQL-запрос: {allTodos {name, id, byUser{username}, byProject{name}}}
# all from snake_case to CamelCase!
# на http://127.0.0.1:8000/graphql/


# позволит одновременно получать ToDo, проекты и пользователей, связанных с проектом:
# {allTodos {id, name}
# allProjects{id, name, users{username}}}

# {allTodos {name, id, byUser{username}, byProject{name, users{username}}}}

# {allUsers{username, todoSet{id, name}}} если не указано related_name то todo_set
# {allProjects{name, todosByProject{id, name}}} если related_name='todos_by_project'
