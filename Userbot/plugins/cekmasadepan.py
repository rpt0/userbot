from pyrogram import Client, filters
import random
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "CekMasaDepan"

def help_string(org):
    return h_s(org, "help_cekmasadepan")


def emoji(alias):
    emojis = {
        "DETEK": "<emoji id=6026321200597176575>🃏</emoji>",    
        "SUBJEK": "<emoji id=5215503483318325191>👊</emoji><emoji id=5217914643598557136>👊</emoji>",
        "KARIR": "<emoji id=5206659381151680254>☀️</emoji>", 
        "JODOH": "<emoji id=5226859896539989141>😘</emoji><emoji id=5204015897500469606>😢</emoji>",
        "WARISAN": "<emoji id=5235457574958023592>💸</emoji>",
        "PASANGAN": "<emoji id=5434008750501415949>🫶</emoji>",
        "ANAK": "<emoji id=5217820936002097532>🍑</emoji>",                   
    }
    return emojis.get(alias, "⎆")


dtk = emoji("DETEK")
subj = emoji("SUBJEK")
kar = emoji("KARIR")
jod = emoji("JODOH")
war = emoji("WARISAN")
pas = emoji("PASANGAN")
anak = emoji("ANAK")


PASANGAN_LIST = [
    "1 Setia",
    "2",
    "3",
    "4",
    "5",
]

ANAK_STATUS_LIST = [
    "2 Anak", 
    "3 Anak", 
    "4 Anak", 
    "5 Anak", 
    "6 Anak", 
    "7 Anak", 
    "8 Anak",
]

@zb.ubot("cmasadepan")
async def _(client, message, *args):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user = await client.get_users(message.command[1])
    else:
        user = message.from_user
    
    if user:
        username = f"@{user.username}" if user.username else user.first_name
        karir_percent = random.randint(10, 100)
        jodoh_percent = random.randint(10, 100)
        warisan_percent = random.randint(10, 100)        
        pasangan = random.choice(PASANGAN_LIST)
        anak_status = random.choice(ANAK_STATUS_LIST)

        response = f"""
<blockquote>**__{dtk} **Hasil Deteksi Masa Depan** {dtk}

{subj} **Subjek**: {username}
{jod} **Jodoh**: [{jodoh_percent}%] {"█" * (jodoh_percent // 10)}
{kar} **Karir**: [{karir_percent}%] {"█" * (karir_percent // 10)}
{war} **Warisan**: [{warisan_percent}%] {"█" * (warisan_percent // 10)}

{pas} **Jumlah Pasangan Masa Depan**: {pasangan}
{anak} **Jumlah Anak Masa Depan**: {anak_status}__**</blockquote>
"""
        await message.reply_text(response)
    else:
        await message.reply_text("⛔  **Gagal mendeteksi pengguna...**")
