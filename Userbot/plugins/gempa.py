import requests
import wget
import os
from pyrogram import Client
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Gempa"

def help_string(org):
    return h_s(org, "help_gempa")


@zb.ubot("gempa")
async def stalkig(client, message, *args):
    jalan = await message.reply(f"💫 Processing...")
    chat_id = message.chat.id
    url = f"https://api.botcahx.eu.org/api/search/gempa?apikey=moire"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            hasil = data['result']['result']
            lintang = hasil['Lintang']
            bujur = hasil['Bujur']
            magnitude = hasil['Magnitudo']
            kedalaman = hasil['Kedalaman']
            potensi = hasil['Potensi']
            wilayah = hasil['Wilayah']
            tanggal = hasil['tanggal']
            jam = hasil['jam']
            photoUrl = f"https://warning.bmkg.go.id/img/logo-bmkg.png"
            caption = f"""
<blockquote><b>╭─ •  「 <b>Info Gempa Terkini</b> 」
│  ◦ <b>Magnitude: <code>{magnitude}</code></b>
│  ◦ <b>Kedalaman: <code>{kedalaman}</code></b>
│  ◦ <b>Koordinat: <code>{bujur}, {lintang}</code></b>
│  ◦ <b>Waktu: <code>{tanggal}, {jam}</code></b>
│  ◦ <b>Lokasi: <code>{wilayah}</code></b>
│  ◦ <b>Potensi: <code>{potensi}</code></b>
╰──── • 
</blockquote></b>
"""
            photo_path = wget.download(photoUrl)
            await client.send_photo(chat_id, caption=caption, photo=photo_path)
            if os.path.exists(photo_path):
                os.remove(photo_path)
            
            await jalan.delete()
        else:
            await jalan.edit(f"⛔ No 'result' key found in the response.")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"⛔ Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"⛔ An error occurred: {e}")
