import aiohttp
import os
import filetype
import json
from pyrogram import Client, filters
from pyrogram.types import Message

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Remini"

def help_string(org):
    return h_s(org, "help_remini")

async def upload_media(m: Message):
    media = await m.reply_to_message.download()
    try:
        with open(media, "rb") as file:
            file_data = file.read()
            ext = filetype.guess_extension(file_data) or "jpg"
            
        form_data = aiohttp.FormData()
        form_data.add_field("fileToUpload", open(media, "rb"), filename=f"file.{ext}")
        form_data.add_field("reqtype", "fileupload")
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://catbox.moe/user/api.php", data=form_data) as res:
                if res.status == 200:
                    url = await res.text()
                    return url.strip()
                else:
                    return None
    finally:
        os.remove(media)

@zb.ubot("hd|remini")
async def remove_watermark(client, message: Message, *args):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("Reply ke foto yang ingin di HD.")
        return
    
    await message.reply_text("Proses HD...")

    url = await upload_media(message)
    if not url:
        await message.reply_text("Gagal mengunggah gambar.")
        return

    api_url = f"https://api.botcahx.eu.org/api/tools/remini-v4?url={url}&resolusi=16&apikey=Priaindia"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as res:
            if res.status == 200:
                api_response = await res.text()
                try:
                    data = json.loads(api_response)
                    image_url = data.get("url")
                    if not image_url:
                        await message.reply_text("Gagal mendapatkan URL gambar dari API.")
                        return
                except Exception as e:
                    await message.reply_text(f"Error parsing API response: {e}")
                    return

                # Download the image from the URL
                async with session.get(image_url) as img_res:
                    if img_res.status == 200:
                        image_data = await img_res.read()
                        kind = filetype.guess(image_data)
                        if not kind or not kind.mime.startswith("image"):
                            await message.reply_text(f"Gambar hasil API tidak valid. {image_url}")
                            return

                        image_path = f"no_watermark.{kind.extension}"
                        with open(image_path, "wb") as f:
                            f.write(image_data)

                        await message.reply_photo(image_path, caption="✅ Image berhasil di HD_kan.")
                        os.remove(image_path)
                    else:
                        await message.reply_text("Gagal mengunduh gambar dari link API.")
            else:
                await message.reply_text("Terjadi kesalahan saat menghubungi API.")
