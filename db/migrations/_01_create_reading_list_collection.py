from db.migrations.base import BaseMigrator


class CreateReadingListCollectionMigrator(BaseMigrator):
    def __init__(self) -> None:
        super().__init__()
        self._name = "01_create_reading_list_collection"
        self._collection_name = "reading_list"

    def get_name(self):
        return self._name

    def up(self) -> None:
        self._db_client.create_search_index(collection_name=self._collection_name, field_names=["url", "title"])
        self._db_client.create_unique_constraints(collection_name=self._collection_name, field_names=["url"])

    def down(self) -> None:
        pass
