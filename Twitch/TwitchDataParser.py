import asyncio
import aiohttp
import json

# print(json.dumps(data, sort_keys=True, indent=4))

AUTH_TOKEN_VALIDATE_BASE_URL = 'https://id.twitch.tv/oauth2/validate'
STREAM_BASE_URL = 'https://api.twitch.tv/helix/streams'
TOKEN = 'fmw74lryx24be48sjcjvwwtlgsn8ke'
CLIENT_ID = 'gp762nuuoqcoxypju8c569th9wz7q5'


async def is_valid_auth_token(token):
    headers = {'Authorization': f'Bearer {token}'}
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', AUTH_TOKEN_VALIDATE_BASE_URL, headers=headers) as resp:
            return resp.status == 200


async def get_stream_info_for_channel(channel_name):
    headers = {'Authorization': f'Bearer {TOKEN}',
               'Client-Id': f'{CLIENT_ID}'}
    params = {'user_login': channel_name}
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', STREAM_BASE_URL, params=params, headers=headers) as resp:
            data = await resp.json()
            info = data["data"][0]
            if not info:
                return None
            return {'game_id': info["game_id"],
                    'language': info["language"],
                    'title': info["title"],
                    'viewer_count': info["viewer_count"]
                    }


async def caller():
    print(await is_valid_auth_token('fmw74lryx24be48sjcjvwwtlgsn8ke'))
    print(await get_stream_info_for_channel('roflo_chelik'))
    print(await get_stream_info_for_channel('bratishkinoff'))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(caller())
