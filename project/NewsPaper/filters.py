from django_filters import FilterSet # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'datetime': ['gt'], # количество товаров должно быть больше или равно тому, что указал пользователь
            'text': ['icontains'], # цена должна быть меньше или равна тому, что указал пользователь
        }
