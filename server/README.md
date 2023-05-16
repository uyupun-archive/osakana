# サーバ

- サーバはFastAPIで構築されており、主にREST APIの提供とMeilisearchの操作を行う

## 環境構築

```bash
$ cp .env.example .env

$ pipenv install

# cchardetのインストールに失敗する場合は以下を実行
$ pip install --upgrade Cython

$ pipenv shell

# FastAPIの起動
$ python main.py

# DBマイグレーションの実行
$ python -m db.migrations.run 01 up
$ python -m db.migrations.run 01 down

# ReDocを開く
$ open http://localhost:8000/redoc

# タイトルを取得するスクレイピングの実行(検証用途)
$ python -m lib.scraper <url>
```
