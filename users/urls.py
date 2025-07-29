from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView


urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.homepage, name='homepage'),
    path('update-profile/', views.update_profile, name='update_profile')
]