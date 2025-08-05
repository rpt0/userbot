import asyncio
from gc import get_objects

from pyrogram.errors import PeerIdInvalid
from pyrogram.helpers import ikb, kb

from config import bot_id, owner_id
from Userbot import bot, nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (MSG, Button, create_inline_keyboard,
                                  extract_ids_from_link, get_msg_button, human,
                                  zb, org_kontol)
import aiohttp
import os
import filetype
from pyrogram import filters
from Userbot import owner_id, bot_id
from pyrogram.types import Message, User
from PIL import Image, ImageDraw, ImageFont, ImageOps

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CARD_BG_PATH = "Userbot/picture/Artboard 1.png"

flood3 = {}

async def upload_to_catbox(m: Message):
    media = await m.reply_to_message.download()
    try:
        with open(media, "rb") as file:
            file_data = file.read()
            ext = filetype.guess_extension(file_data) or "jpg"
        form_data = aiohttp.FormData()
        form_data.add_field("fileToUpload", open(media, "rb"), filename=f"file.{ext}")
        form_data.add_field("reqtype", "fileupload")
        async with aiohttp.ClientSession() as session:
            async with session.post("https://catbox.moe/user/api.php", data=form_data) as res:
                if res.status == 200:
                    url = await res.text()
                    return url.strip()
                else:
                    return None
    finally:
        os.remove(media)

def download_card_bg():
    if os.path.exists(CARD_BG_PATH):
        return Image.open(CARD_BG_PATH).convert("RGBA").resize((800, 400))
    else:
        print("Error: Artboard 1.png tidak ditemukan.")
        return Image.new("RGBA", (800, 400), (30, 30, 40, 255))

async def generate_profile_card(client, user):
    width, height = 800, 400
    img = download_card_bg()
    draw = ImageDraw.Draw(img)
    profile_size = 140
    profile_x, profile_y = 60, 130

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
        profile_photo = Image.new("RGBA", (profile_size, profile_size), (200, 200, 200, 255))

    if profile_photo:
        mask = Image.new("L", (profile_size, profile_size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, profile_size, profile_size), fill=255)
        profile_photo = ImageOps.fit(profile_photo, (profile_size, profile_size))
        profile_photo.putalpha(mask)
        img.paste(profile_photo, (profile_x, profile_y), profile_photo)

    font_title = ImageFont.truetype(FONT_PATH, 36)
    font_text = ImageFont.truetype(FONT_PATH, 24)
    draw.text((230, 40), " ", font=font_title, fill=(255, 220, 100))

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
        draw.text((260, y_text), f"{label}:", font=font_text, fill=label_color) 
        draw.text((430, y_text), value, font=font_text, fill=value_color) 
        y_text += 50

    save_dir = "./downloads"
    os.makedirs(save_dir, exist_ok=True)
    final_path = os.path.join(save_dir, f"profile_card_{user.id}.jpg")
    img = img.convert("RGB")
    img.save(final_path, "JPEG")

    if os.path.exists(profile_photo_path):
        os.remove(profile_photo_path)
    return final_path

async def send_msg_to_owner(c, m, _):
    if m.from_user.id == owner_id:
        return
    else:
        buttons = ikb(
            [
                [
                    ("👤 Akun", f"profil {m.from_user.id}"),
                    ("💬 Kirim Pesan", f"jawab_pesan {m.from_user.id}"),
                ]
            ]
        )
        try:
            return await c.send_message(
                owner_id,
                f"<a href=tg://user?id={m.from_user.id}>{m.from_user.first_name} {m.from_user.last_name or ''}</a>\n\n<code>{m.text}</code>",
                reply_markup=buttons,
            )
        except Exception:
            pass


async def send_restart_owner(c, m, _):
    if m.from_user.id == owner_id:
        return
    else:
        buttons = ikb(
            [
                [
                    ("👤 Akun", f"profil {m.from_user.id}"),
                    ("💬 Kirim Pesan", f"jawab_pesan {m.from_user.id}"),
                ]
            ]
        )
        try:
            return await c.send_message(
                owner_id,
                f"<b> Telah melakukan Restart <a href=tg://user?id={m.from_user.id}>{m.from_user.first_name} {m.from_user.last_name or ''}</a></b>",
                reply_markup=buttons,
            )
        except Exception:
            pass


