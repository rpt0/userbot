from pyrogram import Client, filters
import random
from Userbot import *

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, zb

__MODULES__ = "Cekharta"


def help_string(org):
    return h_s(org, "help_cekharta")



def emoji(alias):
    emojis = {
        "DETEK": "<emoji id=6026321200597176575>🃏</emoji>",    
        "SUBJEK": "<emoji id=5382148180043376268>😱</emoji>",
        "DOMPET": "<emoji id=6257972409190585253>💰</emoji>",
        "ATM": "<emoji id=5472250091332993630>💳</emoji>",
        "MOBIL": "<emoji id=5429317443623339836>🚘</emoji>", 
        "RUMAH": "<emoji id=4958485609464202497>🏡</emoji>",
        "KERJA": "<emoji id=5384549749661641183>🤔</emoji>",
        "HEWAN": "<emoji id=5256041592271157291>🐈‍⬛</emoji>",           
    }
    return emojis.get(alias, "⎆")


dtk = emoji("DETEK")
subj = emoji("SUBJEK")
domp = emoji("DOMPET")
atm = emoji("ATM")
mob = emoji("MOBIL")
rum = emoji("RUMAH")
kerj = emoji("KERJA")
hewn = emoji("HEWAN")
engy = emoji("ENERGY")


MOBIL_LIST = [
    "Rolls-Royce Phantom",
    "Bentley Mulsanne",
    "Mercedes-Benz S-Class",
    "BMW 7 Series",
    "Aston Martin Phantom",
    "Jaguar XJ",
    "Suzuki Carry",
    "Datsun 120Y",
    "Mitsubishi Colt",
    "Bajai",
    "Sepeda Ontel",
    "Becak",
    "Harley-Davidson Cosmic Starship",
    "Kawasaki Ninja H2R",
    "Honda Astrea",
    "Hinda C70",
    "Modal pinjam",
]

RUMAH_LIST = [
    "Kota Deltamas", 
    "Sudirman Park", 
    "The Residence at The Ritz-Carlton", 
    "Pondok Indah ", 
    "Bintaro Jaya", 
    "Rumah Subsidi", 
    "Gubuk Indah",
    "Ngontrak",
]

HEWAN_LIST = [
    "Anjing Tibetan Mastiff", 
    "Anjing Samoyed", 
    "Anjing Chow Chow", 
    "Kucing Bengal", 
    "Kucing Savannah", 
    "Kucing Persian", 
    "Ular albino",
    "Iguana hijau",
    "Kecoa",
    "Tikus",
    "Cacing",
    "Lalat",
    "Nyamuk",
]

PEKERJAAN_LIST = [
    "Direktur", 
    "Manager", 
    "Pengusaha Properti", 
    "Ojek Pangkalan", 
    "Tukang cuci", 
    "Office Boy", 
    "Pengusaha Sawit",
    "Pengangguran",
    "Pengacara",
    "PNS",
    "Kuli Bangunan",
    "Preman Pasar",
    "PNS",
]

@zb.ubot("charta")
async def _(client, message, *args):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user = await client.get_users(message.command[1])
    else:
        user = message.from_user
    
    if user:
        username = f"@{user.username}" if user.username else user.first_name
        sukses_percent = random.randint(10, 100)
        karir_percent = random.randint(10, 100)    
        mobil = random.choice(MOBIL_LIST)
        rumah = random.choice(RUMAH_LIST)
        hewan = random.choice(HEWAN_LIST)
        kerj = random.choice(PEKERJAAN_LIST)

        response = f"""
<blockquote>**__{dtk} **Deteksi Harta** {dtk}

{subj} **Subjek**: {username}
{domp} **Kesuksesan**: [{sukses_percent}%] {"█" * (sukses_percent // 10)}
{atm} **Karir**: [{karir_percent}%] {"█" * (karir_percent // 10)}

{mob} **Kendaraan**: {mobil}
{rum} **Rumah**: {rumah}
{kerj} **Pekerjaan**: {kerj}
{hewn} **hewan**: {hewan}__**</blockquote>
"""
        await message.reply_text(response)
    else:
        await message.reply_text("{ggll} **Gagal mendeteksi pengguna...**")
