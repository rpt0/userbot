import requests
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Shio"

def help_string(org):
    return h_s(org, "help_shio")


@zb.ubot("shio")
async def get_shio(client, message, *args):
    args = message.text.split()
    if len(args) < 5:
        return await message.reply_text("Gunakan format: `.shio <shio> <tanggal> <bulan> <tahun>`")

    shio, tanggal, bulan, tahun = args[1], args[2], args[3], args[4]
    API_URL = f"https://api.botcahx.eu.org/api/primbon/shio?shio={shio}&tanggal={tanggal}&bulan={bulan}&tahun={tahun}&apikey=Biyy"

    try:
        response = requests.get(API_URL)
        data = response.json()

        if not data.get("status") or not data["result"].get("status"):
            return await message.reply_text("⚠️ Data tidak ditemukan atau terjadi kesalahan.")

        result = data["result"]["message"]
        nama = result["nama"]
        arti = result["arti"]

        reply_text = (
            f"<blockquote><emoji id=6026321200597176575>🃏</emoji> **Ramalan Shio** <emoji id=6026321200597176575>🃏</emoji>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<emoji id=5470088387048266598>🐉</emoji> **Shio:** `{nama}`\n"
            f"<emoji id=5251537301154062376>📆</emoji> **Tanggal:** `{tanggal}-{bulan}-{tahun}`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<emoji id=5226512880362332956>📖</emoji> **Arti:**\n`{arti}`\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"<emoji id=5080240441882838117>😎</emoji> Semoga harimu menyenangkan! <emoji id=5080240441882838117>😎</emoji></blockquote>"
        )

        await message.reply_text(reply_text, disable_web_page_preview=True)

    except Exception as e:
        await message.reply_text(f"⚠️ Terjadi kesalahan: `{e}`")
