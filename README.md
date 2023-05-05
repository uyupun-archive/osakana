# Osakana

- 自動タグ付け機能と検索機能を持つ「あとで読む」記事を管理できるWebアプリ

## 環境構築

```bash
$ cp .env.example .env
$ pipenv install
$ pipenv shell
# MeiliSearchの起動
$ docker compose up -d
# FastAPIの起動
$ python main.py
# ReDocを開く
$ open http://localhost:8000/redoc
# DBマイグレーションの実行
$ python -m db.migrations.run 01 up
$ python -m db.migrations.run 01 down
# MeiliSearchを開く
$ open http://localhost:7700/
```
