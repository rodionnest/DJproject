from django.contrib import admin
from NewsPaper.models import Author, Category

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
