import requests
import wget
import os
from pyrogram import Client
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Cuaca"

def help_string(org):
    return h_s(org, "help_cuaca")

@zb.ubot("cuaca")
async def cuaca(client, message, *args):
    jalan = await message.reply(f"🪐 Processing...")
    a = message.text.split(' ', 1)[1]
    chat_id = message.chat.id
    url = f"https://api.botcahx.eu.org/api/tools/cuaca?query={a}&apikey=Biyy"
        
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            hasil = data['result']
            location = hasil['location']
            country = hasil['country']
            weather = hasil['weather']
            currentTemp = hasil['currentTemp']
            maxTemp = hasil['maxTemp']
            minTemp = hasil['minTemp']
            humidity = hasil['humidity']
            windSpeed = hasil['windSpeed']
            photoUrl = f"https://telegra.ph//file/9354c197366cde09650fd.jpg"
            caption = f"""
<blockquote>╭─ •  「 <b>Info Cuaca Terkini</b> 」
│  ◦ <b>location: <code>{location}</code></b>
│  ◦ <b>country: <code>{country}</code></b>
│  ◦ <b>weather: <code>{weather}</code></b>
│  ◦ <b>currentTemp: <code>{currentTemp}</code></b>
│  ◦ <b>Temp: <code>{maxTemp}, {minTemp}</code></b>
│  ◦ <b>windSpeed: <code>{windSpeed}</code></b></blockquote>
╰──── •
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
