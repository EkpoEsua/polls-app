"""Loads database with SQL statements defined in a file."""
# Setup django
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elections.settings")
django.setup()

from date_extractor.data_extractor import SQLDataExecutor

if __name__ == "__main__":
    executor = SQLDataExecutor("test.sql")
    executor.execute()
