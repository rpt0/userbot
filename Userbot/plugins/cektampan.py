from pyrogram import Client, filters
import random
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "CekTampan"

def help_string(org):
    return h_s(org, "help_cektampan")


def emoji(alias):
    emojis = {
        "DETEK": "<emoji id=6026321200597176575>🃏</emoji>",    
        "SUBJEK": "<emoji id=6035142758480482309>💀</emoji>",
        "ANALISIS": "<emoji id=5251569715272248625>💎</emoji>",
        "ANALISISB": "<emoji id=5787363840316411387>🗄</emoji>",
        "KODAM": "<emoji id=5391014066284160588>🔮</emoji>", 
        "ENERGY": "<emoji id=6030821243991626781>⚡️</emoji>",
        "ENERGYY": "<emoji id=5217820936002097532>🍑</emoji>", 
        "KODAMM": "<emoji id=5226859896539989141>😘</emoji>"                
    }
    return emojis.get(alias, "⎆.")


dtk = emoji("DETEK")
subj = emoji("SUBJEK")
anal = emoji("ANALISIS")
analb = emoji("ANALISISB")
kdm = emoji("KODAM")
kdmm = emoji("KODAMM")
engy = emoji("ENERGY")
engyy = emoji("ENERG-Y")


KHODAM_LIST = [
    "Mereka tersenyum ketika melihatmu.",
    "Mereka senang berbicara denganmu.",
    "Mereka curi-curi pandang.",
    "Mereka bersikap berbeda.",
    "Mereka selalu mencoba untuk membantu",
    "Mereka memberikan pujian.",
]

ENERGY_STATUS_LIST = [
    "Sering mengkritik orang lain", 
    "Merendahkan atau meremehkan orang lain", 
    "Tidak memiliki empati", 
    "Mengontrol dan memanipulasi orang lain", 
    "Menimbulkan suasana negatif", 
    "Sulit meminta maaf", 
    "Merasa dirinya paling benar",
    "Menciptakan drama dan konflik",
    "Menyalahkan orang lain",              
]

@zb.ubot("ctampan")
async def _(client, message, *args):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user = await client.get_users(message.command[1])
    else:
        user = message.from_user
    
    if user:
        username = f"@{user.username}" if user.username else user.first_name
        energy_percent = random.randint(10, 100)
        pd_percent = random.randint(10, 100)
        rapi_percent = random.randint(10, 100)
        humor_percent = random.randint(10, 100) 
        skill_percent = random.randint(10, 100)
        atti_percent = random.randint(10, 100)
        pass_percent = random.randint(10, 100)          
        khodam = random.choice(KHODAM_LIST)
        energy_status = random.choice(ENERGY_STATUS_LIST)

        response = f"""
<blockquote>**__{dtk} **Deteksi Ketampanan Aktif** {dtk}

{subj} **Subjek**: {username}
{analb} **Analisis Ketampanan**: [{energy_percent}%] {"█" * (energy_percent // 10)}
{analb} **Rasa Percaya Diri**: [{pd_percent}%] {"█" * (pd_percent // 10)}
{analb} **Rapi dan Stylish**: [{rapi_percent}%] {"█" * (rapi_percent // 10)}
{analb} **Humoris**: [{humor_percent}%] {"█" * (humor_percent // 10)}
{analb} **Skill**: [{skill_percent}%] {"█" * (skill_percent // 10)}
{analb} **Attitude**: [{atti_percent}%] {"█" * (atti_percent // 10)}
{analb} **Passion**: [{pass_percent}%] {"█" * (pass_percent // 10)}
{kdmm} **Dimata Orang Lain**: {khodam}

{engyy} **Sikap Toxic**: {energy_status}__**</blockquote>
"""
        await message.reply_text(response)
    else:
        await message.reply_text("⛔ **Gagal mendeteksi pengguna...**")
