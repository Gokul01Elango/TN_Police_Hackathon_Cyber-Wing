import configparser
import json
import asyncio
from datetime import date, datetime
import tkinter as tk

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone, entity_id, count_limit):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    if entity_id.isdigit():
        entity = PeerChannel(int(entity_id))
    else:
        entity = entity_id

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0

    while True:
        print("Messages exported successfully")
        # print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if count_limit != 0 and total_messages >= count_limit:
            break

    with open('channel_messages.json', 'w') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder)

def get_input():
    entity_id = entity_id_entry.get()
    count_limit = int(count_limit_entry.get()) if count_limit_entry.get() else 0

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(phone, entity_id, count_limit))
    loop.close()

# Create the GUI
root = tk.Tk()
root.title("Telegram Channel Messages Downloader")

entity_id_label = tk.Label(root, text="Enter entity (telegram URL or entity id):")
entity_id_label.pack()

entity_id_entry = tk.Entry(root)
entity_id_entry.pack()

count_limit_label = tk.Label(root, text="Enter the maximum number of messages to download:")
count_limit_label.pack()

count_limit_entry = tk.Entry(root)
count_limit_entry.pack()

download_button = tk.Button(root, text="Download Messages", command=get_input)
download_button.pack()

root.mainloop()
