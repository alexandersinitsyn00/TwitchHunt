import asyncio
from EventManager import EventManager
from TwitchChatHandler import TwitchChatHandler
from SettingsManager import SettingsManager

event_manager = EventManager()
settings = SettingsManager('private_settings.json')

twitch_chat_session = TwitchChatHandler(user_name=settings.get_user_name(),
                                        access_token=settings.get_access_token())

channels_to_handle = settings.get_channels_to_hadnle()


async def run_events_manager():
    for channel in channels_to_handle:
        event_manager.add_task(twitch_chat_session.listen_chat, channel)
    await event_manager.handle()


if __name__ == '__main__':
    asyncio.run(run_events_manager())
