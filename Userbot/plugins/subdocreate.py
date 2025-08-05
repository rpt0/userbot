import requests
import json
from pyrogram import *
from pyrogram import Client, filters
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "SubdoCreate"

def help_string(org):
    return h_s(org, "help_subdocreate")

# Konfigurasi Cloudflare (Tambahkan daftar domain dengan Zone ID)
CLOUDFLARE_API_TOKEN = "auQMrkPsYbpFO29HwHMEVzNvkY_nLNlR3vPW6Y7Y"
DOMAIN_LIST = {
    "digitalatelier.tech": "1932711fb1d4d86b1f53b00d1b275f8a",
    "mydigital-store.me": "11c1abb8f727bf4d7342f1cade2b3cd7"
}

# Fungsi untuk menambahkan subdomain ke Cloudflare
def create_subdomain(zone_id, subdomain, target_ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "type": "A",  # Bisa diubah ke "CNAME" jika ingin menggunakan CNAME
        "name": subdomain,
        "content": target_ip,
        "ttl": 1,
        "proxied": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

@zb.ubot("subdocreate")
async def subdomain_create(client, message, *args):
    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        await message.reply_text("❌ Silakan masukkan format yang benar: `.subdocreate [domain] [subdomain] [IP]`")
        return

    domain = args[1].strip()
    subdomain = args[2].strip()
    target_ip = args[3].strip()

    if domain not in DOMAIN_LIST:
        await message.reply_text(f"❌ Domain `{domain}` tidak ditemukan dalam daftar. Gunakan `.domainlist` untuk melihat daftar domain yang tersedia.")
        return

    zone_id = DOMAIN_LIST[domain]
    full_subdomain = f"{subdomain}.{domain}"

    await message.reply_text(f"🔍 **Menambahkan subdomain:** `{full_subdomain}` ➝ `{target_ip}`")

    result = create_subdomain(zone_id, full_subdomain, target_ip)

    if result.get("success"):
        await message.reply_text(f"✅ **Subdomain Berhasil Ditambahkan!**\n🌐 `{full_subdomain} → {target_ip}`")
    else:
        error_msg = result.get("errors", [{"message": "Unknown Error"}])[0]["message"]
        await message.reply_text(f"❌ **Gagal Menambahkan Subdomain**\n⚠️ Error: `{error_msg}`")

@zb.ubot("domainlist")
async def list_domains(client, message, *args):
    domain_list_text = "📜 **Daftar Domain yang Tersedia:**\n"
    for domain in DOMAIN_LIST.keys():
        domain_list_text += f"✅ `{domain}`\n"
    
    await message.reply_text(domain_list_text)
