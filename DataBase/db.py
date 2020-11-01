from os import environ
from .Engine import *

root_path = environ.get("ROOT_DIR")
db_relative_path = environ.get("DB_RELATIVE_PATH")

db_full_path = f'{root_path}{db_relative_path}'

db = DbEngine(db_full_path)
