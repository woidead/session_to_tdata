from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import asyncio
import os
import logging
import requests
import socks
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def main(session_name, proxy_index):
    
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
