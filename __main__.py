import asyncio
from TwitchChatHandler import TwitchChatHandler
from SettingsManager import SettingsManager
from DataBaseEngine import DataBaseEngine

db = DataBaseEngine('C:\\Users\\asinitsyn\\Desktop\\test\\TwitchHunt\\db.db')
settings = SettingsManager('C:\\Users\\asinitsyn\\Desktop\\test\\TwitchHunt\\private_settings.json')
channels_to_handle = settings.get_channels_to_hadnle()

twitch_chat = TwitchChatHandler(user_name=settings.get_user_name(),
                                access_token=settings.get_access_token(),
                                channels=channels_to_handle)


async def run():
    async for msg in twitch_chat.handle():
        db.save_twitch_message(msg['channel'], msg['user'], msg['msg'])


if __name__ == '__main__':
    asyncio.run(run())
