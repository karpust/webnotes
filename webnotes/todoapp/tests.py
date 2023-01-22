from django.test import TestCase
import django
django.setup()
from todoapp.views import TodoListApiView

import json
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, \
    APIClient, APISimpleTestCase, APITestCase
# from mixer.backend.django import mixer
# from django.contrib.auth.models import User
from todoapp.models import Project, Todo
from authapp.models import User
from mixer.backend.django import mixer


class TestProjectAPIView(TestCase):

    """  --------------------------------  класс APIRequestFactory  ------------------------------------------  """
    def test_get_projects_list_for_not_authenticated(self):  # метод проверяет страницу со списком проектов
        factory = APIRequestFactory()  # фабрика запросов(но не на сервер а во вью)
        request = factory.get('api/projects/')
        view = TodoListApiView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_projects_list_for_authenticated(self):
        factory = APIRequestFactory()
        request = factory.get('api/projects/')
        admin = User.objects.create_superuser('admin2', 'admin@admin.com',
                                              'admin123456')
        force_authenticate(request, admin)
        view = TodoListApiView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """  --------------------------------  класс APIClient  ------------------------------------------  """
    def test_get_detail_todo_for_not_auth(self):
        user_1 = User.objects.create()
        project_1 = Project.objects.create(name='project_555')
        # print(Project.objects.get(pk=13))
        # print(Project.objects.all())
        todo = Todo.objects.create(name='note_555', content='life is the sea', by_user=user_1,
                                   by_project=project_1, status='PR')

        client = APIClient(SERVER_NAME='localhost')
        response = client.get(f'/api/todos/{todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_todo_for_not_auth(self):
        user_1 = User.objects.create()
        project_1 = Project.objects.create(name='project_555')
        todo = Todo.objects.create(name='note_555', content='life is the sea', by_user=user_1,
                                   by_project=project_1, status='PR')
        client = APIClient(SERVER_NAME='localhost')
        response = client.put(path=f'/api/todos/{todo.id}/', data={'name': 'note_444'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_put_todo_for_auth(self):
    #     user_1 = User.objects.create()
    #     project_1 = Project.objects.create(name='project_555')
    #     todo = Todo.objects.create(name='note_555', content='life is the sea', by_user=user_1,
    #                                by_project=project_1, status='PR')
    #     client = APIClient(SERVER_NAME='localhost')  # or allow_hosts in settings
    #     User.objects.create_superuser('admin2', 'admin@admin.com', 'admin123456')
    #     client.login(username='admin2', password='admin123456')
    #     response = client.put(path=f'/api/todos/{todo.id}/', data={"name": "note_444"})
    # {"name":["note_444"]} сериалайзер не проходит валидацию с такими данными
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


"""  --------------------------------  класс APISimpleTestCase  ------------------------------------------  """

# class TestMath(APISimpleTestCase):
#     def test_sqrt(self):
#         import math
#         self.assertEqual(math.sqrt(4), 2)

"""  --------------------------------  класс APITestCase  ------------------------------------------  """


class TestTodoApiView(APITestCase):
    def test_get_todos_list(self):
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_put_todo_for_auth(self):
    #     # user_1 = User.objects.create()
    #     # project_1 = Project.objects.create(name='project_555')
    #     # todo = Todo.objects.create(name='note_555', content='life is the sea', by_user=user_1,
    #     #                            by_project=project_1, status='PR')
    #     todo = mixer.blend(Todo)
    #     # todo = mixer.blend(Todo, name='Алые паруса')  # остальные поля создаст случайно
    #     # todo = mixer.blend(Todo, by_project__name='superSiteNNN')  # указали поле связанной модели
    #     User.objects.create_superuser('admin2', 'admin@admin.com', 'admin123456')
    #     # print(User.objects.get(username='admin2').id)
    #     self.client.login(username='admin2', password='admin123456')
    #     response = self.client.put(path=f'/api/todos/{todo.id}/', data={"name": "note_444"})
    # {"name":["note_444"]} сериалайзер не проходит валидацию с такими данными
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

