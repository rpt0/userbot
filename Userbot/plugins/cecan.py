import random
import requests
from pyrogram.enums import *
from pyrogram import *
from pyrogram.types import *
from io import BytesIO
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Cecan"

def help_string(org):
    return h_s(org, "help_cecan")

URLS = {
    "indonesia": "https://api.botcahx.eu.org/api/cecan/indonesia?apikey=Priaindia",
    "china": "https://api.botcahx.eu.org/api/cecan/china?apikey=Priaindia",
    "thailand": "https://api.botcahx.eu.org/api/cecan/thailand?apikey=Priaindia",
    "vietnam": "https://api.botcahx.eu.org/api/cecan/vietnam?apikey=Priaindia",
    "hijaber": "https://api.botcahx.eu.org/api/cecan/hijaber?apikey=Priaindia",
    "rose": "https://api.botcahx.eu.org/api/cecan/rose?apikey=Priaindia",
    "ryujin": "https://api.botcahx.eu.org/api/cecan/ryujin?apikey=Priaindia",
    "jiso": "https://api.botcahx.eu.org/api/cecan/jiso?apikey=Priaindia",
    "jeni": "https://api.botcahx.eu.org/api/cecan/jeni?apikey=Priaindia",
    "justinaxie": "https://api.botcahx.eu.org/api/cecan/justinaxie?apikey=Priaindia",
    "malaysia": "https://api.botcahx.eu.org/api/cecan/malaysia?apikey=Priaindia",
    "japan": "https://api.botcahx.eu.org/api/cecan/japan?apikey=Priaindia",
    "korea": "https://api.botcahx.eu.org/api/cecan/korea?apikey=Priaindia"
}

@zb.ubot("cecan")
async def _(client, message, *args):
    # Extract query from message
    query = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if query not in URLS:
        valid_queries = ", ".join(URLS.keys())
        await message.reply(f"Query tidak valid. Gunakan salah satu dari: {valid_queries}.")
        return

    processing_msg = await message.reply("Processing.....")
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = requests.get(URLS[query])
        response.raise_for_status()
        
        photo = BytesIO(response.content)
        photo.name = 'image.jpg'
        
        await client.send_photo(message.chat.id, photo)
        await processing_msg.delete()
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(f"Gagal mengambil gambar cecan Error: {e}")
