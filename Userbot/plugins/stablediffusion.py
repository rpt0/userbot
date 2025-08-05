import os
import requests

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Stablediffusion"

def help_string(org):
    return h_s(org, "help_stablediffusion")

def get_giraffe_image(text):
    url = "https://api.botcahx.eu.org/api/search/stablediffusion"
    params = {
        "text": text,
        "apikey": f"045705b1"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None
                                                       
@zb.ubot("sd")
async def _(client, message, *args):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("<b><i>Gunakan perintah /stablediffusion <teks> untuk membuat gambar</i></b>.")
        return

    request_text = args[1]
    await message.reply_text("<b><i>Sedang memproses, mohon tunggu</i></b>...")

    image_content = get_giraffe_image(request_text)
    if image_content:
        temp_file = "img.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)

        await message.reply_photo(photo=temp_file)
        
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")