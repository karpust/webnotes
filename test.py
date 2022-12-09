import requests
from requests.auth import HTTPBasicAuth

# auth = HTTPBasicAuth(username='admin', password='admin')
# response = requests.get('http://127.0.0.1:8000/api/users/1/', auth=auth)
# print(response.status_code)
# print(response.json())

auth = HTTPBasicAuth(username='S', password='admin')  # developer
response = requests.delete('http://127.0.0.1:8000/api/projects/3/', auth=auth)
print(response.status_code)
print(response.json())

# # проверка работы авторизации(то же в постмане см скрины):
# data = {'username': 'admin', 'password': 'admin'}
# # получаем токен из пост-запроса:
# response = requests.post('http://127.0.0.1:8000/api-token-auth/', data=data)
# token = response.json().get('token')
# # добавляем токен в заголовки:
# response_todo = requests.get('http://127.0.0.1:8000/api/todos/', headers={'Authorization': f'Token {token}'})
# print(response_todo.json())

