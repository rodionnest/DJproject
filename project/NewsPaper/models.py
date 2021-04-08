from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self, _username):
        # получаем рейтинги всех статей
        # QS_AR_rate = [i['rating'] for i in Post.objects.filter(
        #     author_id__user_id__username=_username, post_type='AR').values('rating')]
        # # получаем рейтинги всех комментариев автора
        user_id = User.objects.get(username=_username)
        QS_author_comm_rate = [i['comm_rating'] for i in Comment.objects.filter(
            user_id=user_id.id).values('comm_rating')]

        # QS_author_comm_rate = [i['comm_rating'] for i in Comment.objects.filter(
        #     user_id=user_id.id).values('comm_rating')]

        return QS_author_comm_rate

    def product_sum(self):
        a = self.author_rating
        return a

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
        self.comm_rating += 1
        return self.comm_rating

    def dislike(self):
        self.comm_rating += -1
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
