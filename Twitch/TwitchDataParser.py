import asyncio
import aiohttp
import json
import datetime
import pytz

AUTH_TOKEN_VALIDATE_BASE_URL = 'https://id.twitch.tv/oauth2/validate'
STREAM_BASE_URL = 'https://api.twitch.tv/helix/streams'
CHANNEL_SEARCH_BASE_URL = 'https://api.twitch.tv/helix/search/channels'
TOKEN = 'fmw74lryx24be48sjcjvwwtlgsn8ke'
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'


async def is_valid_auth_token(token):
    headers = {'Authorization': f'Bearer {token}'}
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', AUTH_TOKEN_VALIDATE_BASE_URL, headers=headers) as resp:
            return resp.status == 200


async def is_valid_channel(channel_name):
    headers = {'Authorization': f'Bearer {TOKEN}',
               'Client-Id': f'{CLIENT_ID}'}
    params = {'query': channel_name}
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', CHANNEL_SEARCH_BASE_URL, params=params, headers=headers) as resp:
            data = await resp.json()
            try:
                validate_to_channel = data["data"][0]["display_name"]
                return channel_name == validate_to_channel
            except IndexError:
                return False


async def get_stream_info_for_channel_if_streaming(channel_name):
    headers = {'Authorization': f'Bearer {TOKEN}',
               'Client-Id': f'{CLIENT_ID}'}
    params = {'user_login': channel_name}
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', STREAM_BASE_URL, params=params, headers=headers) as resp:
            data = await resp.json()
            try:
                info = data["data"][0]
            except IndexError:
                return None
            except KeyError:
                return None

            utc_started_at = pytz.utc.localize(datetime.datetime.strptime(info['started_at'], '%Y-%m-%dT%H:%M:%SZ'))
            moscow_timezone = pytz.timezone('Europe/Moscow')
            moscow_started_at = utc_started_at.astimezone(moscow_timezone)

            return {'stream_id': info['id'],
                    'channel_name': info['user_name'],
                    'game_id': info['game_id'],
                    'viewer_count': info['viewer_count'],
                    'datetime_create': moscow_started_at}
