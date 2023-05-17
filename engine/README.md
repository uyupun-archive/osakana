# 全文検索エンジン

- 全文検索エンジンにはMeilisearchを使用しており、主にデータの保存と検索を行う

## 環境構築

```bash
$ cd engine

$ cp .env.example .env

# MeiliSearchの起動
$ docker compose up -d

# MeiliSearchを開く
$ open http://localhost:7700/

# MeiliSearchの状態確認
$ docker compose ps

# MeiliSearchの終了
$ docker compose down
```
