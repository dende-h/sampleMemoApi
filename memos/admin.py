from django.contrib import admin
from .models import Memo, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email')  # パスワードは表示しない
    list_filter =['user_name']
    search_fields = ["user_name"]

class MemoAdmin(admin.ModelAdmin):
    list_display = ('user','title', 'content', 'complete_flag', 'created_at')
    list_filter = ['created_at']
    search_fields = ["title"]

admin.site.register(Memo, MemoAdmin)
admin.site.register(User, UserAdmin)