@zb.bots("btch", human.pv)
async def _(c, m, _):
    link = m.text.split(None, 1)[1]
    tujuan, _id = extract_ids_from_link(link)
    txt = dB.get_var(m.from_user.id, "toprem")
    teks, button = get_msg_button(txt)
    if button:
        button = create_inline_keyboard(button)
    dB.remove_var(m.from_user.id, "toprem")
    return await c.edit_message_reply_markup(
        chat_id=tujuan, message_id=_id, reply_markup=button
    )


@zb.bots("bluser")
@zb.seller
async def _(c: bot, m, _):
    blus = dB.get_list_from_var(c.me.id, "BLUSER")
    if len(m.command) > 1:
        user_id = await c.extract_user(m)
        try:
            org = await bot.get_users(user_id)
            if org.id in blus:
                return await m.reply_text("Pengguna sudah didalam blacklist.")
            dB.add_to_var(bot_id, "BLUSER", org.id)
            return await m.reply_text("Added to blacklist-users.")
        except PeerIdInvalid:
            org = user_id
            if org in blus:
                return await m.reply_text("Pengguna sudah didalam blacklist.")
            dB.add_to_var(bot_id, "BLUSER", org)
            return await m.reply_text("Added to blacklist-users.")
    else:
        if not m.reply_to_message.from_user.id:
            return
        user_id = m.reply_to_message.from_user.id
        if user_id in blus:
            return await m.reply_text("Pengguna sudah didalam blacklist.")
        dB.add_to_var(bot_id, "BLUSER", user_id)
        return await m.reply_text("Added to blacklist-user.")


@zb.bots("listbluser")
@zb.seller
async def _(c, m, _):
    blus = dB.get_list_from_var(bot_id, "BLUSER")
    if blus == []:
        return await m.reply_text("Belum ada pengguna yang diblacklist!!")
    text = ""
    for count, chat_id in enumerate(blus, 1):
        text += "<b>• {}. [<code>{}</code>]</b>\n".format(count, chat_id)
    return await m.reply_text(text)


@zb.bots("unbluser")
@zb.seller
async def _(c: bot, m, _):
    blus = dB.get_list_from_var(bot_id, "BLUSER")
    if len(m.command) > 1:
        user_id = await c.extract_user(m)
        org = await bot.get_users(user_id)

        if org.id not in blus:
            return await m.reply_text("Pengguna tidak didalam blacklist.")
        dB.remove_from_var(bot_id, "BLUSER", org.id)
        return await m.reply_text("Remove from blacklist-users.")
    else:
        user_id = m.reply_to_message.from_user.id
        if user_id not in blus:
            return await m.reply_text("Pengguna tidak didalam blacklist.")
        dB.remove_from_var(bot_id, "BLUSER", org.id)
        return await m.reply_text("Remove from blacklist-user.")


async def start_private(c, msg, _):
    brod = dB.get_list_from_var(bot_id, "BROADCAST")
    if msg.from_user.id not in brod:
        dB.add_to_var(c.me.id, "BROADCAST", msg.from_user.id)
    await send_msg_to_owner(c, msg, _)
    buttons = Button.start(msg)
    msge = MSG.START(msg)
    return await msg.reply(msge, reply_markup=buttons, disable_web_page_preview=True)


@bot.on_message(filters.command("setpicstart", prefixes=[".", "/"]) & filters.user(owner_id))
async def setpicstart_command(client, message: Message):
    if len(message.command) > 1 and message.command[1].lower() == "card":
        dB.set_var(bot_id, "START_PIC", "card")
        return await message.reply("✅ Mode start card berhasil diaktifkan!")

    if not message.reply_to_message:
        return await message.reply("Reply ke media (foto/video/sticker) yang ingin dijadikan gambar start.")

    r = message.reply_to_message
    if r.sticker:
        dB.set_var(bot_id, "START_PIC", f"sticker:{r.sticker.file_id}")
        return await message.reply("✅ Sticker start berhasil diubah!")
    elif r.photo:
        await message.reply("Uploading photo, tunggu sebentar...")
        url = await upload_to_catbox(message)
        if url:
            dB.set_var(bot_id, "START_PIC", url)
            await message.reply(f"✅ Gambar start berhasil diubah!\nURL: {url}")
        else:
            await message.reply("❌ Gagal upload photo!")
    elif r.video:
        await message.reply("Uploading video, tunggu sebentar...")
        url = await upload_to_catbox(message)
        if url:
            dB.set_var(bot_id, "START_PIC", url)
            await message.reply(f"✅ Video start berhasil diubah!\nURL: {url}")
        else:
            await message.reply("❌ Gagal upload video!")
    else:
        await message.reply("Unsupported! Hanya photo, video, atau sticker.")

