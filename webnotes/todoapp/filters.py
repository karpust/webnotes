from django_filters import rest_framework as filters
from .models import Todo


# class TodoFilter(filters.FilterSet):
#     # name = filters.CharFilter()  # exact
#     name = filters.CharFilter(lookup_expr='contains')  # only contains
#     publication_date = filters.DateTimeFromToRangeFilter()
#     # http://127.0.0.1:8000/api/todo/?name=&publication_date_after=2022-11-23T12%3A00&publication_date_before=2022-11-23T15%3A30
#
#     # publication_date = filters.DateTimeFilter(lookup_expr='range')  # ???
#
#
#     class Meta:
#         model = Todo
#         # if list then exact if dict-contains:
#         fields = ['name', 'publication_date']  # and exact
#         # fields = {'name': ['contains']}  # and contains



# class TodoFilter(filters.FilterSet):
#     name = filters.CharFilter(lookup_expr='contains')
#     publication_date = filters.DateTimeFilter(lookup_expr='range')
#
#     class Meta:
#         model = Todo
#         fields = ['name', 'publication_date']

class TodoFilter(filters.FilterSet):  # TodoFilterByCreationDate
    # name = filters.DateTimeFilter()
    # publication_date = filters.DateTimeFromToRangeFilter()
    # publication_date = filters.DateTimeFilter()

    class Meta:
        model = Todo
        fields = {
            'publication_date': ['range'],  # publication_date__range
            # 'name': ['contains']  # name__contains
        }
# http://127.0.0.1:8000/api/todo/?publication_date__range=2022-11-23T12:00,2022-11-23T15:00  # передадим в урл

# 2022-11-23T12:00,2022-11-23T15:00  # передаем в фильтр джанго

