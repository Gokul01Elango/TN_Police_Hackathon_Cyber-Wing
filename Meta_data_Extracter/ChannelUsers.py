import configparser
import json
import asyncio
import tkinter as tk
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import PeerChannel

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

# Create the client
client = TelegramClient('session_name', api_id, api_hash)

# Define GUI
def fetch_participants():
    async def main():
        phone = phone_entry.get()
        await client.start()
        print("Client Created")
        # Ensure you're authorizedG
        if await client.is_user_authorized() == False:
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        me = await client.get_me()

        entity_id = channel_entry.get()
        if entity_id.isdigit():
            entity = PeerChannel(int(entity_id))
        else:
            entity = entity_id

        my_channel = await client.get_entity(entity)

        offset = 0
        limit = 100
        all_participants = []

        while True:
            participants = await client(GetParticipantsRequest(
                my_channel, ChannelParticipantsSearch(''), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            all_participants.extend(participants.users)
            offset += len(participants.users)

        all_user_details = []
        for participant in all_participants:
            all_user_details.append(
                {"id": participant.id, "first_name": participant.first_name, "last_name": participant.last_name,
                 "user": participant.username, "phone": participant.phone, "is_bot": participant.bot})

        with open('user_data.json', 'w') as outfile:
            json.dump(all_user_details, outfile)

        # Create a new window to display the fetched data
        display_window = tk.Toplevel()
        display_window.title("Fetched Participants")
        display_window.geometry("600x400")

        # Create a Listbox widget to display the fetched data
        participants_list = tk.Listbox(display_window, width=80)
        participants_list.pack()

        # Insert the fetched data into the Listbox widget
        for participant in all_user_details:
            participant_details = f"{participant['id']}: {participant['first_name']} {participant['last_name']} (@{participant['user']})"
            participants_list.insert(tk.END, participant_details)

    with client:
        client.loop.run_until_complete(main())

# Create GUI window
window = tk.Tk()
window.title("Telegram Channel Participant Fetcher")
window.geometry("400x200")

# Create input fields and labels
phone_label = tk.Label(text="Phone Number")
phone_entry = tk.Entry()
channel_label = tk.Label(text="Channel ID or URL")
channel_entry = tk.Entry()

# Create fetch button
fetch_button = tk.Button(text="Fetch Participants", command=fetch_participants)

# Add input fields, labels, and button to window
phone_label.pack()
phone_entry.pack()
channel_label.pack()
channel_entry.pack()
fetch_button.pack()

window.mainloop()
