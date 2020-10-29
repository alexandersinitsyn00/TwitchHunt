from Settings.misc import settings
from DataBaseManager.DataBaseEngine import DataBaseEngine
db = DataBaseEngine()

# Инициализация БД
db.setup(settings.get_database_path())

if __name__ == '__main__':
    print(db.VIEW_VIEWERS_COUNT_PER_MINUTE_FOR_CHANNEL('buster'))