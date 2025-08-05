import aiohttp
import filetype
import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "WhatMusic"

def help_string(org):
    return h_s(org, "help_whatmusic")


async def upload_media(m: Message):
    media = await m.reply_to_message.download()
    try:
        ext = "unknown"
        if os.path.exists(media):
            kind = filetype.guess(media)
            if kind:
                ext = kind.extension
        
        form_data = aiohttp.FormData()
        form_data.add_field("fileToUpload", open(media, "rb"), filename=f"file.{ext}")
        form_data.add_field("reqtype", "fileupload")
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://catbox.moe/user/api.php", data=form_data) as res:
                if res.status == 200:
                    response_text = await res.text()
                    return response_text.strip()
                else:
                    return None
    except Exception as e:
        print(f"Error saat mengunggah media: {e}")
        return None
    finally:
        if os.path.exists(media):
            os.remove(media)

@zb.ubot("whatmusic")
async def whatmusic_handler(client, message: Message, *args):
    if not message.reply_to_message or not message.reply_to_message.video:
        return await message.reply("Silakan balas ke sebuah video untuk mengenali musiknya.")
    
    msg = await message.reply("🔄 Mengunggah video...")
    video_url = await upload_media(message)

    if not video_url:
        return await msg.edit("❌ Gagal mengunggah video!")
    
    await msg.edit("🎵 Menganalisis musik dalam video...")
    
    response = requests.get(f"https://api.botcax.eu.org/api/tools/whatmusic?url={video_url}&apikey=Biyy")
    if response.status_code == 200:
        try:
            data = response.json()
            print("API Response:", data)
            
            if data.get("status"):
                result = data.get("result", "").strip()
                if not result or "undefined" in result.lower():
                    return await msg.edit("❌ Musik tidak ditemukan dalam video.")
                return await msg.edit(f"**🎶 Hasil Pengenalan Musik:**\n```{result}```")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            return await msg.edit("❌ Terjadi kesalahan dalam memproses data API.")
    return await msg.edit(f"❌ Gagal mendapatkan hasil (Status: {response.status_code})")
