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
            "username": "newuser",
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
        self.assertEqual(User.objects.get().username, 'newuser')

class SecureViewTestCase(APITestCase):
    def setUp(self):
        # テストユーザーを作成
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.token_obtain_pair_url = reverse('token_obtain_pair')
        self.secure_url = reverse('secure-view')  # MySecureViewのURL名を'secure-view'と仮定

    def test_secure_view_unauthorized(self):
        # 認証されていないリクエストが401 Unauthorizedを返すことを確認
        response = self.client.get(self.secure_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_secure_view_with_token(self):
        # テストユーザーでログインしてトークンを取得
        response = self.client.post(self.token_obtain_pair_url, {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

        # 取得したアクセストークンを使用して認証済みリクエストを送信
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        response = self.client.get(self.secure_url)

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
