# Osakana

<img src="./images/logo.png" width="500">

「あとで読む」記事を管理できるWebアプリ

## ユーザガイド

ユーザとして利用する場合、DockerとDocker Composeによる構築を推奨します。

```bash
# Dockerネットワークの作成
$ make network

# Dockerイメージのビルド
$ make build

# Dockerコンテナの起動
$ make up

# Dockerコンテナの停止
$ make down
```

## 開発者ガイド

開発者として利用する場合、以下のドキュメントに従ってホストマシン上に直接構築することを推奨します。

- [全文検索エンジン(Meilisearch)](./engine/README.md)
- [サーバ(FastAPI)](./server/README.md)
- [ダッシュボード(Vite + preact-ts)](./dashboard/README.md)
