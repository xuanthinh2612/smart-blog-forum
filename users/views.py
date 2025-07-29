from django.shortcuts import render, redirect
from .models import *
from .form import *
from .const import ARTICLE_PUBLISHED_STATUS
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login  # <-- Import hàm login
from django.core.paginator import Paginator
from blogapp.models import *


def homepage(request):
    list_category = Category.objects.all()
    set_article_list = {}
    for category in list_category:
        list_article = Article.objects.filter(status=ARTICLE_PUBLISHED_STATUS, category=category)
        if list_article:
            set_article_list[category] = list_article

    context = {
        "set_article_list": set_article_list
    }

    return render(request, 'users/homepage.html', context)

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Bạn đã đăng nhập.")
            return redirect('homepage')
        return super().dispatch(request, *args, **kwargs)
    
def register(request):

    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST, request.FILES)

    if request.method == 'POST':

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)  # <-- Auto login user mới tạo

            return redirect('homepage')
        else:
            # Trường hợp form không hợp lệ => trả về form có lỗi
            return render(request, 'users/register.html', {
                'user_form': user_form,
                'profile_form': profile_form
            })
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
        context = {
            "user_form": user_form,
            "profile_form": profile_form
        }
        return render(request, 'users/register.html', context)
    
def update_profile(request):
    if request.method == 'POST':
        user_form = UserFormForUpdate(request.POST, instance = request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Cập nhật thành công!")
            # ✅ Giữ user đăng nhập sau khi thay đổi email
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)

            return redirect("homepage")
        else:
             # ⛔ Form không hợp lệ => quay lại trang và giữ lại form + lỗi
            context = {
                "user_form": user_form,
                "profile_form": profile_form
            }
            return render(request, 'users/register.html', context)
    else:
        user_form = UserFormForUpdate(instance = request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        context = {
            "user_form": user_form,
            "profile_form": profile_form
        }
        return render(request, 'users/register.html', context)
    