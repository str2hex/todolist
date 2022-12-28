import requests

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse, GET_UPDATES_SCHEMA, SEND_MESSAGE_RESPONSE_SCHEMA


class TgClient:
    """Клиент телеграмм бота"""
    def __init__(self, token: str) -> None:
        self.token = token

    def get_url(self, method: str) -> str:
        """Передаём токен и метод"""
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """Получение введеных сообщений"""
        url = self.get_url("getUpdates")
        response = requests.get(url, params={"offset": offset, "timeout": timeout})
        return GET_UPDATES_SCHEMA.load(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """Отправка сообщения"""
        url = self.get_url("sendMessage")
        response = requests.get(url, params={"chat_id": chat_id, "text": text})
        return SEND_MESSAGE_RESPONSE_SCHEMA.load(response.json())
