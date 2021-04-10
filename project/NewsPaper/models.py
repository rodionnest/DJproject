from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):

        #  получаем рейтинги всех постов
        post_rate = self.post_set.all().aggregate(_pr=Sum('rating'))
        post_rate = post_rate.get('_pr')

        #  получаем рейтинги всех комментариев автора
        comm_author_rate = self.user.comment_set.all().aggregate(_cr=Sum('comm_rating'))
        comm_author_rate = comm_author_rate.get('_cr')

        # получаем рейтинги всех комментариев к статьям автора
        comm_all_rate = Comment.objects.filter(
            post_id__author_id=self.id).aggregate(_car=Sum('comm_rating'))
        comm_all_rate = comm_all_rate.get('_car')

        self.author_rating = post_rate*3 + comm_author_rate + comm_all_rate
        self.save()

        return self.author_rating

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ManyToManyField(Category, through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    post_type = models.CharField(max_length=10, choices=[(
        'AR', 'Article'), ('NE', 'News')], default='AR')

    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    text = models.TextField(blank=True)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def preview(self):
        return self.text[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def __str__(self):
        return self.title + ', Автор: ' + self.author.user.username


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    post_datetime = models.DateTimeField(auto_now_add=True)
    comm_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def like(self):
        self.comm_rating += 1
        self.save()
        return self.comm_rating

    def dislike(self):
        self.comm_rating -= 1
        self.save()
        return self.comm_rating

    def __str__(self):
        return 'Пост: ' + self.post.title + ', Пользователь: ' + self.user.username
