from rest_framework import serializers
from test_models import Author, Book, Biography


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    birthday_year = serializers.IntegerField()


class BiographySerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1024)
    author = AuthorSerializer()  # сложный, автор передастся в словаре


class BookSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    authors = AuthorSerializer(many=True)  # сложный, сериализуем несколько авторов(несколько словарей)


author1 = Author('Грин', 1880)
serializer = AuthorSerializer(author1)
print(serializer.data)
# {'name': 'Грин', 'birthday_year': 1880}

biography = Biography('Текст биографии', author1)
serializer = BiographySerializer(biography)
print(serializer.data)
# {'text': 'Текст биографии', 'author': OrderedDict([('name', 'Грин'), ('birthday_year', 1880)])}

author2 = Author('Пушкин', 1799)
book = Book('Некоторая книга', [author1, author2])

serializer = BookSerializer(book)
print(serializer.data)
# {'name': 'Некоторая книга', 'authors': [
# OrderedDict([('name', 'Грин'), ('birthday_year', 1880)]),
# OrderedDict([('name', 'Пушкин'), ('birthday_year', 1799)])
# ]}


