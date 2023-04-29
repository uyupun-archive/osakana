from db.client import DBClient


def get_db_client():
    db_client = DBClient()
    return db_client
