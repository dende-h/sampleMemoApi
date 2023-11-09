# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

# ユーザーモデルを取得
User = get_user_model()

# ユーザー登録のためのシリアライザー
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('user_name', 'email', 'password')

    def create(self, validated_data):
        # ユーザーを作成
        user = User.objects.create_user(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
