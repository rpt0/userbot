import random
import requests
from pyrogram.enums import *
from pyrogram import *
from pyrogram.types import *
from io import BytesIO

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Wallpaper"

def help_string(org):
    return h_s(org, "help_wallpaper")

URLS = {
    "teknologi": "https://api.botcahx.eu.org/api/wallpaper/teknologi?apikey=Biyy",
    "aesthetic": "https://api.botcahx.eu.org/api/wallpaper/aesthetic?apikey=Biyy",
    "katakata": "https://api.botcahx.eu.org/api/wallpaper/katakata?apikey=Biyy",
    "heker": "https://api.botcahx.eu.org/api/wallpaper/hacker?apikey=Biyy",
    "anjing": "https://api.botcahx.eu.org/api/wallpaper/anjing?apikey=Biyy",
    "hp": "https://api.botcahx.eu.org/api/wallpaper/wallhp?apikey=Biyy",
    "gamer": "https://api.botcahx.eu.org/api/wallpaper/gaming?apikey=Biyy",
    "progaming": "https://api.botcahx.eu.org/api/wallpaper/programing?apikey=Biyy",
    "chuky": "https://api.botcahx.eu.org/api/wallpaper/boneka-chucky?apikey=Biyy",
    "kucing": "https://api.botcahx.eu.org/api/wallpaper/kucing?apikey=Biyy",
    }


@zb.ubot("wall")
async def _(client, message, *args):
    # Extract query from message
    query = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if query not in URLS:
        valid_queries = ", ".join(URLS.keys())
        await message.reply(f"Query tidak valid. Gunakan salah satu dari: {valid_queries}.")
        return

    processing_msg = await message.reply("Processing...")
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = requests.get(URLS[query])
        response.raise_for_status()
        
        photo = BytesIO(response.content)
        photo.name = 'image.jpg'
        
        await client.send_photo(message.chat.id, photo)
        await processing_msg.delete()
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(f"Gagal mengambil gambar anime Error: {e}")
