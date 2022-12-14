import requests
from requests.auth import HTTPBasicAuth

# проверка работы базовой авторизации:
auth = HTTPBasicAuth(username='admin', password='admin')  # админ
response = requests.get('http://127.0.0.1:8000/api/users/1/', auth=auth)
assert response.status_code == 200
# print(response.status_code)
# print(response.json())
auth = HTTPBasicAuth(username='S', password='admin')  # неавторизованный юзер
response = requests.delete('http://127.0.0.1:8000/api/projects/3/', auth=auth)
# assert response.status_code == 401
# print(response.status_code)
# print(response.json())


# авторизация по токену(см скрины из постмана):
data = {'username': 'admin', 'password': 'admin'}
# получаем токен из пост-запроса:
response = requests.post('http://127.0.0.1:8000/api-token-auth/', data=data)
token = response.json().get('token')
# добавляем токен в заголовки:
response_todo = requests.get('http://127.0.0.1:8000/api/todos/', headers={'Authorization': f'Token {token}'})
assert response.status_code == 200
# print(response_todo.json())


# авторизация по jwt-токену:
# получаем токены доступа и обновления:
data = {'username': 'S', 'password': 'admin'}
response = requests.post('http://127.0.0.1:8000/api/token/', data=data)
result = response.json()  # при создании в response будет два токена: access и refresh
access_token = result['access']  # это токен для доступа(приложим к запросу)
refresh_token = result['refresh']  # это токен для обновления access_token
# авторизуемся с токеном доступа:
headers = {'Authorization': f'Bearer {access_token}'}  # Bearer-JWT
response = requests.get('http://127.0.0.1:8000/api/users/2', headers=headers)
assert response.status_code == 200
# обновляем access-токен:
response = requests.post('http://127.0.0.1:8000/api/refresh/', data={'refresh': refresh_token})
# print(response.status_code)
# print(response.text)
result = response.json()  # при обновлении в response будет один access-токен
access_token = result['access']  # получили новый access-токен который также приложим к запросам


