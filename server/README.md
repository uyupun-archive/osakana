# サーバ

- サーバはFastAPIで構築されており、主にREST APIの提供とMeilisearchの操作を行う

## 環境構築

```bash
$ cd server

$ cp .env.example .env

$ pipenv install --dev

# cchardetのインストールに失敗する場合は以下を実行し、再度 `pipenv install` を実行する
$ pip install --upgrade Cython

$ pipenv shell

# FastAPIの起動
$ python main.py

# DBマイグレーションの実行
$ python -m db.migrations.run 01 up

# DBマイグレーションのロールバック
$ python -m db.migrations.run 01 down

# Redocを開く
$ open http://localhost:8000/redoc

# タイトルを取得するスクレイピングの実行(検証用途)
$ python -m lib.web_scraping <url>

# リンター、フォーマッタの実行
$ pipenv run flake8 .
$ pipenv run black .
$ pipenv run isort .
```
