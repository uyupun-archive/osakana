# サーバ

- サーバはFastAPIで構築されており、主にREST APIの提供とMeilisearchの操作を行う

## 環境構築

```bash
$ cd server

$ cp .env.example .env

# `server/.env` の以下の項目を変更する
$ cat server/.env
...
+ MS_ADDRESS=engine
- MS_ADDRESS=localhost
...

$ poetry install --sync

# Pyrightのインストール
$ npm install

$ poetry shell

# FastAPIの起動
$ python main.py

# DBマイグレーションの実行
$ python -m db.migrations.run 01 up

# DBマイグレーションのロールバック
$ python -m db.migrations.run 01 down

# Redocを開く
$ open http://localhost:8000/redoc

# タイトルを取得するスクレイピングの実行(検証用途)
$ python -m services.web_scraping <url>

# n-gramの実行(検証用途)
$ python -m services.ngrams <title>

# 形態素解析の実行(検証用途)
$ python -m services.morphological_analysis <title>

# リンター、フォーマッタの実行
$ poetry run flake8 .
$ poetry run black .
$ poetry run isort .
$ npm run pyright .
```
