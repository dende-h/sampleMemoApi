import pytest
import environ 
import testinfra

env = environ.Env()
env.read_env('.env')


inventory_file = "./ansible/inventories/hosts"

# Testinfraを使用してホストを指定（もしEC2_HOSTが未設定ならローカルホストを使用）
@pytest.fixture(scope="module")
def host(request):
    return testinfra.get_host(f"ansible://{inventory_file}?ansible_inventory={inventory_file}")

# 各種パッケージがインストールされているかを確認するテスト
@pytest.mark.parametrize("pkg", [
    "python3", "python3-pip", "git", "python3-venv", "pkg-config", 
    "default-libmysqlclient-dev", "nginx"
])
def test_package_installed(host, pkg):
    package = host.package(pkg)
    assert package.is_installed  # パッケージがインストールされていることを確認

# Gunicornのsystemdサービスが実行中かつ有効になっているかを確認するテスト
def test_gunicorn_service(host):
    gunicorn = host.service("gunicorn")
    assert gunicorn.is_running  # Gunicornが実行中であることを確認
    assert gunicorn.is_enabled  # Gunicornが有効になっていることを確認

# Nginxサービスが実行中かを確認するテスト
def test_nginx_running(host):
    nginx = host.service("nginx")
    assert nginx.is_running  # Nginxが実行中であることを確認

# Nginxの設定ファイルが適切に配置されているかを確認するテスト
def test_nginx_config_exists(host):
    nginx_config = host.file("/etc/nginx/sites-available/sampleApi.conf")
    assert nginx_config.exists  # Nginx設定ファイルが存在することを確認
    assert nginx_config.is_symlink  # シンボリックリンクであることを確認
    assert nginx_config.linked_to == "/etc/nginx/sites-enabled/sampleApi.conf"  # 正しい場所にリンクされていることを確認

# プロジェクトディレクトリが存在するかを確認するテスト
def test_project_directory(host):
    project_dir = host.file("/sampleMemoApi")
    assert project_dir.exists  # プロジェクトディレクトリが存在することを確認
    assert project_dir.is_directory  # ディレクトリであることを確認

# データベースへの接続が可能かを確認するテスト
def test_database_connection(host):
    db_host = env('DB_HOST')
    assert host.run(f"nc -zv {db_host} 3306").rc == 0  # データベースへの接続が可能であることを確認