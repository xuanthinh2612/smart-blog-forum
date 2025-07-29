from django.urls import path
from . import views

urlpatterns = [
    path('create-article/', views.create_article, name='createarticle'),
    path('list-article/', views.list_article, name='listarticle'),
    path('update-article/<slug:slug>', views.update_article, name='updatearticle'),
    path('article/<slug:slug>', views.view_article, name='viewarticle'),
    path('article/<slug:slug>/comment', views.add_comment, name='add_comment'),
]