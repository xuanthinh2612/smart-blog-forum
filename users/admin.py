from django.contrib import admin
from .models import CustomUser, Profile
from .const import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
  list_display = ("email", "last_login", "is_active", "is_staff", "date_joined")
  search_fields = ["email"]
  list_filter = ("email", "date_joined")
#   prepopulated_fields = {"slug": ("firstname", "lastname")}    

class ProfileAdmin(admin.ModelAdmin):
  list_display = ("full_name", "birth_day", "bio", "avatar")
  search_fields = ["full_name"]
  list_filter = ("full_name", "birth_day")
#   prepopulated_fields = {"slug": ("firstname", "lastname")}
  class Meta: 
    js = APP_VALUE_ADMIN_SRC_JS
    css = APP_VALUE_ADMIN_SRC_CSS

admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.site_header = ADMIN_PAGE_HEADER
admin.site.site_title = ADMIN_PAGE_TITLE
