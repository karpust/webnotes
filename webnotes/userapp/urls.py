from django.urls import path
from .views import UserListAPIViewGen


app_name = 'userapp'

urlpatterns = [
    path('', UserListAPIViewGen.as_view()),  # NamespaceVersioning: http://127.0.0.1:8000/api/users/0.1 or 0.2
]

