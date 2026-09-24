import os
import requests
from dotenv import load_dotenv
from telethon import TelegramClient, events
from msgdb import init_db, save_message, get_message, update_message, get_message_data

load_dotenv()

api_id = int(os.getenv("BOT_API"))
api_hash = os.getenv("BOT_HASH")
bot_token = os.getenv("BOT_TOKEN")

BOT_CHAT_ID = 8251759731
client = TelegramClient('user', api_id, api_hash)

def send_to_bot(message):
    requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": BOT_CHAT_ID, "text": message})
send_to_bot("Бот запущен!")

@client.on(events.NewMessage)
async def new_message(event):
    sender = await event.get_sender()
    sender_id = sender.id if sender else None
    sender_username = getattr(sender, 'username', None)

    if sender:
        first_name = getattr(sender, 'first_name', None)
        last_name = getattr(sender, 'last_name', None)
        sender_name = f"{first_name} {last_name}".strip() if first_name or last_name else None
    else:
        sender_name = None

    text = event.raw_text

    save_message(event.chat_id, event.message.id, sender_id, sender_username, sender_name, text, event.message.date.isoformat())

@client.on(events.MessageEdited)
async def edited_message(event):
    sender = await event.get_sender()

    if sender:
        username = getattr(sender, "username", None)
        first_name = getattr(sender, "first_name", None) or ""
        last_name = getattr(sender, "last_name", None) or ""
        sender_name = f"{first_name} {last_name}".strip()
    else:
        username = None
        sender_name = None

    old_text = get_message(event.chat_id, event.message.id)
    new_text = event.raw_text
    if old_text is None:
        return
    if old_text == new_text:
        return
    send_to_bot(f"Сообщение отредактировано: \n"
        f"Отправитель: {sender_name}, {f'(@{username})' if username else ''}\n"
        f"Old: \n {old_text}\n"
        f"New: \n {new_text}\n"
        )


    update_message(event.chat_id, event.message.id, new_text)

@client.on(events.MessageDeleted)
async def deleted_message(event):
    for message_id in event.deleted_ids:
        message_data = get_message_data(event.chat_id, message_id)
        if message_data is None:
            continue
        sender_username, sender_name, old_text = message_data
        old_text = get_message(event.chat_id, message_id)
        if old_text is None:
            continue
        send_to_bot(f"Сообщение удалено: \n"
            f"Отправитель: {sender_name} {f'(@{sender_username})' if sender_username else ''}\n"
            f"Old: \n {old_text}\n"
            )
        update_message(event.chat_id, message_id, "[deleted]")



init_db()

print("Бот запущен. Ожидание новых сообщений...")


client.start()
client.run_until_disconnected()