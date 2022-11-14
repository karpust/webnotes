import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser  # dict< json,html,xml
from rest_framework.renderers import JSONRenderer  # dict > json,html,xml
from test_models import Author


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    birthday_year = serializers.IntegerField()


def start():
    """ преобразования данных для передачи с бэка на фронт: """

    author = Author('Толстой', 1828)
    # передали сериализатору экз класса (объект модели)
    # он вернул словарь:
    serializer = AuthorSerializer(author)
    print(serializer.data)  # {'name': 'Толстой', 'birthday_year': 1828}
    print(type(serializer.data))  # словарь - <class 'rest_framework.utils.serializer_helpers.ReturnDict'>

    renderer = JSONRenderer()
    # рендереру отдали словарь:
    # рендерер: словарь -> json-строка -> байты
    json_bytes = renderer.render(serializer.data)
    print(json_bytes)  # b'{"name":"\xd0\xa2\xd0\xbe\xd0\xbb\xd1\x81\xd1\x82\xd0\xbe\xd0\xb9","birthday_year":1828}'
    print(type(json_bytes))  # <class 'bytes'>
    # дальше байты передаются на фронт

    """ преобразования при получении данных с фронта: """
    stream = io.BytesIO(json_bytes)  # преобразовали байты в объект BytesIO
    print(stream)  # <_io.BytesIO object at 0x0000021DC116C040>
    # объект BytesIO передали парсеру:
    # парсер: BytesIO -> словарь
    data = JSONParser().parse(stream)  # {'name': 'Толстой', 'birthday_year': 1828}
    print(type(data))  # <class 'dict'>
    serializer = AuthorSerializer(data=data)  # без инстанса - создание нового объекта
    # serializer = AuthorSerializer(author, data=data)  # c инстансом - обновление сущ объекта
    print(serializer.is_valid())  # True
    print(serializer.validated_data)  # OrderedDict([('name', 'Толстой'), ('birthday_year', 1828)])
    print(type(serializer.validated_data))  # словарь - <class 'collections.OrderedDict'>


start()
