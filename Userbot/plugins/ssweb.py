import os
import datetime
import requests
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "SsWeb"

def help_string(org):
    return h_s(org, "help_ssweb")

def get_ssweb_image(url):
    api_url = "https://api.botcahx.eu.org/api/tools/ssweb"
    params = {
        "url": url,
        "device": "desktop",
        "apikey": "Priaindia"
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None

@zb.ubot("ssweb")
async def screenshot_handler(client, message, *args):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("<b><i>Input URL!</i></b>")
        return

    url = args[1].strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    await message.reply_text("<b><i>Ｌｏａｄｉｎｇ．．.</i></b>")

    image_data = get_ssweb_image(url)
    if not image_data:
        await message.reply_text("<b><i>Gagal mengambil screenshot.</i></b>")
        return

    filepath = f"img2p.jpeg"
    with open(filepath, "wb") as file:
        file.write(image_data)

    await client.send_photo(message.chat.id, filepath, caption="**__Nih Gambarnya Dah Gw Eses.__**")
    os.remove(filepath)
    
