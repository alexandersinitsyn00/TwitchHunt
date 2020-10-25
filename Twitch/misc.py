from Settings.misc import settings
from Twitch.TwitchChatHandler import TwitchChatHandler

twitch_chat = TwitchChatHandler(settings.get_user_name(), settings.get_access_token(), settings.get_channels_to_hadnle())