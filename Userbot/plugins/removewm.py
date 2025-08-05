import aiohttp
import os
import filetype
from pyrogram import Client, filters
from pyrogram.types import Message

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "RemoveWm"

def help_string(org):
    return h_s(org, "help_removewm")


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

@zb.ubot("removewm")
async def remove_watermark(client, message: Message, *args):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("Reply ke foto yang ingin dihapus watermarknya.")
        return
    
    await message.reply_text("Menghapus watermark...")

    url = await upload_media(message)
    if not url:
        await message.reply_text("Gagal mengunggah gambar.")
        return

    api_url = f"https://api.siputzx.my.id/api/tools/dewatermark?url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as res:
            if res.status == 200:
                image_data = await res.read()
                image_path = "no_watermark.jpg"
                
                with open(image_path, "wb") as f:
                    f.write(image_data)

                await message.reply_photo(image_path, caption="✅ Watermark berhasil dihapus.")
                os.remove(image_path)
            else:
                await message.reply_text("Terjadi kesalahan saat menghubungi API.")
