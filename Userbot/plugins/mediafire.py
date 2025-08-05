from pyrogram import Client, filters
import requests
import os
import mimetypes
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Mediafire"

def help_string(org):
    return h_s(org, "help_mediafire")

@zb.ubot("mediafire|mf")
async def _(client, message, *args):
    args = message.text.split(" ", 1)

    if len(args) < 2:
        await message.reply_text("❌ Harap kirimkan URL Mediafire dengan format:\n`.mediafire <url_mediafire>`", quote=True)
        return

    mediafire_url = args[1]
    api_url = f"https://api.botcahx.eu.org/api/dowloader/mediafire?url={mediafire_url}&apikey=Priaindia"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("status") and "result" in data:
            file_info = data["result"]
            filename = file_info["filename"]
            filesize = file_info["filesize"]
            file_url = file_info["url"]

            downloading_msg = await message.reply_text(f"📥 Mengunduh **{filename}** ({filesize})...", quote=True)

            file_path = f"./{filename}"
            file_response = requests.get(file_url, stream=True)

            with open(file_path, "wb") as file:
                for chunk in file_response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            mime_type, _ = mimetypes.guess_type(file_path)

            if mime_type:
                if mime_type.startswith("image"):
                    await message.reply_photo(file_path, caption=f"✅ **Gambar berhasil diunduh!**\n📂 **Nama:** `{filename}`\n📦 **Ukuran:** `{filesize}`")
                elif mime_type.startswith("video"):
                    await message.reply_video(file_path, caption=f"✅ **Video berhasil diunduh!**\n📂 **Nama:** `{filename}`\n📦 **Ukuran:** `{filesize}`")
                elif mime_type.startswith("audio"):
                    await message.reply_audio(file_path, caption=f"✅ **Audio berhasil diunduh!**\n📂 **Nama:** `{filename}`\n📦 **Ukuran:** `{filesize}`")
                else:
                    await message.reply_document(file_path, caption=f"✅ **File berhasil diunduh!**\n📂 **Nama:** `{filename}`\n📦 **Ukuran:** `{filesize}`")
            else:
                await message.reply_document(file_path, caption=f"✅ **File berhasil diunduh!**\n📂 **Nama:** `{filename}`\n📦 **Ukuran:** `{filesize}`")

            os.remove(file_path)

            await downloading_msg.delete()
        else:
            await message.reply_text("⚠️ Gagal mendapatkan informasi file dari Mediafire.", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan:\n`{str(e)}`", quote=True)
        
