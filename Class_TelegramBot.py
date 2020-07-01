import requests


class TelegramBot:
    """
    Простейший класс Telegram бота
    """
    def __init__(self, bot_url, logger_, database=None):
        self.bot_url = bot_url
        self.logger = logger_
        self.database = database

    def get_text_updates(self, offset=0):
        """
        Get updates from Telegram
        :return: Dictionary Updates
        """
        params = {'timeout': 1, 'offset': offset, 'limit': 1000, 'allowed_updates': ['message', 'edited_message']}
        response = requests.get(self.bot_url + '/getUpdates', data=params)
        self.logger.debug(response)
        self.logger.debug(response.json())
        if response.ok:
            self.logger.debug("get_updates_json OK")
            return True, response.json()
        else:
            self.logger.error(f"ERROR:{response.text}")
            return False, response.text

    def send_text_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.bot_url + '/sendMessage', data=params)
        self.logger.debug(response)
        if response.ok:
            self.logger.debug("get_updates_json ОК")
            return True, None
        else:
            self.logger.error(f"ERROR:{response.text}")
            return False, response.text
