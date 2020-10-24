import asyncio
from Twitch.TwitchChatHandler import TwitchChatHandler
from Settings.SettingsManager import SettingsManager
from DataBaseManager.DataBaseEngine import DataBaseEngine

# Файл с настройками
settings = SettingsManager('C:/Users/asinitsyn/Desktop/test/Settings/private_settings.json')

# Каналы, которые которые прослушиваются по умолчанию
channels_to_handle = settings.get_channels_to_hadnle()

# Инициализация БД
db = DataBaseEngine(settings.get_database_path())

# Обьект для получения сообщений с Твича
twitch_chat = TwitchChatHandler(user_name=settings.get_user_name(),
                                access_token=settings.get_access_token(),
                                channels=channels_to_handle)


# Получение сообщений и сохранение в БД
async def run():
    async for msg in twitch_chat.handle():
        db.save_twitch_message(msg['channel'], msg['user'], msg['msg'])


if __name__ == '__main__':
    asyncio.run(run())
