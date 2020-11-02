from os import environ
from Twitch.TwitchChatHandler import TwitchChatHandler

tw_user_name = environ.get("TWITCH_USER_NAME")
tw_token = environ.get("TWITCH_ACCESS_TOKEN")

twitch_chat = TwitchChatHandler(tw_user_name, tw_token, None)
