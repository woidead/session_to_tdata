from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import asyncio
import os
import logging
import requests
import socks
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class Proxy:
    """Класс для работы с прокси-серверами.

    Позволяет получать адрес и порт прокси-сервера для использования в сетевых запросах.
    Поддерживает три режима работы:
    - Через загрузку списка прокси из URL (proxy_type == 0)
    - Через чтение списка прокси из файла (proxy_type == 1)
    - Без использования прокси (proxy_type == 2)

    Attributes:
        proxy_type (int): Тип использования прокси.
        proxy_file (str): Путь к файлу с прокси или URL.

    Methods:
        get_proxy(index): Возвращает параметры прокси-сервера в зависимости от типа.
    """

    def __init__(self, proxy_type:int):
        self.proxy_type = int(proxy_type)
        self.proxy_file = self.get_proxy_file()

    def get_proxy_file(self):
        with open("proxy.txt", 'r') as proxy_data:
            proxy_file = proxy_data.read().strip()
            return proxy_file

    def fetch_proxy_from_link(self, link, index):
        proxies = requests.get(link)
        proxy = proxies.text.split("\n")[index].split(":")
        addr = proxy[0]
        port = proxy[1]
        try:
            login = proxy[2]
            password = proxy[3]
            return addr, int(port), login, password
        except:
            return addr, int(port)
    
    def fetch_proxy_from_file(self, index):
        proxies = self.proxy_file.split("\n")
        proxy = proxies[index].split(":")
        addr = proxy[0]
        port = proxy[1]
        try:
            login = proxy[2]
            password = proxy[3]
            return addr, int(port), login, password
        except:
            return addr, int(port)
    
    def get_proxy(self, index:int):
        """Возвращает параметры прокси-сервера по заданному индексу.

        Args:
            index (int): Индекс прокси-сервера в списке.

        Returns:
            tuple: Параметры прокси-сервера (адрес, порт). Возвращает пустые строки, если прокси не используется.
        """
        if self.proxy_type == 0:
            return self.fetch_proxy_from_link(self.proxy_file, index)
        
        if self.proxy_type == 1:
            return self.fetch_proxy_from_file(index)
        
        else:
            logging.warning("Авторизация без прокси")
            return "", ""




async def main(session_name, proxy_index):
    proxy = Proxy(0)
    proxy.get_proxy(proxy_index)
    if len(proxy.get_proxy(proxy_index)) == 4:
        addr, port, username, password = proxy.get_proxy(proxy_index)
        proxy_conn = (socks.SOCKS5, addr, int(port), True, username, password)
        logging.info(f"{session_name} | Прокси: {addr}:{port}:{username}:{password}")
    else:
        addr, port = proxy.get_proxy(proxy_index)
        proxy_conn = (socks.SOCKS5, addr, int(port), True)
        logging.info(f"{session_name} | Прокси: {addr}:{port}")


    # Load the client from telethon.session file
    # We don't need to specify api, api_id or api_hash, it will use TelegramDesktop API by default.
    session_path = os.path.join('sessions', session_name)
    api = API.TelegramDesktop.Generate()
    client = TelegramClient(session_path)
    
    # flag=UseCurrentSession
    # Convert Telethon to TDesktop using the current session.
    tdesk = await client.ToTDesktop(flag=UseCurrentSession, )
    
    # Save the session to a folder named "tdata"
    tdesk.SaveTData(session_name)

asyncio.run(main('telegram.session'))
