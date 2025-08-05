import os
import requests
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "Ephoto4"

def help_string(org):
    return h_s(org, "help_ephoto4")

# Masukkan API Key Anda di sini
API_KEY = "Biyy"  # Ganti dengan API key yang benar

def fetch_image(api_url, text, *args):
    """
    Fungsi untuk mengambil gambar dari API
    """
    params = {"text": text, "apikey": API_KEY}
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            print("Response bukan gambar:", response.text)  # Debugging
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image: {e}")  # Debugging jika ada kesalahan
        return None

async def process_image_command(client, message, api_url, command_name, *args):
    """
    Fungsi umum untuk menangani perintah pembuatan gambar
    """
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text(f"<b><i>Gunakan perintah /{command_name} <teks> untuk membuat gambar.</i></b>")
        return

    request_text = args[1]
    await message.reply_text("<b><i>Sedang memproses, mohon tunggu...</i></b>")

    image_content = fetch_image(api_url, request_text)
    if image_content:
        temp_file = f"{command_name}.jpg"
        with open(temp_file, "wb") as f:
            f.write(image_content)
        await message.reply_photo(photo=temp_file)
        os.remove(temp_file)
    else:
        await message.reply_text("Gagal membuat gambar. Coba lagi nanti.")

# Handler untuk setiap perintah
@zb.ubot("bn")
async def eraser_command(client, message, *args):
    api_url = "https://api.botcahx.eu.org/api/ephoto/blueneon"
    await process_image_command(client, message, api_url, "blueneon")

@zb.ubot("ns")
async def papercut_command(client, message, *args):
    api_url = "https://api.botcahx.eu.org/api/ephoto/nightstars"
    await process_image_command(client, message, api_url, "nightstars")
    
@zb.ubot("cloud")
async def papercut_command(client, message, *args):
    api_url = "https://api.botcahx.eu.org/api/ephoto/cloud"
    await process_image_command(client, message, api_url, "cloud")

@zb.ubot("paper")
async def papercut_command(client, message, *args):
    api_url = "https://api.botcahx.eu.org/api/ephoto/papercut"
    await process_image_command(client, message, api_url, "papercut")
    
@zb.ubot("horor")
async def papercut_command(client, message, *args):
    api_url = "https://api.botcahx.eu.org/api/ephoto/horor"
    await process_image_command(client, message, api_url, "horor")
    
@zb.ubot("pigcute")
async def papercut_command(client, message, *args):
    api_url = "https://api.botcahx.eu.org/api/ephoto/pig"
    await process_image_command(client, message, api_url, "pig")
