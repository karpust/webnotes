import io
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from test_models import Author


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    birthday_year = serializers.IntegerField()

    def create(self, validated_data):
        return Author(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)  # берем из поля name или из default(instance.name)
        instance.birthday_year = validated_data.get('birthday_year', instance.birthday_year)
        return instance

    def validate_birthday_year(self, value):  # в value приходит то что проверяем
        # для валидации по 1 полю создается метод validate_имя_поля
        if value < 5:
            raise serializers.ValidationError('Год рождения не может быть отрицательным')
        return value

    # def validate(self, attrs):
    #     # для валидации по неск полям создается метод validate
    #     if attrs['name'] == 'Толстой' and attrs['birthday_year'] != 1828:
    #         raise serializers.ValidationError('Неверный год рождения Толстого')
    #     return attrs


def start():
    author = Author('Толстой', 1828)
    serializer = AuthorSerializer(author)  # -> словарь

    renderer = JSONRenderer()
    json_bytes = renderer.render(serializer.data)  # -> байты

    stream = io.BytesIO(json_bytes)
    data = JSONParser().parse(stream)  # -> словарь

    serializer = AuthorSerializer(data=data)  # when save - call create
    serializer.is_valid()  # call all exists validators

    """ Создание """
    # author = serializer.save()
    # # save вызывает либо create(data, no instance) либо update(data+instance)
    # print(type(author))
    # print(author)

    """ Обновление всех данных """
    # data = {'name': 'Пушкин', 'birthday_year': 1880}
    # serializer = AuthorSerializer(author, data=data)  # call update
    # serializer.is_valid()  # если ок данные попадают в validated_data
    # print(serializer.validated_data)  # OrderedDict([('name', 'Пушкин'), ('birthday_year', 1880)])
    # author = serializer.save()  # при сохранении поля заполняются из validated_data
    # print(author)

    """ Обновление частичное """
    data = {'birthday_year': 1828}
    serializer = AuthorSerializer(author, data=data, partial=True)  # если обновляем не все поля
    serializer.is_valid()  # когда запускается is_valid, запускаются все валидаторы кот есть
    author = serializer.save()
    print(f'{author} {author.birthday_year}')

    """ Проверка 1го поля """
    # data = {'birthday_year': 1}  # 1 пойдет в value в валидаторе
    # serializer = AuthorSerializer(author, data=data, partial=True)
    # if serializer.is_valid():
    #     author = serializer.save()
    #     print(f'{author} {author.birthday_year}')
    # else:
    #     print(serializer.errors)

    """ Проверка всех полей """
    # data = {
    #     'name': 'Толстой',
    #     'birthday_year': 2000
    # }
    # serializer = AuthorSerializer(author, data=data)
    # if serializer.is_valid():
    #     author = serializer.save()
    #     print(author)
    # else:
    #     print(serializer.errors)


start()