@zb.bots("start", human.pv)
@zb.menten
@org_kontol
async def _(c, msg, _):
    await send_msg_to_owner(c, msg, _)
    brod = dB.get_list_from_var(bot_id, "BROADCAST")
    if msg.from_user.id not in brod:
        dB.add_to_var(c.me.id, "BROADCAST", msg.from_user.id)
    blus = dB.get_list_from_var(bot_id, "BLUSER")
    org = msg.from_user
    if int(org.id) in flood3:
        flood3[int(org.id)] += 1
    else:
        flood3[int(org.id)] = 1
    if flood3[int(org.id)] > 10:
        del flood3[int(org.id)]
        if org.id not in blus:
            dB.add_to_var(bot_id, "BLUSER", org.id)
        return await msg.reply_text(
            f"**SPAM DETECTED, ✅ BLOCKED USER AUTOMATICALLY!**"
        )
    if len(msg.command) < 2:
        buttons = Button.start(msg)
        msge = MSG.START(msg)
        start_pic = dB.get_var(bot_id, "START_PIC")
        if start_pic:
            if start_pic == "card":
                profile_card_path = await generate_profile_card(c, msg.from_user)
                await msg.reply_photo(
                    profile_card_path,
                    caption=msge,
                    reply_markup=buttons,
#                    quote=True,
                )
                os.remove(profile_card_path)
                return
            #@moire_mor
            if start_pic.startswith("sticker:"):
                sticker_id = start_pic.replace("sticker:", "", 1)
                await msg.reply_sticker(sticker_id)
                return await msg.reply(
                    msge, reply_markup=buttons, disable_web_page_preview=True
                )
            elif start_pic.startswith("http"):
                if any(start_pic.endswith(x) for x in [".mp4", ".webm"]):
                    return await msg.reply_video(
                        start_pic, caption=msge, reply_markup=buttons
                    )
                else:
                    return await msg.reply_photo(
                        start_pic, caption=msge, reply_markup=buttons
                    )
        return await msg.reply_photo(
            "https://files.catbox.moe/2fid5g.mp4", caption=msge, reply_markup=buttons
        )
    else:
        txt = msg.text.split(None, 1)[1]
        msg_id = txt.split("_", 1)[1]
        send = await msg.reply(_("proses_1"))
        if "secretMsg" in txt:
            try:
                m = [obj for obj in get_objects() if id(obj) == int(msg_id)][0]
            except Exception as error:
                return await send.edit(_("err_1".format(error)))
            user_or_me = [m.reply_to_message.from_user.id, m.from_user.id]
            if msg.from_user.id not in user_or_me:
                return await send.edit(
                    f"<b>❌ Ahahahahahaha <a href=tg://user?id={msg.from_user.id}>{msg.from_user.first_name} {msg.from_user.last_name or ''}</a>"
                )
            else:
                text = await c.send_message(
                    msg.chat.id,
                    m.text.split(None, 1)[1],
                    protect_content=True,
                    reply_to_message_id=msg.id,
                )
                await send.delete()
                await asyncio.sleep(120)
                await msg.delete()
                return await text.delete()


async def reset_prefixes(c: bot, m, _):
    mepref = [".", "!", "-", "+"]
    pros = await m.reply("<b>Processing...</b>")
    if m.from_user.id not in nlx._my_id:
        return await pros.edit(
            "<b>ANAK DAJJAL !! SADAR DIRI LAG GOBLOK. LO TUH BUKAN PENGGUNA GW, DASAR MMG GA TAU DIRI LO . BAJINGAN, DAJJAL.</b>"
        )
    gw = next((x for x in nlx._ubot), None)
    gw.set_prefix(m.from_user.id, mepref)
    dB.set_pref(m.from_user.id, mepref)
    key = kb([[("⬅️ Kembali")]], resize_keyboard=True, one_time_keyboard=True)
    await pros.delete()
    return await m.reply(
        f"<b>Prefix lo berhasil direset menjadi {' '.join(mepref)} .</b>",
        reply_markup=key,
    )


