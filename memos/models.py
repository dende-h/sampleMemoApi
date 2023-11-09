# 必要なモジュールをインポート
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# カスタムユーザーマネージャークラス
class CustomUserManager(BaseUserManager):
    # 通常のユーザーを作成するためのメソッド
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The given email must be set')
        # ユーザーモデルのインスタンスを作成
        user = self.model(username=username, email=self.normalize_email(email))
        # パスワードをハッシュ化して設定
        user.set_password(password)
        # ユーザーをデータベースに保存
        user.save(using=self._db)
        return user

    # スーパーユーザーを作成するためのメソッド
    def create_superuser(self, username, email, password=None):
        # 上記のcreate_userを使ってユーザーを作成
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        # スーパーユーザーとして管理画面へのアクセス権を与える
        user.is_staff = True
        user.is_superuser = True
        # ユーザーをデータベースに保存
        user.save(using=self._db)
        return user

# カスタムユーザーモデルクラス
class User(AbstractBaseUser):
    # ユーザー名とメールアドレスは一意でなければならない
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    # ユーザーが管理画面にアクセスできるかどうか
    is_staff = models.BooleanField(default=False)
    # ユーザーがスーパーユーザーかどうか
    is_superuser = models.BooleanField(default=False)

    # カスタムユーザーマネージャーの使用を宣言
    objects = CustomUserManager()

    # ユーザー名をユーザーのユニークな識別子として使用
    USERNAME_FIELD = 'username'
    # スーパーユーザー作成時にメールアドレスの入力を要求
    REQUIRED_FIELDS = ['email']

    # オブジェクトを文字列で表現したときの挙動を定義
    def __str__(self):
        return self.username

    # ユーザーに特定の権限があるかどうかを確認（ここでは常にTrue）
    def has_perm(self, perm, obj=None):
        return True

    # ユーザーが特定のアプリのモジュールを見る権限があるかどうかを確認（ここでは常にTrue）
    def has_module_perms(self, app_label):
        return True

# メモモデルクラス
class Memo(models.Model):
    # メモは特定のユーザーに属しており、ユーザーが削除されたときにメモも削除される
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)  # メモのタイトル
    content = models.TextField()  # メモの内容、長いテキストに対応
    complete_flag = models.BooleanField(default=False)  # メモが完了したかどうかのフラグ
    created_at = models.DateTimeField(auto_now_add=True)  # メモが作成された日時

    # オブジェクトを文字列で表現したときの挙動を定義
    def __str__(self):
        return self.title