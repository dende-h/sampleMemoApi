from django.test import TestCase

# Create your tests here.
# tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserRegistrationTestCase(APITestCase):
    # ユーザー登録のテストケースを定義します。
    
    def test_user_registration(self):
        # 新しいユーザーのデータを辞書形式で作成します。
        data = {
            "user_name": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
        
        # テストクライアントを使用して、ユーザー登録のためのPOSTリクエストを送信します。
        # reverse関数はURLパターンの名前を解決してURLを取得します。
        response = self.client.post(reverse('user-register'), data)
        
        # レスポンスのステータスコードが201 CREATEDであることを検証します。
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Userモデルにレコードが1つだけ存在することを検証します。
        self.assertEqual(User.objects.count(), 1)
        
        # 作成されたユーザーのユーザー名が指定したものと一致することを検証します。
        self.assertEqual(User.objects.get().user_name, 'newuser')
