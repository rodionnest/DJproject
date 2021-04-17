from django_filters import FilterSet
from .models import Post
from django.forms import DateInput

import django_filters

class PostFilter(FilterSet):

    datetime = django_filters.DateFilter(field_name='datetime', widget=DateInput(attrs={'type': 'date'}),  lookup_expr='gt', label='Позже даты')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    author_name = django_filters.CharFilter(field_name='author_id__user_id__username', lookup_expr='icontains', label='Автор')

    # class Meta:
    #     model = Post
    #     fields = {
    #         'author_id__user_id__username': ['icontains'],
    #     }
