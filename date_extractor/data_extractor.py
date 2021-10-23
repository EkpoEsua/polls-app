"""Define class to handle execution of SQL queries from a file."""
from django.db import connection
from django.db.utils import IntegrityError, OperationalError


class SQLDataExecutor:

    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._insert_statements = list()
    
    def _extract_insert_statements(self) -> None:
        """Read file containing sql statements and load them into the statements attribute."""
        with open(self._filename, "rt") as f:
            for line in f:
                statement = str()
                if line.startswith("INSERT INTO"):
                    statement = line
                    current_line = line
                    while not(current_line.endswith(";\n")):
                        current_line = next(f)
                        statement += current_line
                    #do some cleanup to make sql statement sqlite compliant
                    statement = statement.replace("AUTO_INCREMENT", "AUTOINCREMENT")

                    self._insert_statements.append(statement)
                    

    def _clean_data(self):
        """Clean malformated datetime data i.e "0000-00-00 00:00:00" and replaces with fill in
        data "1111-11-11 11:11:11" """
        for index, statement in enumerate(self._insert_statements):
            self._insert_statements[index] = statement.replace(
                "0000-00-00 00:00:00",
                "1111-11-11 11:11:11"
            )

    def execute(self) -> None:
        self._extract_insert_statements()
        self._clean_data()

        with connection.cursor() as cursor:
            for statement in self._insert_statements:
                try:
                    cursor.execute(statement)
                except IntegrityError as e:
                    print("*"*100)
                    print("Integrity Error: ", e)
                    print()
                    print()
                    print(statement)
                    print("*"*100)
                    print()
                    print()
                except OperationalError as e:
                    print("*"*100)
                    print("Operational Error: ", e)
                    print()
                    print()
                    print(statement)
                    print("*"*100)
                    print()
                    print()

