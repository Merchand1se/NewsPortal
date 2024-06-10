from django.urls import path

from .models import Subscriber
from .views import NewsList, NewDetail, create_new, NewDelete, NewUpdate, ArticleDelete, ArticleCreate, ArticleUpdate


urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewDetail.as_view(), name='new_detail'),
    path('create/', create_new.as_view(), name='new_create'),
    path('<int:pk>/edit/', NewUpdate.as_view(), name='new_update'),
    path('<int:pk>/delete/', NewDelete.as_view(), name='delete_new'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', Subscriber, name='subscriptions')
]