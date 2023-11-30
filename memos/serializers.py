# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Memo

# Djangoのデフォルトユーザーモデルを動的に取得します。
# これにより、カスタムユーザーモデルが設定されていても、このコードを変更せずに使用できます。
User = get_user_model()

# ユーザー登録のためのシリアライザーを定義します。
# serializers.ModelSerializerを継承することで、モデルベースでシリアライズ機能を実現します。
class UserRegistrationSerializer(serializers.ModelSerializer):
    # パスワードは書き込み専用フィールドとして定義します。
    # これは、パスワードが読み取り可能な形で返されることを防ぐためです。
    password = serializers.CharField(write_only=True)

    # Meta内部クラスでシリアライザーの設定を行います。
    class Meta:
        # Userモデルをシリアライザーに関連付けます。
        model = User
        # クライアントに公開するフィールドを指定します。
        # ここでは'username'、'email'、および'password'フィールドを含めます。
        fields = ('username', 'email', 'password')

    # createメソッドをオーバーライドし、validateされたデータからユーザーオブジェクトを作成します。
    def create(self, validated_data):
        # Userモデルのcreate_userメソッドを使用して新しいユーザーを作成します。
        # これにより、パスワードは適切にハッシュ化されます。
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # 作成されたユーザーオブジェクトを返します。
        return user

class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ['id', 'title', 'content', 'complete_flag', 'created_at']
        read_only_fields = ('user',)  # ユーザーはリクエストから直接セットされません