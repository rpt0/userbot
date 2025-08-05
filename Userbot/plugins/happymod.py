from pyrogram import Client, filters
import requests
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "HappyMod"

def help_string(org):
    return h_s(org, "help_happymod")

@zb.ubot("hmod")
async def _(client, message, *args):
    args = message.text.split(" ", 1)

    if len(args) < 2:
        await message.reply_text("❌ Harap gunakan format:\n`.happymod <nama_aplikasi>`", quote=True)
        return

    query = args[1]
    api_url = f"https://api.botcahx.eu.org/api/search/happymod?query={query}&apikey=Priaindia"

    try:
        response = requests.get(api_url)
        data = response.json()

        if not data.get("status") or "result" not in data:
            await message.reply_text("⚠️ Tidak ditemukan hasil untuk pencarian ini.", quote=True)
            return

        results = data["result"][:5]
        response_text = "🔍 **Hasil Pencarian HappyMod:**\n\n"

        for item in results:
            title = item["title"]
            icon = item["icon"]
            rating = item["rating"]
            link = item["link"]

            response_text += (
                f"""
**__📌 {title}
⭐ Rating: {rating}
🔗 [Unduh di HappyMod]({link})__**"""
            )

        await message.reply_text(response_text, disable_web_page_preview=True, quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Terjadi kesalahan:\n`{str(e)}`", quote=True)
