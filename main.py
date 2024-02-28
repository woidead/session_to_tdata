from threading import Thread
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession
import asyncio
import os
import logging
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



async def main(session_name):
    
    session_path = os.path.join(os.path.join('sessions', session_name, f"{session_name}.session"))
    api = API.TelegramDesktop.Generate()
    client = TelegramClient(session_path, api)

    tdesk = await client.ToTDesktop(flag=UseCurrentSession, api=api)
    
    tdesk.SaveTData(os.path.join('tdatas', f"tdata{session_name.split('.')[0]}"))

def start_func(session_name):
    asyncio.run(main(session_name))

def rename_dirs():
    directory_path = 'tdatas'

    files = os.listdir(directory_path)

    files.sort()

    for index, file_name in enumerate(files, start=1):
        new_file_name = f"tdata{index}"
        old_file_path = os.path.join(directory_path, file_name)
        new_file_path = os.path.join(directory_path, new_file_name)
        os.rename(old_file_path, new_file_path)
        print(f"Файл {file_name} был переименован в {new_file_name}")
    

def start():
    session_names = os.listdir("./sessions")
    for session_name in session_names:
        logging.info(f'Начал {session_name}')
        t = Thread(
                target=start_func,
                args=(
                    session_name,
                ),
            )
        t.start()
        time.sleep(1)
        logging.info(f'Закончил {session_name}')
    
start()