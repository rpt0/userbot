import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "ConnvertCurency"

def help_string(org):
    return h_s(org, "help_convertcurency")
    
def emoji(alias):
    emojis = {
        "COIN": "<emoji id=5872804530973840220>💲</emoji>",    
        "CONV": "<emoji id=5377336227533969892>💱</emoji>",
        "ANALISIS": "<emoji id=5251569715272248625>💎</emoji>",
        "ANALISISB": "<emoji id=6154275405990727821>🔸</emoji>",                
    }
    return emojis.get(alias, "⎆")


coin = emoji("COIN")
conv = emoji("CONV")
anal = emoji("ANALISIS")
analb = emoji("ANALISISB")

API_URL = "https://api.exchangerate-api.com/v4/latest/"

@zb.ubot("convert")
async def convert_currency(client: Client, message: Message, *args):
    args = message.text.split()
    
    if len(args) != 4:
        return await message.reply("⛔ Format salah! Gunakan: `/convert [jumlah] [dari] [ke]`.\n\nContoh: `/convert 50000 IDR USD`")

    try:
        amount = float(args[1])
        from_currency = args[2].upper()
        to_currency = args[3].upper()

        # Ambil data nilai tukar terbaru
        response = requests.get(f"{API_URL}{from_currency}")
        data = response.json()

        if "rates" not in data:
            return await message.reply("⛔ Mata uang tidak ditemukan atau tidak didukung!")

        # Hitung konversi
        if to_currency not in data["rates"]:
            return await message.reply("⛔ Mata uang tujuan tidak tersedia!")

        converted_amount = amount * data["rates"][to_currency]
        await message.reply(f"<blockquote>{coin} **Konversi Mata Uang** {coin}\n\n{conv} {amount} {from_currency} ≈ **{converted_amount:.2f} {to_currency}**</blockquote>")

    except ValueError:
        await message.reply("⛔ Jumlah harus berupa angka!")
    except Exception as e:
        await message.reply(f"⛔ Terjadi kesalahan: {e}")
