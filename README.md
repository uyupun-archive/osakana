# Osakana

<img src="./images/logo.png" width="500">

「あとで読む」記事を管理できるWebアプリ

## ユーザガイド

ユーザとして利用する場合、DockerとDocker Composeによる構築を推奨します。

```bash
# `server/.env` の以下の項目を変更する
$ cat server/.env
...
+ API_ADDRESS=0.0.0.0
- API_ADDRESS=127.0.0.1
...
+ MS_ADDRESS=engine
- MS_ADDRESS=localhost
...

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

開発者として利用する場合、設定変更の容易であることやホットリロードを利用できる等の理由から、以下のドキュメントに従ってホストマシン上に直接構築することを推奨します。

- [全文検索エンジン(Meilisearch)](./engine/README.md)
- [サーバ(FastAPI)](./server/README.md)
- [ダッシュボード(Vite + preact-ts)](./dashboard/README.md)

## アーキテクチャ

<img src="./images/architecture.png" width="800">

## ディレクトリ構造

ディレクトリ構造の抜粋

```bash
.
├── Makefile                    # Docker Compose関連のスクリプト
├── README.md       
├── dashboard
│   ├── .env                    # 環境変数
│   ├── .env.example            # 環境変数の例
│   ├── .gitignore
│   ├── .node-version           # nodenvが求めるNode.jsのバージョン
│   ├── Dockerfile
│   ├── README.md
│   ├── compose.yml
│   ├── default.conf.template   # Dockerfileから使用されるnginxの設定
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   ├── src
│   │   ├── api
│   │   │   ├── endpoints       # APIとの通信処理
│   │   │   ├── errors          # APIとの通信で固有に発生するエラーの定義
│   │   │   └── types           # APIとの通信で固有に使用する型定義
│   │   ├── assets
│   │   ├── errors              # ダッシュボード全体で使用されるエラーの定義
│   │   ├── index.css
│   │   ├── main.tsx
│   │   ├── pages               # 各ページの定義
│   │   ├── types               # ダッシュボード全体で使用される型定義
│   │   └── vite-env.d.ts
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts          # ダッシュボード全体の設定
├── engine
│   ├── .env                    # 環境変数
│   ├── .env.example            # 環境変数の例
│   ├── .gitignore
│   ├── README.md
│   ├── compose.yml
│   └── data                    # Meilisearchが保持するデータ
├── images                      # ドキュメントで利用する画像
└── server
    ├── .env                    # 環境変数
    ├── .env.example            # 環境変数の例
    ├── .gitignore
    ├── Dockerfile
    ├── Pipfile
    ├── Pipfile.lock
    ├── README.md
    ├── api
    │   ├── routes              # APIのルーティング
    │   └── schemas             # APIのスキーマ
    ├── compose.yml
    ├── db
    │   ├── __init__.py
    │   ├── client.py           # Meilisearchのクライアント
    │   ├── migrations          # DBマイグレーション
    │   ├── models              # データモデル
    │   ├── repos               # リポジトリ
    │   └── settings.py         # Meilisearchの設定
    ├── errors
    │   ├── handlers.py         # エラーハンドラ
    │   └── responses.py        # エラーのレスポンスの定義
    ├── lib
    │   ├── scraper.py          # Webスクレイピング関連の処理
    │   └── timezone.py         # タイムゾーン関連の処理
    ├── main.py                 # APIのエントリポイント
    └── settings.py             # API全体の設定
```
