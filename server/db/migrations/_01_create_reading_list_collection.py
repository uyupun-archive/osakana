from typing import Type

from db.migrations.base import BaseMigrator
from db.models.reading_list import ReadingListRecord


class CreateReadingListCollectionMigrator(BaseMigrator):
    def __init__(self, reading_list_record: Type[ReadingListRecord]=ReadingListRecord) -> None:
        super().__init__()
        self._name = "01_create_reading_list_collection"
        self._reading_list_record = reading_list_record
        self._index_name = self._reading_list_record.get_name()

    def get_name(self) -> str:
        return self._name

    def up(self) -> None:
        self._db_client.create_index(index_name=self._index_name)

        created_at = self._reading_list_record.has_field(field="created_at")
        updated_at = self._reading_list_record.has_field(field="updated_at")
        self._db_client.sortable(index_name=self._index_name, attributes=[created_at, updated_at])

        is_bookmarked = self._reading_list_record.has_field(field="is_bookmarked")
        is_read = self._reading_list_record.has_field(field="is_read")
        self._db_client.filterable(index_name=self._index_name, attributes=[is_bookmarked, is_read])

    def down(self) -> None:
        self._db_client.delete_index(index_name=self._index_name)
