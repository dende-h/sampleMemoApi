# Create your tests here.
# tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)

class MemoAPITests(APITestCase):

    def setUp(self):
        # テストユーザーの作成
        self.user = User.objects.create_user(username='test', email='test@example.com', password='testpassword')
        # JWTトークンの取得
        refresh = RefreshToken.for_user(self.user)
        self.token = refresh.access_token
        # 認証情報を持つクライアントの設定
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        # メモの作成
        self.memo = self.user.memo_set.create(title='Test Memo', content='Test Content')

    def test_get_memos(self):
        # メモリスト取得のテスト
        url = reverse('memo-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_memo(self):
        # メモ作成のテスト
        url = reverse('memo-list')
        data = {'title': 'New Memo', 'content': 'Content of new memo'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_memo_detail(self):
        # メモ詳細取得のテスト
        url = reverse('memo-detail', kwargs={'pk': self.memo.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_memo(self):
        # メモ更新のテスト
        url = reverse('memo-detail', kwargs={'pk': self.memo.pk})
        data = {'title': 'Updated Memo', 'content': 'Updated content'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_memo(self):
        # メモ削除のテスト
        url = reverse('memo-detail', kwargs={'pk': self.memo.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)