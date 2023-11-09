from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from django.http import Http404, HttpResponse
from rest_framework.permissions import IsAuthenticated
from .models import Memo
from .serializers import MemoSerializer
from drf_spectacular.utils import extend_schema





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


class MySecureView(APIView):
    # 認証済みのユーザーにのみアクセスを許可
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ここにビジネスロジックを実装
        return Response({"message": "Hello, world!"})

class MemoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 認証されたユーザーのメモを取得
        memos = Memo.objects.filter(user=request.user)
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        request=MemoSerializer,
        responses={201: MemoSerializer}
    )
    def post(self, request):
        # リクエストデータにユーザー情報を追加してシリアライザに渡す
        serializer = MemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Memo.objects.get(pk=pk, user=user)
        except Memo.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        memo = self.get_object(pk, request.user)
        serializer = MemoSerializer(memo)
        return Response(serializer.data)
    
    @extend_schema(
        request=MemoSerializer,
        responses={200: MemoSerializer}
    )
    def put(self, request, pk):
        memo = self.get_object(pk, request.user)
        serializer = MemoSerializer(memo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        memo = self.get_object(pk, request.user)
        memo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
