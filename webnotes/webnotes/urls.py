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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todoapp import views
from authapp.views import UserListApiView, UserDetailApiView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


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

    path('api/users/', UserListApiView.as_view()),  # ApiView
    path('api/users/<int:pk>/', UserDetailApiView.as_view()),  # ApiView
    path('api/projects/', views.ProjectListApiView.as_view()),  # ApiView
    path('api/projects/<int:pk>/', views.ProjectDetailApiView.as_view()),  # ApiView
    path('api/todos/', views.TodoListApiView.as_view()),  # ApiView
    path('api/todos/<int:pk>/', views.TodoDetailApiView.as_view()),  # ApiView
    path('api-token-auth/', obtain_auth_token),  # авторизация по токену
    # авторизация по JWT-токену:
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT: создание токена
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT: обновление токена
]
