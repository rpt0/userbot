from pyrogram import Client, filters
from pyrogram import *
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Cuser"

def help_string(org):
    return h_s(org, "help_cuser")

@zb.ubot("cuser")
async def cek_user_command(client, message, *args):
    # Ambil argumen dari pesan
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.reply_text(
            "<blockquote><b>⛔ Gunakan format: cuser [username]</b></blockquote>"
        )
        return

    username = args[1]
    platforms = {
        "🔹 GitHub": f"https://github.com/{username}",
        "🔹 Instagram": f"https://www.instagram.com/{username}",
        "🔹 Facebook": f"https://www.facebook.com/{username}",
        "🔹 Twitter/X": f"https://x.com/{username}",
        "🔹 TikTok": f"https://www.tiktok.com/@{username}",
        "🔹 Telegram": f"https://t.me/{username}"
    }

    result_text = f"🔍 **Hasil Pencarian untuk Username:** `{username}`\n\n"
    result_text += "\n".join([f"{platform}: [Klik disini]({link})" for platform, link in platforms.items()])

    await message.reply_text(result_text, disable_web_page_preview=True)
