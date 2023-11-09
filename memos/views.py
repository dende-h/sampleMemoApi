from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from django.http import HttpResponse

# UserRegistrationAPIViewクラスはAPIViewクラスを継承しており、
# RESTフレームワークの基本的なAPIビュー機能を利用することができます。
class UserRegistrationAPIView(APIView):
    # POSTメソッドのリクエストを処理するためのメソッドを定義しています。
    # ユーザー登録のためのデータがリクエストとして送られてくることを想定しています。
    def post(self, request, *args, **kwargs):
        # リクエストデータをUserRegistrationSerializerに渡してバリデーションを行います。
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # バリデーションが成功した場合、serializer.save()でユーザーを保存します。
            user = serializer.save()
            # 成功のレスポンスとしてユーザー情報と201 Createdステータスを返します。
            return Response({
                "user": UserRegistrationSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        # バリデーションが失敗した場合、エラーメッセージと400 Bad Requestステータスを返します。
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ホームページへのリクエストに対するシンプルな応答を返すためのビュー関数です。
# 特定のHTMLテンプレートを使用する代わりに、HTTPレスポンスとして単純なテキストを返しています。
def home(request):
    # リクエストに対して、"Welcome to my site!"というメッセージが含まれたHTTPレスポンスを返します。
    return HttpResponse("Welcome to my site!")
