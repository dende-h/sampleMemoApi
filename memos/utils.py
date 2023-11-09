# rest_framework_simplejwtからRefreshTokenをインポートします。
from rest_framework_simplejwt.tokens import RefreshToken

# my_jwt_response_handler関数を定義します。
# この関数はJWTのカスタム応答を生成するために使用されます。
def my_jwt_response_handler(token, user=None, request=None):
    # 与えられたユーザーに対して新しいリフレッシュトークンを生成します。
    refresh = RefreshToken.for_user(user)
    
    # JWTトークン、リフレッシュトークン、ユーザー情報を含む辞書を返します。
    # リフレッシュトークンはアクセストークンを再発行するために使用されます。
    return {
        # リフレッシュトークンの文字列表現を'refresh'キーに設定します。
        'refresh': str(refresh),
        # アクセストークンの文字列表現を'access'キーに設定します。
        'access': str(refresh.access_token),
        # ユーザー情報を'user'キーに格納した辞書として返します。
        'user': {
            'id': user.id,              # ユーザーID
            'username': user.user_name, # ユーザー名
            'email': user.email,        # メールアドレス
        }
    }

