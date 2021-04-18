from django.urls import path
from .views import NewsList, NewDetail, SearchNews, PostDetail, PostCreateView, PostDeleteView, PostUpdateView

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('search', SearchNews.as_view()),
    path('add/', PostCreateView.as_view()),
    path('<int:pk>/edit/', PostUpdateView.as_view()),
    path('<int:pk>/delete/', PostDeleteView.as_view()),
]
