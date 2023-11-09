"""
URL configuration for sampleMemoApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Djangoの管理サイト機能をインポート
from django.urls import path  # URLパターンを指定するための関数pathをインポート
from memos.views import UserRegistrationAPIView, home ,MySecureView # memosアプリのビューをインポート

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# URLパターンを定義するリスト
urlpatterns = [
    # admin/ にアクセスがあったときにDjangoの管理サイトを表示する
    path('admin/', admin.site.urls),  
    
    # register/ にアクセスがあったときにUserRegistrationAPIViewを使用してユーザー登録処理を行う
    # .as_view()はクラスベースのビューを関数ベースのビューとして呼び出すために使用する
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    
    # ルートURL（ドメインの直下、例: http://127.0.0.1:8000/）にアクセスがあったときにhomeビューを表示する
    path('', home, name='home'), 

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('secure-view/', MySecureView.as_view(), name='secure-view'),
]

