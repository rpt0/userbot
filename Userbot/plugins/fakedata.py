import requests
from pyrogram import Client, filters
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "FakeData"

def help_string(org):
    return h_s(org, "help_fakedata")

@zb.ubot("fakedata")
async def generate_fake_data(client, message, *args):
    API_URL = "https://api.siputzx.my.id/api/tools/fake-data"
    params = {
        "type": "person",
        "count": 5
    }
    
    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        
        if data.get("status"):
            fake_list = data.get("data", [])
            result = "<blockquote>**Fake Profiles:**\n"
            
            for i, fake in enumerate(fake_list, start=1):
                result += f"\n**{i}.**\n"
                result += f"👤 **Name:** `{fake['name']}`\n"
                result += f"📧 **Email:** `{fake['email']}`\n"
                result += f"📞 **Phone:** `{fake['phone']}`\n"
                result += f"🎂 **Birth Date:** `{fake['birthDate']}`\n"
                result += f"⚧ **Gender:** `{fake['gender']}`</blockquote>\n"
            
            await message.reply_text(result)
        else:
            await message.reply_text("Gagal mengambil data Fake Data.")
    
    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {e}")
                
