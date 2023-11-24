プロジェクトルートに移動
cd /sampleMemoApi/
仮想環境へ入る
source venv/bin/activate
maigrateコマンド
python manage.py migrate
nginxのデフォルト設定のシンボリックリンクを削除
sudo rm /etc/nginx/sites-enabled/default
新しいマイグレーションを作成する
python manage.py makemigrations
migrationsディレクトリにadminユーザーから書き込める権限を付与
sudo chown -R $(whoami) /sampleMemoApi/memos/migrations/
仮想環境から離れる
deactivate
静的ファイルをstaticfilesディレクトリに集める
python manage.py collectstatic
nginxのエラーログ確認
tail -F /var/log/nginx/error.log
tail:

tail コマンドは、テキストファイルの末尾の内容を表示するために使用されます。デフォルトでは、ファイルの最後の10行を表示します。
-F オプション:

このオプションは、ファイルがローテート（古いログファイルが新しいファイルに置き換えられるプロセス）されても追跡を続けるようにtailに指示します。つまり、ファイルが削除されて新しいファイルが同じ名前で作成された場合でも、新しいファイルの内容を続けて表示します。
この振る舞いは、特にログファイルを扱う際に役立ちます。ログファイルは定期的にローテートされることが一般的で、-F オプションは新しいログファイルへの移行を透過的に扱うことができます。