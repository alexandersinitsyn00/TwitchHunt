import re as regex
import websockets

users = {}


class TwitchChatHandler:
    def __init__(self, user_name, access_token):
        self.token = access_token
        self.user_name = user_name
        self.url_chat = 'ws://irc-ws.chat.twitch.tv:80'

    # TODO - нужно реализовать игру в пинг понг с сервером чтобы он не закрывал сокет
    #   Сервер присылает сообщение PING
    #     Нужно ответить PONG
    async def listen_chat(self, channel_name):
        async with websockets.connect(self.url_chat) as socket:
            await self.auth(socket, channel_name)
            while True:
                response_data = await socket.recv()
                msg = TwitchMessage(response_data)
                msg.print_with_channel(channel_name)

    async def auth(self, socket, channel_name):
        await socket.send(f'PASS oauth:{self.token}')
        await socket.send(f'NICK {self.user_name}')
        await socket.send(f'JOIN #{channel_name}')


class TwitchMessage:
    def __init__(self, socket_response):
        self.response = socket_response
        self.user_name = ''
        self.user_message = ''
        self.decode()

    def decode(self):
        if self.is_user_message():
            self.decode_user_message()
        else:
            self.decode_system_message()

    def is_user_message(self):
        return regex.search('tv\sPRIVMSG\s#\w+\s:', self.response) is not None

    def print_with_channel(self, channel_name):
        if len(self.user_message) > 0:
            print(f'{channel_name:>20} - {self.user_name:>20}: {self.user_message}')

    def decode_user_message(self):
        self.user_name = regex.search('^:(.+?)!', self.response).group(1)
        self.user_message = regex.search("^:.+?:(.*)", self.response).group(1)

    # TODO - корректный вывод системных сообщений Твича,в том числе и содержащих несколько строк
    def decode_system_message(self):
        print(self.response)
