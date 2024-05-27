

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pymongo import MongoClient
import random
import os

API_ID = "6435225"
API_HASH = "4e984ea35f854762dcde906dce426c2d"
SESSION_NAME = os.environ.get("SESSION_NAME", "")
MONGO_URL = os.environ.get("MONGO_URL", "")

client = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)

@client.on_message(filters.command("alive", prefixes=["/", ".", "?", "-"]) & ~filters.private)
async def start(client, message):
    await message.reply_text(f"** ᴀɪ ᴜsᴇʀʙᴏᴛ ғᴏʀ ᴄʜᴀᴛᴛɪɴɢ ɪs ᴡᴏʀᴋɪɴɢ**")

async def process_message(client, message, chatai):
    K = []
    is_chat = chatai.find({"word": message.text})
    k = chatai.find_one({"word": message.text})
    if k:
        for x in is_chat:
            K.append(x['text'])
        hey = random.choice(K)
        is_text = chatai.find_one({"text": hey})
        Yo = is_text['check']
        if Yo == "sticker":
            await message.reply_sticker(f"{hey}")
        else:
            await message.reply_text(f"{hey}")

@client.on_message((filters.text | filters.sticker) & ~filters.private & ~filters.me & ~filters.bot)
async def Daxxai(client, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    if not message.reply_to_message:
        Daxxdb = MongoClient(MONGO_URL)
        Daxx = Daxxdb["DaxxDb"]["Daxx"]
        is_Daxx = Daxx.find_one({"chat_id": message.chat.id})
        if not is_Daxx:
            await client.send_chat_action(message.chat.id, "typing")
            await process_message(client, message, chatai)

    if message.reply_to_message:
        Daxxdb = MongoClient(MONGO_URL)
        Daxx = Daxxdb["DaxxDb"]["Daxx"]
        is_Daxx = Daxx.find_one({"chat_id": message.chat.id})
        getme = await client.get_me()
        user_id = getme.id
        if message.reply_to_message.from_user.id == user_id:
            if not is_Daxx:
                await client.send_chat_action(message.chat.id, "typing")
                await process_message(client, message, chatai)
        else:
            if message.sticker:
                is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
                if not is_chat:
                    chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
            if message.text:
                is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})
                if not is_chat:
                    chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})

@client.on_message((filters.text | filters.sticker) & filters.private & ~filters.me & ~filters.bot)
async def Daxxprivate(client, message):
    chatdb = MongoClient(MONGO_URL)
    chatai = chatdb["Word"]["WordDb"]

    if not message.reply_to_message:
        await client.send_chat_action(message.chat.id, "typing")
        await process_message(client, message, chatai)

    if message.reply_to_message:
        getme = await client.get_me()
        user_id = getme.id
        if message.reply_to_message.from_user.id == user_id:
            await client.send_chat_action(message.chat.id, "typing")
            await process_message(client, message, chatai)

client.run()
