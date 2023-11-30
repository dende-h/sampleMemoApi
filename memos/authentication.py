# from django.contrib.auth.backends import ModelBackend
# from django.core.exceptions import MultipleObjectsReturned
# from .models import User

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(email=email)
#             if user.check_password(password) and self.user_can_authenticate(user):
#                 return user
#         except User.DoesNotExist:
#             # ユーザーが存在しない場合の処理
#             return None
#         except MultipleObjectsReturned:
#             # メールアドレスが複数存在する場合の処理
#             return User.objects.filter(email=email).order_by('id').first()
#         return None
