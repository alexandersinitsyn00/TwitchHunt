from os import environ
from pathlib import Path
from .Engine import *

db_full_path = Path.cwd() / environ.get("DATA_DIR") / "db.db"

db = DbEngine(db_full_path)
