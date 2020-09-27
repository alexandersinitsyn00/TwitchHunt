###############################################################################
###############################################################################
###############################################################################

# TODO - проанализировать TwitchApi ( прочитать документацию ) и понять,
#   какие данные можно вытащить и что с ними можно сделать

# TODO - полностью переписать код и сделать его асинхронным
#   В Будущем добавить возможность мультисессий от разных пользователей


###############################################################################
###############################################################################
###############################################################################
import requests as req
import webbrowser


class TwitchClient:
    def __init__(self):
        self.id = '1boo9kzohq8onmja6umzwnuiz9itx5'
        self.params = {
            "response_type": "token",
            "client_id": '1boo9kzohq8onmja6umzwnuiz9itx5',
            "redirect_url": "http://localhost",
            "scope": "chat:read chat:edit"
        }
        self.access_token = 'k49zh9f0zudgyveskhbbhoy460omg0'
        self.redirect_url = 'http://localhost'
        self.authentication_url = 'https://id.twitch.tv/oauth2/authorize'

    def authentificate(self):
        r = req.get(
            f"https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={self.id}&redirect_uri={self.redirect_url}&scope={self.params['scope']}")
        webbrowser.open(r.url)
        print('Input access token: ')
        input(self.access_token)
        print(f'ACCESS TOKEN: {self.access_token}')

    def get_top_games(self):
        r = req.session()
        r.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": f"{self.id}"
        }
        data = r.get('https://api.twitch.tv/helix/games/top')
        return data.json()

    def search_games_categories(self, s_string):
        r = req.session()
        r.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": f"{self.id}"
        }
        data = r.get(f'https://api.twitch.tv/helix/search/categories?query={s_string}')
        return data.json()

    def search_channel(self, s_string):
        r = req.session()
        r.params = {
            "query": s_string,
        }
        r.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": f"{self.id}"
        }
        data = r.get('https://api.twitch.tv/helix/search/channels')
        return data.json()

    def get_current_streams(self):
        r = req.session()
        r.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": f"{self.id}"
        }
        data = r.get('https://api.twitch.tv/helix/streams')
        return data.json()

    def get_channel_info(self, channel_id):
        r = req.session()
        r.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Client-Id": f"{self.id}"
        }
        r.params = {
            "broadcaster_id": channel_id,
        }
        data = r.get('https://api.twitch.tv/helix/channels')
        return data.json()
