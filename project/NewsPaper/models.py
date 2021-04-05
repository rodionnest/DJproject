from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# class Post(models.Model):
#     username = models.ForeignKey(Author, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'Пост'
#         verbose_name_plural = 'Посты'


# class PostCategory(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name


# class Comment(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'
