from django.urls import path
from .views import *

urlpatterns = [
    # article/<slug:slug> phải ở dưới cùng vì
    # Khi vào /api/article/list django sẽ hiểu list là một slug nên sẽ vào /api/ticle/<slug:slug> thay vì vào /list
    # Cách sửa:
    # 1. Đưa /api/article/list lên trên
    # 2. định nghĩa rõ ràng /api/article/list/
    # 3. đổi article/list thành articles/list

    path('article/<slug:slug>', ArticleDetailAPIView.as_view(), name='api_get_article'),
    path('article/private/<slug:slug>', ArticlePrivateDetailAPIView.as_view(), name='api_get_article'),
    path('articles/list/', ArticleListAPIView.as_view(), name='api_get_article_list'),
    path('articles/my-list/', ArticleMyListAPIView.as_view(), name='api_get_my_article_list'),
    
    path('register/', UserRegister.as_view(), name='api_login'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('profile/', UserInfoAPIView.as_view(), name='api_login')
]