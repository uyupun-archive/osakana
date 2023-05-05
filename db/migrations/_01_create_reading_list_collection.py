from db.migrations.base import BaseMigrator


class CreateReadingListCollectionMigrator(BaseMigrator):
    def __init__(self) -> None:
        super().__init__()
        self._name = "01_create_reading_list_collection"
        self._index_name = "reading_list"

    def get_name(self) -> str:
        return self._name

    def up(self) -> None:
        self._db_client.create_index(index_name=self._index_name)
        self._db_client.sortable(index_name=self._index_name, attribute="updated_at")

    def down(self) -> None:
        self._db_client.delete_index(index_name=self._index_name)
