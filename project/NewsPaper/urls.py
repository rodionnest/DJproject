from django.urls import path
from .views import NewsList, NewDetail, SearchNews

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewDetail.as_view()),
    path('search', SearchNews.as_view()),
]
