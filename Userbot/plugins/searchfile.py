import requests
from pyrogram import Client, filters
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "SearchFilei"

def help_string(org):
    return h_s(org, "help_searchfile")

@zb.ubot("sfile")
async def search_sfile(client, message, *args):
    if len(message.command) < 2:
        return await message.reply_text("Gunakan format: `/sfile <query>`")

    query = " ".join(message.command[1:])
    API_URL = f"https://api.siputzx.my.id/api/s/sfile?query={query}"
    
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        if not data.get("status") or not data.get("data"):
            return await message.reply_text("Tidak ada hasil ditemukan.")

        results = data["data"][:5]
        reply_text = "<blockquote>**Hasil Pencarian:**\n\n"

        for item in results:
            reply_text += f"📂 **{item['title']}**\n🔗 [Download]({item['url']})</blockquote>\n\n"

        await message.reply_text(reply_text, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"Terjadi kesalahan: {e}")
