from Settings.misc import settings
from Twitch.TwitchChatHandler import TwitchChatHandler
from DataBaseManager.misc import db

twitch_chat = TwitchChatHandler(settings.get_user_name(), settings.get_access_token(), db.get_list_of_listening_channels())
