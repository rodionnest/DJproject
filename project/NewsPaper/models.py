from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    _author_rating = models.IntegerField(default=0, db_column='author_rating')

    @property
    def author_rating(self):
        return self._amount

    @author_rating.setter
    def author_rating(self, value):
        self._author_rating = value
        self.save()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self, _username):
        _user_id = User.objects.get(username=_username)

        #  получаем рейтинги всех статей
        QS_AR_rate = [i['rating'] for i in Post.objects.filter(
            author_id__user_id__username=_username, post_type='AR').values('rating')]

        #  получаем рейтинги всех комментариев автора
        QS_author_comm_rate = [i['comm_rating'] for i in Comment.objects.filter(
            user_id=_user_id.id).values('comm_rating')]

        # получаем рейтинги всех комментариев к статьям автора
        QS_all_comm_rate = [i['comm_rating'] for i in Comment.objects.filter(
            post_id__author_id__user_id=_user_id.id, post_id__post_type='AR').values('comm_rating')]

        self.author_rating = Total_author_rating = sum(QS_AR_rate)*3 + \
            sum(QS_author_comm_rate) + sum(QS_all_comm_rate)

        return Total_author_rating

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
    post_type = models.CharField(max_length=10,
                                 choices=[('AR', 'Article'), ('NE', 'News')], default='AR')  # ! насколько это корректное решение? Или лучше реализовывать через отдельную переменную?
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
        return self.comm_rating

    def dislike(self):
        return self.comm_rating

    def __str__(self):
        return self.title


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
        return self.comm_rating

    def dislike(self):
        self.comm_rating += -1
        return self.comm_rating

    def __str__(self):
        return 'Пост: ' + self.post.title + ', Пользователь: ' + self.user.username
