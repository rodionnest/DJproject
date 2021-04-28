from django.contrib import admin
from django.urls import path, include
from NewsPaper import views
from django.views.generic import RedirectView
from NewsPaper.views import UserUpdateView, upgrade_me


urlpatterns = [
    path('', RedirectView.as_view(url='/news')),
    path('admin/', admin.site.urls),
    path('news/', include('NewsPaper.urls')),
    path('news/search', include('NewsPaper.urls')),
    path('profile/', UserUpdateView.as_view()),
    path('profile/upgrade/', upgrade_me, name = 'upgrade'),
    path('accounts/', include('allauth.urls')),
]
