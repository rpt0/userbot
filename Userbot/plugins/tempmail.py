import requests
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bs4 import BeautifulSoup
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "TempMail"

def help_string(org):
    return h_s(org, "help_tempmail")

sessions_mail = {}

def fetch_json(url):
    try:
        resp = requests.get(url)
        print(resp.text)
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()

@zb.ubot("tempmail")
async def temp_mail(client, message, *args):
    user_id = message.from_user.id

    expired_sessions = [uid for uid, data in sessions_mail.items() if datetime.utcnow() - data["created_at"] > timedelta(minutes=30)]
    for uid in expired_sessions:
        del sessions_mail[uid]

    if user_id in sessions_mail:
        email = sessions_mail[user_id]["email"]
        return await message.reply_text(
            f"✅ Temp Mail Anda:\n📩 Email: `{email}`\n⏳ Tunggu sekitar 5-10 menit sebelum cek.\n\n"
            f"➡ Gunakan perintah `.cekmail` untuk mengecek pesan.\n"
            f"➡ Gunakan perintah `.resetmail` untuk mendapatkan email baru."
        )

    url = f"https://api.botcahx.eu.org/api/tools/create-temp-mail?apikey=Biyy"
    data = fetch_json(url)

    if not data.get("status"):
        return await message.reply_text("⚠️ Gagal membuat email sementara! Coba lagi nanti.")

    email = data["result"]
    sessions_mail[user_id] = {
        "email": email,
        "created_at": datetime.utcnow(),
        "last_checked_at": datetime.utcnow(),
    }

    await message.reply_text(
        f"✅ Temp Mail Anda:\n📩 Email: `{email}`\n⏳ Tunggu sekitar 5-10 menit sebelum cek.\n\n"
        f"➡ Gunakan perintah `.cekmail` untuk mengecek pesan.\n"
        f"➡ Gunakan perintah `.resetmail` untuk mendapatkan email baru."
    )

@zb.ubot("cekmail")
async def check_mail(client, message, *args):
    user_id = message.from_user.id

    if user_id not in sessions_mail:
        return await message.reply_text("⚠️ Anda belum memiliki Temp Mail!\nGunakan `/tempmail` untuk membuatnya.")

    email = sessions_mail[user_id]["email"]
    sessions_mail[user_id]["last_checked_at"] = datetime.utcnow()

    url = f"https://api.botcahx.eu.org/api/tools/cek-msg-tmp-mail?email={email}&apikey=Biyy"
    data = fetch_json(url)

    if not data.get("status"):
        return await message.reply_text("⚠️ Gagal mengambil pesan email!")

    messages = data.get("result", [])
    if not messages:
        return await message.reply_text(f"📭 Belum ada pesan masuk di `{email}`.\n⏳ Coba cek lagi nanti.")

    pesan_list = []
    for msg in messages:
        pengirim = msg.get("sf", "Tidak diketahui")
        subjek = msg.get("s", "Tidak diketahui")
        waktu = msg.get("cr", "Waktu tidak tersedia")
        isi_pesan = msg.get("html") or msg.get("text") or "Tidak ada isi"
        isi_pesan = str(isi_pesan).strip()  # Pastikan isi_pesan adalah string sebelum strip
        
        isi_pesan = extract_text(isi_pesan)

        pesan_list.append(f"""
<blockquote>📬 **Pesan Baru!**
💌 **Dari:** `{pengirim}`
🕒 **Waktu:** `{waktu}`
📚 **Subjek:** {subjek}
📜 **Isi:** `{isi_pesan}`</blockquote>
""")

    hasil = "\n\n".join(pesan_list)
    await message.reply_text(hasil, disable_web_page_preview=True)

@zb.ubot("resetmail")
async def reset_mail(client, message, *args):
    user_id = message.from_user.id

    if user_id in sessions_mail:
        del sessions_mail[user_id]

    url = f"https://api.botcahx.eu.org/api/tools/create-temp-mail?apikey=Biyy"
    data = fetch_json(url)

    if not data.get("status"):
        return await message.reply_text("⚠️ Gagal membuat email baru!")

    email = data["result"]
    sessions_mail[user_id] = {
        "email": email,
        "created_at": datetime.utcnow(),
        "last_checked_at": datetime.utcnow(),
    }

    await message.reply_text(
        f"✅ Temp Mail Baru Anda:\n📩 Email: `{email}`\n⏳ Tunggu sekitar 5-10 menit sebelum cek.\n\n"
        f"➡ Gunakan perintah `.cekmail` untuk mengecek pesan.\n"
        f"➡ Gunakan perintah `.resetmail` untuk mendapatkan email baru."
    )
    
