from server_side.database_objects.column import Column
from server_side.database_objects.dbo import Dbo
from server_side.database_objects.index import Index
from server_side.database_objects.primary_key import PrimaryKey
from server_side.database_objects.foreign_key import ForeignKey
from server_side.database_objects.unique import Unique
from server_side.database_objects.check import Check
from server_side.interpreter.constraint_objects import (
    PrimaryKey as PrimaryKeyCObj,
    ForeignKey as ForeignKeyCObj,
    Unique as UniqueCObj,
    Check as CheckCObj,
    Identity as IdentityCObj,
    Default as DefaultCObj,
    NotNull as NotNullCObj
)


class Table(Dbo):
    def __init__(self,
                 name: str = "",
                 columns: list[Column] | None = None,
                 indexes: list[Index] | None = None,
                 primary_key: PrimaryKey | None = None,
                 foreign_keys: list[ForeignKey] | None = None,
                 unique_keys: list[Unique] | None = None,
                 checks: list[Check] | None = None
                 ):
        self.__name = name
        self.__columns = columns if columns else []
        self.__indexes = indexes if indexes else []
        self.__primary_key = primary_key if primary_key else None
        self.__foreign_keys = foreign_keys if foreign_keys else []
        self.__unique_keys = unique_keys if unique_keys else []
        self.__checks = checks if checks else []

    def __dict__(self) -> dict:
        return {
            "name": self.__name,
            "columns": [column.__dict__() for column in self.__columns],
            "indexes": [index.__dict__() for index in self.__indexes],
            "primary_key": self.__primary_key.__dict__() if self.__primary_key is not None else {},
            "foreign_keys": [fk.__dict__() for fk in self.__foreign_keys] if self.__foreign_keys else [],
            "unique_keys": [uk.__dict__() for uk in self.__unique_keys] if self.__unique_keys else [],
            "checks": [c.__dict__() for c in self.__checks] if self.__checks else []
        }

    def from_dict(self, data: dict) -> 'Table':
        self.__name = data.get("name", "")
        self.__columns = [Column().from_dict(column) for column in data.get("columns", [])]
        self.__indexes = [Index().from_dict(index) for index in data.get("indexes", [])]
        pk_dict = data.get("primary_key", {})
        self.__primary_key = PrimaryKey().from_dict(pk_dict) if pk_dict else None
        self.__foreign_keys = [ForeignKey().from_dict(fk) for fk in data.get("foreign_keys", [])]
        self.__unique_keys = [Unique().from_dict(uk) for uk in data.get("unique_keys", [])]
        return self

    def get_name(self) -> str:
        return self.__name

    def get_column(self, col_name):
        for col in self.__columns:
            if col.get_name() == col_name:
                return col
        raise ValueError(f"Column {col_name} not found")

    def exists_column(self, col_name):
        for col in self.__columns:
            if col.get_name() == col_name:
                return True
        return False

    def get_columns(self) -> list[Column]:
        return self.__columns

    def get_indexes(self) -> list[Index]:
        return self.__indexes

    def set_name(self, name: str):
        self.__name = name

    def set_columns(self, columns: list[Column]):
        self.__columns = columns

    def set_indexes(self, indexes: list[Index]):
        self.__indexes = indexes

    def add_column(self, column: Column):
        # TO-DO: check if the column already exists
        self.__columns.append(column)

    def add_index(self, index: Index):
        # TO-DO: check if the index already exists
        self.__indexes.append(index)

    def get_primary_key(self) -> PrimaryKey:
        return self.__primary_key

    def set_primary_key(self, primary_key: PrimaryKey):
        self.__primary_key = primary_key

    def get_column_names(self) -> list[str]:
        return [col.get_name() for col in self.__columns]

    def has_primary_key(self) -> bool:
        return self.__primary_key is not None

    def get_identity_column(self) -> Column | None:
        for col in self.__columns:
            if col.has_identity():
                return col
        return None

    def has_identity(self) -> bool:
        for col in self.__columns:
            if col.has_identity():
                return True
        return False

    def get_unique_keys(self) -> list:
        return self.__unique_keys

    def get_foreign_keys(self) -> list:
        return self.__foreign_keys

    def add_key(self, key):
        """
        Adds a key to the table.

        Note: Convert the key - constraint object (CObj) to a database object (Dbo) before adding it to the table.
        """
        if isinstance(key, PrimaryKeyCObj):
            self.__primary_key = PrimaryKey(key)
            # every column that is part of the primary key should not allow nulls
            for col_name in key.get_column_names():
                self.get_column(col_name).set_allow_nulls(False)
        elif isinstance(key, ForeignKeyCObj):
            self.__foreign_keys.append(ForeignKey(key))
        elif isinstance(key, UniqueCObj):
            self.__unique_keys.append(Unique(key))
        else:
            raise ValueError(f"Invalid key type: {type(key)}")

    def add_constraint(self, constraint):
        """
        Adds a constraint to the table or to the corresponding column.

        :param constraint: CObj object
        """

        if isinstance(constraint, NotNullCObj):
            col_name = constraint.get_column_name()
            self.get_column(col_name).set_allow_nulls(False)
        elif isinstance(constraint, DefaultCObj):
            col_name = constraint.get_column_name()
            self.get_column(col_name).set_default_value(constraint.get_default_value())
        elif isinstance(constraint, CheckCObj):
            self.__checks.append(Check(constraint))
        elif isinstance(constraint, IdentityCObj):
            col_name = constraint.get_col_name()
            self.get_column(col_name).set_identity(
                (constraint.get_seed(), constraint.get_increment())
            )
        else:
            raise ValueError(f"Invalid constraint type: {type(constraint)}")
