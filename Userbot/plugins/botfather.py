from pyrogram import Client, filters
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Botfather"

def help_string(org):
    return h_s(org, "help_botfather")

@zb.ubot("cbot")
async def create_bot_command(client, message, *args):
    # Ambil argumen dari pesan
    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        await message.reply_text(
            "<blockquote><b>⛔ Gunakan format: <code>{0}cbot</code> [namabot] [username_bot]</b></blockquote>\n"
            "Contoh: <code>cbot NewBot New_Bot</code>"
        )
        return

    bot_name = args[1]
    bot_username = args[2]

    if not bot_username.endswith("Bot"):
        await message.reply_text("⛔ **Username bot harus diakhiri dengan '_Bot'.**")
        return

    try:
        botfather = "@BotFather"
        
        # Kirim perintah ke BotFather
        await client.send_message(botfather, "/newbot")
        await asyncio.sleep(2)
        await client.send_message(botfather, bot_name)
        await asyncio.sleep(2)
        await client.send_message(botfather, bot_username)

        await message.reply_text(
            f"<blockquote><b>✅ **Permintaan pembuatan bot telah dikirim ke @BotFather!**\n"
            f"🆕 **Nama Bot:** `{bot_name}`\n"
            f"🤖 **Username:** @{bot_username}\n\n"
            "Silakan cek @BotFather untuk melanjutkan proses.</blockquote></b>"
        )
    
    except Exception as e:
        await message.reply_text(f"⛔ Terjadi kesalahan: {str(e)}")
