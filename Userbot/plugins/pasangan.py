import requests
from pyrogram import Client, filters
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Pasangan"

def help_string(org):
    return h_s(org, "help_pasangan")


@zb.ubot("pasangan")
async def cek_kecocokan(_, message, *args):
    text = message.text[len(message.command[0]) + 2:].strip()

    if "," not in text:
        return await message.reply("**Gunakan format:**\n`.pasangan nama1, nama2`")

    nama1, nama2 = map(str.strip, text.split(",", 1))

    api_url = f"https://api.siputzx.my.id/api/primbon/kecocokan_nama_pasangan?nama1={nama1}&nama2={nama2}"
    
    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("status"):
            hasil = data["data"]
            teks = (
                "<blockquote>"
                f"<emoji id=6026321200597176575>🃏</emoji> **Kecocokan Nama Pasangan** <emoji id=6026321200597176575>🃏</emoji>\n"
                f"<emoji id=5204015897500469606>😢</emoji> **{hasil['nama_anda']}**\n <emoji id=5226859896539989141>😘</emoji> **{hasil['nama_pasangan']}**\n\n"
                f"<emoji id=5217466996337165348>👍</emoji> **Sisi Positif:**\n`{hasil['sisi_positif']}`\n\n"
                f"<emoji id=5436223772510142944>👎</emoji> **Sisi Negatif:**\n`{hasil['sisi_negatif']}`\n\n"
                f"<emoji id=5238039443008408242>💌</emoji> **Catatan:**\n_{hasil['catatan']}_"
                "</blockquote>"
            )
            await message.reply_photo(hasil["gambar"], caption=teks)
        else:
            await message.reply("⚠️ **Gagal mendapatkan data kecocokan.**")
    
    except Exception as e:
        await message.reply(f"❌ **Terjadi kesalahan:** `{e}`")
