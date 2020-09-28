import asyncio
from EventManager import EventManager
from TwitchChatHandler import TwitchChatHandler
from SettingsManager import SettingsManager

event_manager = EventManager()

settings = SettingsManager('private_settings.json')
channels_to_handle = settings.get_channels_to_hadnle()

twitch_chat = TwitchChatHandler(user_name=settings.get_user_name(),
                                access_token=settings.get_access_token(),
                                channels=channels_to_handle)

twitch_chats = [twitch_chat]


# Проверка
async def control_test():
    count = 0
    while True:
        await asyncio.sleep(1)
        count = count + 1
        if count == 5:
            try:
                await twitch_chat.remove_channel('evelone192')
            except:
                print("You was not subscribed to channel")
        if count == 10:
            try:
                await twitch_chat.remove_channel('nickmercs')
            except:
                print("You was not subscribed to channel")
        if count == 15:
            await twitch_chat.add_channel('kendinemuzisyen')


async def run_events_manager():
    for chat in twitch_chats:
        event_manager.add_task(chat.handle)
    event_manager.add_task(control_test)
    await event_manager.handle()


if __name__ == '__main__':
    asyncio.run(run_events_manager())
