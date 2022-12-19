"""webnotes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from mainapp import views as mainapp
from todoapp import views
from authapp.views import UserListApiView, UserDetailApiView
from userapp.views import UserListAPIViewGen
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view as get_schema_view_1
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view as get_schema_view_2

schema_view_1 = get_schema_view_1(  # drf_yasg: схема по которой сгенерится дока (OpenAPI-спецификация)
    openapi.Info(
        title='Webnotes',
        default_version='1.0',
        description='Documentation for project',
        contact=openapi.Contact(email='1@mail.ru'),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # права на документацию
)

# schema_view = get_schema_view_2(
#     title='Webnotes',
#     description='Documentation for project',
#     version='1.0',
#     url='http://127.0.0.1:8000/api/',
#     urlconf='webnotes/urls.py',
# )


router = DefaultRouter()
# router.register('users', views.UserModelViewSet)
# router.register('projects', views.ProjectModelViewSet)
# router.register('todos', views.TodoModelViewSet)
# router.register('todos', views.TodoViewSet, basename='todo')  # viewsets
# basename это начальная часть для генерации имени урла: todo-list, todo-update
# обязательно, если во viewset нет queryset(если нет basename берется из queryset)
# router.register('todos', views.TodoCustomViewSet)
# router.register('todos', views.TodoQuerysetFilterViewSet)  # filters 1
# filter_router = DefaultRouter()  # filters 3
# filter_router.register('param', views.TodoParamFilterView)  # filters 3
# router.register('todo', views.TodoDjangoFilterViewSet)  # django-filters 1
# router.register('todo', views.TodoCustomDjangoFilterViewSet)  # django-filters 2
# router.register('todo', views.TodoLimitOffsetPaginationViewSet)  # pagination

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),  # ModelViewSet, CustomViewSet
    # path('views/api-view/', views.TodoApiView.as_view()),  # ApiView
    # path('views/api-view/', views.todo_view),  # @api-view
    # path('api/create/', views.TodoCreateApiView.as_view()),  # Concrete View
    # path('api/list/', views.TodoListApiView.as_view()),
    # path('api/detail/<int:pk>/', views.TodoRetrieveUpdateDestroyAPIView.as_view()),
    # path('api/update/<int:pk>/', views.TodoRetrieveUpdateDestroyAPIView.as_view()),
    # path('api/delete/<int:pk>/', views.TodoRetrieveUpdateDestroyAPIView.as_view()),
    # path('viewsets/', include(router.urls)),  # viewsets
    # path('filters/kwargs/<str:name>/', views.TodoKwargsFilterView.as_view())  # filters 2
    # path('filters/', include(filter_router.urls)),  # filters 3

    # path('api/users/', UserListApiView.as_view()),  # ApiView
    path('api/users/', mainapp.UserListAPIViewGen.as_view()),
    # QueryParameterVersioning: http://127.0.0.1:8000/api/users/?version=2.0
    path('api/users/<int:pk>/', UserDetailApiView.as_view()),  # ApiView
    path('api/projects/', views.ProjectListApiView.as_view()),  # ApiView
    path('api/projects/<int:pk>/', views.ProjectDetailApiView.as_view()),  # ApiView
    path('api/todos/', views.TodoListApiView.as_view()),  # ApiView
    path('api/todos/<int:pk>/', views.TodoDetailApiView.as_view()),  # ApiView
    path('api-token-auth/', obtain_auth_token),  # авторизация по токену
    # авторизация по JWT-токену:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT: создание токена
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT: обновление токена
    # re_path(r'^api/(?P<version>\d.\d)/users/$', UserListAPIViewGen.as_view()),
    # UrlPathVersioning: http://127.0.0.1:8000/api/0.2/users/
    # path('api/users/0.1', include('userapp.urls', namespace='0.1')),  # NamespaceVersioning
    # path('api/users/0.2', include('userapp.urls', namespace='0.2')),  # NamespaceVersioning

    # schema from drf_yasg: http://127.0.0.1:8000/swagger.json, http://127.0.0.1:8000/swagger.yaml:
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_1.without_ui(cache_timeout=0), name='schema-json'),
    # schema from drf_yasg: http://127.0.0.1:8000/swagger/ :
    re_path(r'^swagger/$', schema_view_1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # schema from drf_yasg: http://127.0.0.1:8000/redoc/ :
    re_path(r'^redoc/$', schema_view_1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('openapi', get_schema_view_2(  # openapi-schema
        title='Webnotes',
        description='Documentation for project',
        version='1.0',
        url='http://127.0.0.1:8000/api/',
    ), name='openapi-schema'),

    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={
            'schema_url': 'openapi-schema'
        }),
         name='swagger-ui'),

    path('redoc-ui/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={
            'schema_url': 'openapi-schema'
        }),
         name='redoc'),

]
