import sys

from db.migrations.base import BaseMigrator
from db.migrations._01_create_reading_list_collection import CreateReadingListCollectionMigrator


class MigratorExecutor:
    def __init__(self) -> None:
        create_reading_list_collection_migrator = CreateReadingListCollectionMigrator()
        self._migrators = [{
            "name": create_reading_list_collection_migrator.get_name(),
            "instance": create_reading_list_collection_migrator,
        }]

    def _find_migrator(self, migration_id: str) -> BaseMigrator:
        migrator = [
            migrator["instance"] for migrator in self._migrators
            if migrator["name"].startswith(f"{migration_id}_")
        ]

        if len(migrator) == 1:
            return migrator[0]
        elif len(migrator) > 1:
            raise MigratorDuplicateError()
        else:
            raise MigratorNotFoundError()

    def exec_action(self, migration_id: str, action: str) -> None:
        migrator = self._find_migrator(migration_id=migration_id)

        if action == "up":
            migrator.up()
        elif action == "down":
            migrator.down()
        else:
            raise InvalidActionError()


class InvalidArgumentCountError(Exception):
    pass


class InvalidActionError(Exception):
    pass


class MigratorNotFoundError(Exception):
    pass


class MigratorDuplicateError(Exception):
    pass


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise InvalidArgumentCountError()
    else:
        MigratorExecutor().exec_action(migration_id=sys.argv[1], action=sys.argv[2])
