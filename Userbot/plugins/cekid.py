import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyrogram import Client
from pyrogram.types import Message, User, Chat
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx
from io import BytesIO

__MODULES__ = "Cekid"


def help_string(org):
    return h_s(org, "help_cekid")

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEFAULT_PROFILE_PATH = "Userbot/default.jpg"

def download_image():
    if os.path.exists(DEFAULT_PROFILE_PATH):
        return Image.open(DEFAULT_PROFILE_PATH).convert("RGBA").resize((140, 140))
    else:
        print("Error: File default.jpg tidak ditemukan.")
        return None

async def generate_profile_card(client: Client, user: User):
    width, height = 800, 400
    bg_color = (30, 30, 40)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    frame_color = (50, 50, 70)
    draw.rounded_rectangle([(20, 20), (780, 380)], radius=30, fill=frame_color)

    profile_size = 140
    profile_x, profile_y = 60, 130
    profile_photo = None

    def get_safe_value(user, attr, default="Tidak diketahui"):
        return getattr(user, attr, default) if isinstance(user, User) else default

    first_name = get_safe_value(user, "first_name", "Pengguna")
    username = get_safe_value(user, "username", None)
    username_text = f"@{username}" if username else "Tidak ada"
    dc_id = get_safe_value(user, "dc_id")
    is_premium = "Iya" if get_safe_value(user, "is_premium", False) else "Tidak"

    has_profile_photo = False
    profile_photo_path = f"downloads/profile_photo_{user.id}.jpg"
    
    async for photo in client.get_chat_photos(user.id, limit=1):
        await client.download_media(photo.file_id, file_name=profile_photo_path)
        has_profile_photo = True
        break

    if has_profile_photo and os.path.exists(profile_photo_path):
        profile_photo = Image.open(profile_photo_path).convert("RGBA").resize((profile_size, profile_size))
    else:
        profile_photo = download_image()

    if profile_photo:
        mask = Image.new("L", (profile_size, profile_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, profile_size, profile_size), fill=255)
        profile_photo = ImageOps.fit(profile_photo, (profile_size, profile_size))
        profile_photo.putalpha(mask)
        img.paste(profile_photo, (profile_x, profile_y), profile_photo)

    font_title = ImageFont.truetype(FONT_PATH, 36)
    font_text = ImageFont.truetype(FONT_PATH, 24)
    draw.text((230, 40), "TELEGRAM ID CARD", font=font_title, fill=(255, 220, 100))

    details = [
        ("Nama", first_name),
        ("User ID", str(user.id)),
        ("Username", username_text),
        ("DC ID", str(dc_id)),
        ("Premium?", is_premium),
    ]

    label_color = (200, 200, 200)
    value_color = (173, 216, 230)
    y_text = 100
    for label, value in details:
        draw.text((230, y_text), f"{label}:", font=font_text, fill=label_color)
        draw.text((400, y_text), value, font=font_text, fill=value_color)
        y_text += 50

    save_dir = "./downloads"
    os.makedirs(save_dir, exist_ok=True)
    final_path = os.path.join(save_dir, f"profile_card_{user.id}.jpg")
    img.save(final_path, "JPEG")

    return final_path

@zb.ubot("cekid")
async def cekidte(client, message, *args):
    user = message.from_user
    target_user = user

    if message.reply_to_message:
        replied_user = message.reply_to_message.from_user
        if replied_user:
            target_user = replied_user

    if len(message.text.split()) > 1:
        try:
            user_target = await client.get_users(message.text.split()[1])
            target_user = user_target
        except:
            return await message.reply("<b>❌ Pengguna tidak ditemukan</b>")

    name_link = f'<a href="tg://user?id={target_user.id}">{target_user.first_name}</a>'
    digit_info = f"({len(str(target_user.id))} digit)"

    waiting_msg = await message.reply("**__⏳ Tunggu sebentar!__**")

    profile_card_path = await generate_profile_card(client, target_user)

    chat_title = message.chat.title if isinstance(message.chat, Chat) else "Private Chat"
    username_text = f"@{target_user.username}" if target_user.username else "Tidak ada"

    msg = f"""
<blockquote><b>╭──「 🔍 INFORMASI TELEGRAM 」</b>
│ 👤 <b>Nama Pengguna:</b> {name_link}
│ 🆔 <b>User ID:</b> <code>{target_user.id}</code> {digit_info}
│ 📌 <b>Username:</b> {username_text}
│ 🏷️ <b>Data Center ID:</b> <code>{target_user.dc_id or 'Tidak diketahui'}</code>
│ 💠 <b>Premium Telegram:</b> { "Ya ✅" if getattr(target_user, 'is_premium', False) else "Tidak ❌"}
│ 📍 <b>Chat ID:</b> <code>{message.chat.id}</code> ({chat_title})
│ 🔗 <b>Link Profil:</b> <a href="tg://user?id={target_user.id}">Klik Disini</a>
╰──「 <b>By @{client.me.username}</b> 」</blockquote>
"""

    if profile_card_path:
        await waiting_msg.delete()
        await message.reply_photo(profile_card_path, caption=msg, quote=True)
        os.remove(profile_card_path)

        if os.path.exists(profile_photo_path):
            os.remove(profile_photo_path)
    else:
        await waiting_msg.edit_text("❌ Gagal membuat kartu profil! Pastikan default.jpg tersedia.", disable_web_page_preview=True)
        
