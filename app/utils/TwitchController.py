import asyncio
from DataBase import *
from DataBase.Engine import Exceptions as DbExceptions
from Twitch import twitch_chat
from Twitch.TwitchDataParser import get_stream_info_for_channel_if_streaming


async def control_tw_chat():
    await asyncio.sleep(5)
    while True:
        actions_list = db.get_tasks_from_channel_actions_deque()
        for action in actions_list:
            acton_id = action[0]
            action_name = action[1]
            channel_name = action[2]
            await process_action(action_name, channel_name)
            db.remove_task_from_channel_actions_deque(acton_id)

        await asyncio.sleep(5)


async def process_action(action, channel):
    if action == 'JOIN':
        await twitch_chat.add_channel(channel)
    if action == 'LEAVE':
        await twitch_chat.remove_channel(channel)


async def save_twitch_message():
    async for msg in twitch_chat.handle():
        channel_name = msg["channel"]
        user_name = msg["user"]
        msg = msg["msg"]

        try:
            db.add_twitch_message(channel_name, user_name, msg)
        except DbExceptions.TwStreamNotFound:
            stream_info = await get_stream_info_for_channel_if_streaming(channel_name)
            if stream_info:
                db.add_tw_stream(stream_info)
                db.add_twitch_message(channel_name, user_name, msg)


async def save_stream_info():
    while True:
        listening_channels = db.get_listening_channels()
        for channel in listening_channels:
            stream_info = await get_stream_info_for_channel_if_streaming(channel)
            if stream_info:
                db.add_tw_stream_info(stream_info)
        await asyncio.sleep(60)


async def handle_new_streams_by_channel():
    while True:
        listening_channels = db.get_listening_channels()
        for channel in listening_channels:
            stream_info = await get_stream_info_for_channel_if_streaming(channel)
            if stream_info:
                db.add_tw_stream(stream_info)
        await asyncio.sleep(600)


def add_twitch_tasks_to_event_loop(loop):
    loop.create_task(handle_new_streams_by_channel())
    loop.create_task(save_stream_info())
    loop.create_task(save_twitch_message())
    loop.create_task(control_tw_chat())
