import os

from ..utils.config_load_helpers import load_config

CONFIG_PATH = os.getenv("CONFIG_PATH") or 'collatorx.config:settings-test.yaml'

def load_settings(context: str, target: str = 'settings', provider: str = 'base'):
    config = load_config(CONFIG_PATH)
    if context == 'providers':
        return config[target][context][provider]
    else:
        return config[target][context]


class Provider():

    PROVIDER_ID = 'base'

    def __init__(self, config_path: str = CONFIG_PATH):
        self._settings = {}

        self._load_settings()
        # self._load_provider_settings()

    @property
    def settings(self):
        return self._settings

    def _load_settings(self, context: str = 'providers'):
        config = load_settings(context, provider=self.PROVIDER_ID)

        if config:

            if "credentials" in config:
                self._settings = config["credentials"] 
            else:
                self._settings = config

            if "api_url" in config:
                self._settings["api_url"] = config["api_url"]

        else:
            return Exception("Error while loading provider settings, configurations:",config)

        return self._settings
