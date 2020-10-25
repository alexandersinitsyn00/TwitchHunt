import json


class SettingsManager:
    def __init__(self, file_path='private_settings.json'):
        self.file_path = file_path
        self.settings = {}
        self.read_settings()

    def read_settings(self):
        with open(self.file_path) as file:
            self.settings = json.load(file)

    def get_user_name(self):
        return self.settings["user_name"]

    def get_access_token(self):
        return self.settings["access_token"]

    def get_channels_to_hadnle(self):
        return self.settings["channels_to_handle"]

    def get_database_path(self):
        return self.settings["database_path"]

    def get_settings(self):
        return self.settings


if __name__ == '__main__':
    settings = SettingsManager('../Data/private_settings.json')
    print(settings.get_user_name())
