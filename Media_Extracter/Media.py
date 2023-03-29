from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from tqdm import tqdm

api_id = 23368900
api_hash ='e633b0a3f68e71cb5e90b7f57faf95ed'


def download_media(group, cl, name):
    messages = cl.get_messages(group, limit=2000)

    for message in tqdm(messages):
        message.download_media('./' + name + '/')


with TelegramClient('Gokul', api_id, api_hash) as client:
    result = client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=500,
        hash=0,
    ))

    title = ''
    for chat in result.chats:
        print(chat)

        if chat.title == title:
            download_media(chat, client, title)

    title = 'TN_Police_Test_Channel'
    channel = client(GetFullChannelRequest(title))
    print(channel.full_chat)

    download_media(channel.full_chat, client, title)
