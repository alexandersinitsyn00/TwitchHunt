from Settings.misc import settings
from DataBaseManager.DataBaseEngine import DataBaseEngine
db = DataBaseEngine()

# Инициализация БД
db.setup(settings.get_database_path())
