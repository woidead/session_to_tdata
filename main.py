from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import asyncio



async def main(session):

    # Load the client from telethon.session file
    # We don't need to specify api, api_id or api_hash, it will use TelegramDesktop API by default.
    client = TelegramClient(session)
    
    # flag=UseCurrentSession
    #
    # Convert Telethon to TDesktop using the current session.
    tdesk = await client.ToTDesktop(flag=UseCurrentSession)
    
    # Save the session to a folder named "tdata"
    tdesk.SaveTData(session)

asyncio.run(main('sessions/telegram.session'))
