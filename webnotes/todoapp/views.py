from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from .models import Project, Todo
from .serializers import ProjectModelSerializer, TodoModelSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework import mixins
from .filters import TodoFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import status
from django.http import Http404
from rest_framework.settings import api_settings
from rest_framework.generics import GenericAPIView
import django_filters.rest_framework
from rest_framework.parsers import JSONParser


class ProjectLimitOffsetPagination(LimitOffsetPagination):  # not working automatically in APIView class
    default_limit = 10  # http://127.0.0.1:8000/api/projects/?limit=10&offset=10

# class ProjectPageNumberPagination(PageNumberPagination):  # not working automatically in APIView class
#     page_size = 2

# class ProjectModelViewSet(ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectModelSerializer


class ProjectListApiView(APIView, ProjectLimitOffsetPagination):
    """implemented methods: get, post"""
    # renderers из настроек проекта
    # template = None # 'rest_framework/pagination/previous_and_next.html'   'rest_framework/pagination/numbers.html'
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    # 'to_html() must be implemented to display page controls.')
    # filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        name = self.request.query_params.get('name', '')  # http://127.0.0.1:8000/api/projects/?name=new_
        projects = Project.objects.all()
        if name:
            projects = projects.filter(name__contains=name)
        return projects

    def get(self, request):
        projects = self.get_queryset()
        # paginator = ProjectLimitOffsetPagination() можно так, но отнаследовались
        page = self.paginate_queryset(projects, request)
        if page:
            serializer = ProjectModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # count, next, previous, result on page
        serializer = ProjectModelSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # сохраняем в модель
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailApiView(APIView):
    """implemented methods: get, put, patch, delete"""
    # renderers из настроек проекта

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):  # get - взяли данные из модели и вернули их словарем
        project = self.get_object(pk=pk)
        serializer = ProjectModelSerializer(project)
        print(serializer.data)
        return Response(serializer.data)

    def put(self, request, pk):
        # а если в request.data передать новый pk то будет post(((
        project = self.get_object(pk)
        serializer = ProjectModelSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # {"name": "superSiteNNN"} - add in browser all in double quotes
        project = self.get_object(pk)
        serializer = ProjectModelSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """change status project"""
        project = self.get_object(pk)
        data = {'is_active': 0}
        serializer = ProjectModelSerializer(project, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TodoModelViewSet(ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer


class TodoLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20


@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])  # или из настроек проекта
def todo_list_api_view(request):
    """
    добавить фильтрацию по проекту;
    размер страницы 20
    """
    if request.method == 'GET':
        todos = Todo.objects.all()
        project = request.query_params.get('project')  # default=None
        # http://127.0.0.1:8000/api/todos/?project=1

        date_after = request.query_params.get('date_after')
        date_before = request.query_params.get('date_before')
        # http://127.0.0.1:8000/api/todos/?date_after=2022-11-23 12:00&date_before=2022-11-23 14:00

        # http://127.0.0.1:8000/api/todos/?date_after=2022-11-23%2012:00&date_before=2022-11-23%2014:00&project=2

        if date_after and date_before:
            todos = todos.filter(publication_date__range=(date_after, date_before))  # range
        if project:
            todos = todos.filter(by_project=project)  # exact
        paginator = TodoLimitOffsetPagination()
        page = paginator.paginate_queryset(todos, request)
        if page:
            serializer = TodoModelSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = TodoModelSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TodoModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def todo_detail_api_view(request, pk=None):
    if request.method == 'GET':
        todo = get_object_or_404(Todo, pk=pk)  # Todo.objects.get(pk=pk)
        serializer = TodoModelSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoModelSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        todo = get_object_or_404(Todo, pk=pk)
        serializer = TodoModelSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo = get_object_or_404(Todo, pk=pk)
        data = {'status': 'CL'}
        serializer = TodoModelSerializer(todo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
используем APIView:
базовый класс не имеет методов реализаций запросов,
определяем те которые нам понадобятся:
'''
# class TodoApiView(APIView):
#     renderer_classes = [JSONRenderer]  # список renderers
#
#     def get(self, request, format=None):
# https://www.django-rest-framework.org/tutorial/2-requests-and-responses/#adding-optional-format-suffixes-to-our-urls
#         todos = Todo.objects.all()
#         serializer = TodoModelSerializer(todos, many=True)
#         return Response(serializer.data)  # data to be rendered


'''
используем @api_view:
APIView для функций
'''
# @api_view(['GET'])  # список доступных запросов
# @renderer_classes([JSONRenderer])  # список renderers
# def todo_view(request):
#     todos = Todo.objects.all()
#     serializer = TodoModelSerializer(todos, many=True)
#     return Response(serializer.data)


"""
Concrete Views
самый распространенный способ представления
в его основе GenericAPIView + миксины
лаконичен: нужно отнаследоваться и прописать 
queryset и serializer_class
"""
# class TodoCreateApiView(CreateAPIView):
#     # renderer_classes = [JSONRenderer]
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer
#
#
# class TodoListApiView(ListAPIView):
#     renderer_classes = [JSONRenderer]  # откроет страницу с json
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer
#
#
# class TodoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     # renderer_classes = [JSONRenderer]
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer


"""
используем ViewSet
несколько представлений в одном наборе
все методы класса нужно определить, их нет
"""
# class TodoViewSet(ViewSet):
#     # renderer_classes = [JSONRenderer]
#
#     def list(self, request):
#         todos = Todo.objects.all()
#         serializer = TodoModelSerializer(todos, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):  # -> http://127.0.0.1:8000/viewsets/todos/1/
#         todo = get_object_or_404(Todo, pk=pk)
#         serializer = TodoModelSerializer(todo)
#         return Response(serializer.data)
#
#     def destroy(self, request, pk=None):  # action name destroy or delete
#         todo = get_object_or_404(Todo, pk=pk)
#         todo.delete()
#         serializer = TodoModelSerializer(todo, many=True)
#         return Response(serializer.data)
#
#     def update(self, request, pk=None):
#         todo = get_object_or_404(Todo, pk=pk)
#         serializer = TodoModelSerializer(todo)
#         return Response(serializer.data)
#
#     def partial_update(self, request, pk=None):
#         todo = get_object_or_404(Todo, pk=pk)
#         serializer = TodoModelSerializer(todo)
#         return Response(serializer.data)
#
#     @action(methods=['GET'], detail=True)
#     # extra action: detail: action for 1 object(add pk to address) or for all collection
#     def todo_text_only(self, request, pk=None):
#         todo = get_object_or_404(Todo, pk=pk)
#         # todo = Todo.objects.get(pk=pk)
#         return Response({'todo.content': todo.content})
#         # -> http://127.0.0.1:8000/viewsets/todos/1/todo_text_only/
"""
используем ModelViewSet
все actions уже определены
"""
# class TodoModelViewSet(ModelViewSet):
#     queryset = Todo.objects.all()
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     serializer_class = TodoModelSerializer

"""
Custom ViewSet
используем GenericViewSet + сами выбираем миксины
"""
# class TodoCustomViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
#                         mixins.CreateModelMixin, GenericViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


"""-----------------------------фильтрация----------------------------------"""
"""
параметр для фильтрации захардкодили - не удобно
"""
# class TodoQuerysetFilterViewSet(ModelViewSet):
#     serializer_class = TodoModelSerializer
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     queryset = Todo.objects.all()
#
#     def get_queryset(self):
#         return Todo.objects.filter(name__contains='_1')

"""
параметр передаем в урл: http://127.0.0.1:8000/filters/kwargs/todo_/
и берем из урла - но тогда в уллах много path
"""
# class TodoKwargsFilterView(ListAPIView):
#     serializer_class = TodoModelSerializer
#
#     def get_queryset(self):
#         name = self.kwargs['name']  # name = 'todo_'
#         return Todo.objects.filter(name__contains=name)


"""
используем параметры запроса - лучше
передаем параметр для фильтрации в урл: http://127.0.0.1:8000/filters/param/?name=_1  # ?name=_1
значения параметра берем из self.request.query_params.get
если параметр есть
не нужно создавать кучу путей
"""
# class TodoParamFilterView(ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer
#
#     def get_queryset(self):
#         name = self.request.query_params.get('name', '')
#         todos = Todo.objects.all()
#         if name:
#             todos = todos.filter(name__contains=name)
#         return todos


"""
django_filters 
позволяет избежать повторений кода
использует request.query_params
кнопкой выбрать имя полей
"""
# class TodoDjangoFilterViewSet(ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer
#     filterset_fields = ['name', 'by_user']  # equality-based filtering - полное соответствие имени поля


# class TodoCustomDjangoFilterViewSet(ModelViewSet):
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer
#     filterset_class = TodoFilter  # этот фильтер по части в имени


"""
Пагинация:
LimitOffsetPagination
задаем кол-во записей для вывода
ссылка теперь: http://127.0.0.1:8000/api/todo/?limit=1&offset=1
"""
# class TodoLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 1


# class TodoLimitOffsetPaginationViewSet(ModelViewSet):
#
#     renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
#     queryset = Todo.objects.all()
#     serializer_class = TodoModelSerializer
#     pagination_class = TodoLimitOffsetPagination

