from pyrogram import Client, filters
import random
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Kodam"

def help_string(org):
    return h_s(org, "help_kodamm")


def emoji(alias):
    emojis = {
        "DETEK": "<emoji id=6026321200597176575>🃏</emoji>",    
        "SUBJEK": "<emoji id=6035142758480482309>💀</emoji>",
        "ANALISIS": "<emoji id=5251569715272248625>💎</emoji>",
        "KODAM": "<emoji id=5391014066284160588>🔮</emoji>", 
        "ENERGY": "<emoji id=6030821243991626781>⚡️</emoji>",                   
    }
    return emojis.get(alias, "⎆.")


dtk = emoji("DETEK")
subj = emoji("SUBJEK")
anal = emoji("ANALISIS")
kdm = emoji("KODAM")
engy = emoji("ENERGY")


KHODAM_LIST = [
    "Naga Hitam Dimensi Ketujuh",
    "Macan Gaib Penjaga Pintu Alam",
    "Siluman Kelelawar Pemakan Cahaya",
    "Jin Api Neraka Abadi",
    "Raja Ular Bermahkota Kabut",
    "Harimau Putih Bersayap Emas",
    "Singa Gaib Penguasa Rembulan",
    "Hantu Tertawa di Balik Bayangan",
    "Pendekar Ilusi Tak Terlihat",
    "Burung Gagak Berlidah Petir",
    "Banteng Sakti Bertanduk Berlian",
    "Raksasa Mata Seribu Pengintai",
    "Dewi Penunggu Langit Senja",
    "Kera Sakti Pemegang Kitab Terlarang",
    "Jin Pasir Penghisap Nyawa",
    "Rajawali Bermata Iblis",
    "Hantu Kayu Berbisik",
    "Lelembut Merah Pengantar Mimpi",
    "Makhluk Bayangan Penjaga Gerbang Gaib",
    "Siluman Serigala Bersuara Manusia",
    "Roh Kegelapan dari Masa Depan",
    "Monyet Sakti Berjubah Api",
]

ENERGY_STATUS_LIST = [
    "Stabil", 
    "Tidak Stabil", 
    "Sangat Kuat", 
    "Melemah", 
    "Overload", 
    "Kosong", 
    "Terkendali",
]

@zb.ubot("kodam")
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
        khodam = random.choice(KHODAM_LIST)
        energy_status = random.choice(ENERGY_STATUS_LIST)

        response = f"""
<blockquote>**__{dtk} **Deteksi Khodam Aktif** {dtk}

{subj} **Subjek**: {username}
{anal} **Analisis Energi**: [{energy_percent}%] {"█" * (energy_percent // 10)}
{kdm} **Khodam Terdeteksi**: {khodam}

{engy} **Energi Mistis**: {energy_status}__**</blockquote>
"""
        await message.reply_text(response)
    else:
        await message.reply_text("{ggll} **Gagal mendeteksi pengguna...**")
