# Osakana

- 自動タグ付け機能と検索機能を持つ「あとで読む」記事を管理できるWebアプリ

## 環境構築

```bash
$ pipenv install
$ pipenv shell
$ python labeler.py
$ python scraper.py
$ docker compose up -d
$ uvicorn main:app --reload
$ open http://localhost:8000/redoc
```

## MongoDBの操作

```bash
$ brew tap mongodb/brew
$ brew update
$ brew install mongodb-community@6.0
$ mongosh mongodb://localhost:27017 -u root -p password
> show dbs
> use my_db
> show collections
> db.my_collection.find({name: "John Doe"})
[
  {
    _id: ObjectId("644b9fb9fd7ead2e1edf2154"),
    name: 'John Doe',
    age: 30,
    city: 'New York'
  }
]
```
