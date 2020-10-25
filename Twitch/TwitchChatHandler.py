import re as regex
import websockets


class TwitchChatHandler:
    def __init__(self, user_name, access_token, channels=None):
        if channels is None:
            channels = []

        self.token = access_token
        self.user_name = user_name
        self.url_chat = 'ws://irc-ws.chat.twitch.tv:80'
        self.channel_names_to_listen = {is_listening: False for is_listening in channels}
        self.socket = None

    async def handle(self):
        async with websockets.connect(self.url_chat) as self.socket:
            await self.__auth__()
            await self.__joint_to_channel_list()
            while True:
                try:
                    response = await self.socket.recv()
                except websockets.ConnectionClosedError:
                    print("Network or Auth error!")
                    break
                msg = TwitchMessage(response)
                if msg.is_game():
                    await self.__play_game__()
                if msg.user_message:
                    yield {'channel': msg.channel, 'user': msg.user_name, 'msg': msg.user_message}

    async def __auth__(self):
        await self.socket.send(f'PASS oauth:{self.token}')
        await self.socket.send(f'NICK {self.user_name}')

    async def __joint_to_channel_list(self):
        for channel_name in self.channel_names_to_listen:
            await self.__join__(channel_name)

    async def add_channel(self, channel_name):
        self.channel_names_to_listen.setdefault(channel_name, False)
        await self.__join__(channel_name)

    async def remove_channel(self, channel_name):
        del self.channel_names_to_listen[channel_name]
        await self.__leave__(channel_name)

    async def __join__(self, channel):
        await self.socket.send(f'JOIN #{channel}')
        self.channel_names_to_listen[channel] = True

    async def __leave__(self, channel):
        await self.socket.send(f'PART #{channel}')

    async def __play_game__(self):
        print("PING - PONG")
        await self.socket.send('PONG')


class TwitchMessage:
    def __init__(self, response):
        self.response = response
        self.user_name = None
        self.user_message = None
        self.channel = None
        if self.is_user_message():
            self.__decode__()

    def is_user_message(self):
        return regex.search('tv\sPRIVMSG\s#\w+\s:', self.response) is not None

    def is_game(self):
        return regex.search('^PING', self.response) is not None

    def __decode__(self):
        self.user_name = regex.search('^:(.+?)!', self.response).group(1)
        self.user_message = regex.search("^:.+?:(.*)", self.response).group(1)
        self.channel = regex.search("^:.+?#(\\w*)", self.response).group(1)

    def print_user_message(self):
        print(f'{self.channel:>20} | {self.user_name:>20}: {self.user_message}')
