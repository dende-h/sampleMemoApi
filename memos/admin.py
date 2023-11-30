from django.contrib import admin
from .models import Memo, User
# from django.contrib.admin import AdminSite
# from .forms import CustomAdminAuthenticationForm

# class CustomAdminSite(AdminSite):
#     login_form = CustomAdminAuthenticationForm

# custom_admin_site = CustomAdminSite(name='custom_admin')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')  # パスワードは表示しない
    list_filter =['username']
    search_fields = ["username"]

class MemoAdmin(admin.ModelAdmin):
    list_display = ('user','title', 'content', 'complete_flag', 'created_at')
    list_filter = ['created_at']
    search_fields = ["title"]

admin.site.register(Memo, MemoAdmin)
admin.site.register(User, UserAdmin)