async def reset_emoji(c: bot, m, _):
    pros = await m.reply("<b>Processing...</b>")
    if m.from_user.id not in nlx._my_id:
        return await pros.edit(
            "<b>ANAK DAJJAL !! SADAR DIRI LAG GOBLOK. LO TUH BUKAN PENGGUNA GW, DASAR MMG GA TAU DIRI LO . BAJINGAN, DAJJAL.</b>"
        )
    delete_emoji(m)
    await pros.edit("<b>Running for reset costum emoji, please wait 2 minutes...</b>")
    await asyncio.sleep(2)
    change_emoji(m)
    await pros.edit("<b>Setting costum emoji for you...</b>")
    await asyncio.sleep(1)
    key = kb([[("⬅️ Kembali")]], resize_keyboard=True, one_time_keyboard=True)
    await pros.delete()
    return await m.reply("<b>Finished reseting costum emoji...</b>", reply_markup=key)


def delete_emoji(msg):
    dia = msg.from_user
    dB.remove_var(dia.id, "emo_ping")
    dB.remove_var(dia.id, "emo_pong")
    dB.remove_var(dia.id, "emo_proses")
    dB.remove_var(dia.id, "emo_sukses")
    dB.remove_var(dia.id, "emo_gagal")
    dB.remove_var(dia.id, "emo_profil")
    dB.remove_var(dia.id, "emo_owner")
    dB.remove_var(dia.id, "emo_warn")
    dB.remove_var(dia.id, "emo_block")


def change_emoji(msg):
    dia = msg.from_user
    ping_ = dB.get_var(dia.id, "emo_ping")
    pong_ = dB.get_var(dia.id, "emo_pong")
    proses_ = dB.get_var(dia.id, "emo_proses")
    sukses_ = dB.get_var(dia.id, "emo_sukses")
    gagal_ = dB.get_var(dia.id, "emo_gagal")
    profil_ = dB.get_var(dia.id, "emo_profil")
    alive_ = dB.get_var(dia.id, "emo_owner")
    warn_ = dB.get_var(dia.id, "emo_warn")
    block_ = dB.get_var(dia.id, "emo_block")
    ping = "🏓"
    ping_id = int("5258330865674494479")
    pong = "🥵"
    pong_id = int("5258501105293205250")
    proses = "🔄"
    proses_id = int("5427181942934088912")
    gagal = "❌"
    gagal_id = int("5260342697075416641")
    sukses = "✅"
    sukses_id = int("5260416304224936047")
    profil = "👤"
    profil_id = int("5258011929993026890")
    alive = "⭐"
    alive_id = int("5258165702707125574")
    warn = "❗"
    warn_id = int("5260249440450520061")
    block = "🚫"
    block_id = int("5258362429389152256")
    if not (ping_, pong_, proses_, sukses_, gagal_, profil_, alive_, warn_, block_):
        if dia.is_premium == True:
            dB.set_var(dia.id, "emo_ping", ping_id)

            dB.set_var(dia.id, "emo_pong", pong_id)

            dB.set_var(dia.id, "emo_proses", proses_id)

            dB.set_var(dia.id, "emo_gagal", gagal_id)

            dB.set_var(dia.id, "emo_sukses", sukses_id)

            dB.set_var(dia.id, "emo_profil", profil_id)

            dB.set_var(dia.id, "emo_owner", alive_id)

            dB.set_var(dia.id, "emo_warn", warn_id)

            dB.set_var(dia.id, "emo_block", block_id)

        elif dia.is_premium == False:
            dB.set_var(dia.id, "emo_ping", ping)

            dB.set_var(dia.id, "emo_pong", pong)

            dB.set_var(dia.id, "emo_proses", proses)

            dB.set_var(dia.id, "emo_gagal", gagal)

            dB.set_var(dia.id, "emo_sukses", sukses)

            dB.set_var(dia.id, "emo_profil", profil)

            dB.set_var(dia.id, "emo_owner", alive)

            dB.set_var(dia.id, "emo_warn", warn)

            dB.set_var(dia.id, "emo_block", block)
