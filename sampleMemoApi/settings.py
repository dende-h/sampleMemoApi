"""
Django settings for sampleMemoApi project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import environ                  # environライブラリをインポートして環境変数を管理しやすくします。
import datetime                # datetimeモジュールをインポートして時間に関するオブジェクトを使用します。
 
env = environ.Env()            # 環境変数オブジェクトを作成します。
env.read_env('.env')           # プロジェクトのルートにある.envファイルから環境変数を読み込みます。

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')  # .envファイルからシークレットキーを読み込みます。

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'memos',
    'drf_spectacular'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sampleMemoApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sampleMemoApi.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'), # 環境変数からデータベース名を読み込む
        'USER': env('DB_USER'), # 環境変数からユーザー名を読み込む
        'PASSWORD': env('DB_PASSWORD'), # 環境変数からパスワードを読み込む
        'HOST': <DB_HOST>, # 環境変数から書き換える用のプレースホルダ
        'PORT': env('DB_PORT'), # 環境変数からポートを読み込む
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'memos.User'  # カスタムユーザーモデルを使用するための設定

# Django REST Frameworkの設定
REST_FRAMEWORK = {
    # JWTを使用した認証方式を設定します。
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    # アクセストークンとリフレッシュトークンの有効期限を設定します。
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=3),    # アクセストークンは3日間有効です。
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),    # リフレッシュトークンは7日間有効です。
    # その他のJWT設定をここに追加できます。
}

SPECTACULAR_SETTINGS = {
    'TITLE': '簡易メモアプリAPI',
    'DESCRIPTION': '簡易メモアプリのユーザー登録、認証とメモのCRUD処理を実行するためのAPIです',
    'VERSION': '1.0.0',
    # Optional: 'TERMS_OF_SERVICE', 'CONTACT', 'LICENSE' なども含めることができます
    'SERVERS': [
        {
            'url': 'https://api.example.com/',
            'description': 'Production server',
        },

    ],
    'SECURITY': [
        {
            "TokenAuth": []
        }
    ],
    'COMPONENTS': {
        'securitySchemes': {
            "TokenAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
    
}


# AUTHENTICATION_BACKENDS = [
#     # ...他のバックエンドがあればここに追加...
#     'memos.authentication.EmailBackend',  # EmailBackendクラスへのパスを追加
# ]
