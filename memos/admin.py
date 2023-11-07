from django.contrib import admin
from .models import Memo, User

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email')  # パスワードは表示しない

class MemoAdmin(admin.ModelAdmin):
    list_display = ('user','title', 'content', 'complete_flag', 'created_at')

admin.site.register(Memo, MemoAdmin)
admin.site.register(User, UserAdmin)