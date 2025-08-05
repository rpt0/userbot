from datetime import datetime
from time import time

from pyrogram.helpers import ikb, kb
from pyrogram.raw.functions import Ping
from pytz import timezone

from config import DEVS, nama_bot, owner_id
from Userbot import bot, nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import MSG, Button, get_time, zb, start_time

CONFIRM_PAYMENT = []
SUPPORT = []

kata_perintah = "📜 Buat Userbot|⚡ Trial Userbot|📇 Status Akun|🛠️ Cek Fitur|🇲🇨 Bahasa|🧸 Owner|🚀 Updates|👥 Cek User|✅ Setuju|❌ Tidak|🏠 Menu Utama|📃 Saya Setuju|🛠️ Cek Fitur|Start|start|✅ Lanjutkan Buat Userbot|🆘 Dukungan|🔄 Reset Emoji|🔄 Reset Prefix|⬅️ Kembali"
words = kata_perintah.split("|")
wrapped_words = [f'"{word}"' for word in words]
final_result = "[" + ", ".join(wrapped_words) + "]"


async def cb_support(client, m, _):
    user_id = int(m.from_user.id)
    full_name = f"{m.from_user.first_name} {m.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    SUPPORT.append(get.id)
    try:
        button = ikb([[("❌ Batalkan", f"batal {user_id}")]])
        pesan = await bot.ask(
            user_id,
            f"<b>✍️ Tulis pesan anda: {full_name}</b>",
            reply_markup=button,
        )
        if pesan.text in final_result:
            await pesan.delete()
            return await bot.send_message(
                user_id, "<b>Proses di batalkan.</b>", reply_markup=Button.start(m)
            )
    except:
        if get.id in SUPPORT:
            SUPPORT.remove(get.id)
            return await bot.send_message(get.id, "Pembatalan Otomatis")
    text = f"<b>💬 Pesan anda terkirim: {full_name}</b>"
    buttons = ikb(
        [
            [
                ("👤 Akun", f"profil {user_id}"),
                ("💬 Jawab Pesan", f"jawab_pesan {user_id}"),
            ]
        ]
    )
    if get.id in SUPPORT:
        try:
            await pesan.copy(
                owner_id,
                reply_markup=buttons,
            )
            SUPPORT.remove(get.id)
            await pesan.request.edit(f"<b>✍️ Tulis pesan anda: {full_name}</b>")
            if pesan.text in final_result:
                await pesan.delete()
                return await bot.send_message(
                    user_id, "<b>Proses di batalkan.</b>", reply_markup=Button.start(m)
                )
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)


@zb.callback("^jawab_pesan")
async def cb_jwpesan(client, callback_query, _):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    user_ids = int(callback_query.data.split()[1])
    SUPPORT.append(get.id)
    try:
        button = ikb([[("❌ Batalkan", f"batal {user_id}")]])
        pesan = await bot.ask(
            user_id,
            f"<b>✉️ Silakan tulis pesan anda: {full_name}</b>",
            reply_markup=button,
        )
        if pesan.text in final_result:
            await pesan.delete()
            return await bot.send_message(
                user_id,
                "<b>Proses di batalkan.</b>",
                reply_markup=Button.start(callback_query.message),
            )
    except:
        if get.id in SUPPORT:
            SUPPORT.remove(get.id)
            return await bot.send_message(get.id, "Pembatalan Otomatis")
    text = f"<b>✅ Pesan Balasan Terkirim : {full_name}</b>"
    if not user_ids == owner_id:
        buttons = ikb([[("💬 Jawab Pesan", f"jawab_pesan {user_id}")]])
    else:
        buttons = ikb(
            [
                [
                    ("👤 Akun", f"profil {user_id}"),
                    ("💬 Balas Pesan", f"jawab_pesan {user_id}"),
                ]
            ]
        )
    if get.id in SUPPORT:
        try:
            await pesan.copy(
                user_ids,
                reply_markup=buttons,
            )
            SUPPORT.remove(get.id)
            await pesan.request.edit(
                f"<b>✉️ Silakan tulis pesan anda: {full_name}</b>",
            )
            if pesan.text in final_result:
                await pesan.delete()
                return await bot.send_message(
                    user_id,
                    "<b>Proses di batalkan.</b>",
                    reply_markup=Button.start(callback_query.message),
                    disable_web_page_preview=True,
                )
            return await bot.send_message(user_id, text)
        except Exception as error:
            return await bot.send_message(user_id, error)


@zb.callback("^profil")
async def cb_porfil(client, callback_query, _):
    user_id = int(callback_query.data.split()[1])
    try:
        get = await bot.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>👤 <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b> ┣ ID Pengguna:</b> <code>{get.id}</code>\n"
            f"<b> ┣ Nama Depan:</b> {first_name}\n"
        )
        if last_name == "None":
            msg += ""
        else:
            msg += f"<b> ┣ Nama Belakang:</b> {last_name}\n"
        if username == "None":
            msg += ""
        else:
            msg += f"<b> ┣ Username:</b> @{username}\n"
        msg += f"<b> ┗ Bot: {bot.me.mention}\n"
        buttons = ikb([[(f"{full_name}", f"tg://openmessage?user_id={get.id}", "url")]])
        return await callback_query.message.reply_text(msg, reply_markup=buttons)
    except Exception as why:
        return await callback_query.message.reply_text(why)


@zb.callback("^batal")
async def cb_batal(client, callback_query, _):
    user_id = int(callback_query.data.split()[1])
    if user_id in SUPPORT:
        try:
            SUPPORT.remove(user_id)
            await callback_query.message.delete()
            buttons = Button.start(callback_query)
            return await bot.send_message(
                user_id, MSG.START(callback_query), reply_markup=buttons
            )
        except Exception as why:
            await callback_query.message.delete()
            return await bot.send_message(user_id, f"<b>❌ Gagal {why}</b>")


async def cb_start_profile(client, m, _):
    user_id = m.from_user.id
    my_id = []
    _ubot_ = None
    seles = dB.get_list_from_var(client.me.id, "seller", "user")
    for _ubot_ in nlx._my_id:
        my_id.append(_ubot_)
    if user_id in my_id:
        status2 = "aktif"
    else:
        status2 = "tidak aktif"

    if user_id in DEVS:
        status = f"<b>{nama_bot}</b> <code>[owner]</code>"
    elif user_id in seles:
        status = f"<b>{nama_bot}</b> <code>[reseller]</code>"
    else:
        status = f"<b>{nama_bot}</b> <code>[buyer]</code>"
    uptime = await get_time((time() - start_time))
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    (end - start).microseconds / 1000
    exp = dB.get_expired_date(user_id)
    habis = (
        exp.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
        if exp
        else "None"
    )
    prefix = dB.get_pref(user_id)
    keyboard = kb(
        [[("🇲🇨 Bahasa")], [("⬅️ Kembali")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return await m.reply(
        f"""
<blockquote>
<b>{nama_bot}</b>
    <b>Status Ubot:</b> <code>{status2}</code>
      <b>Status Pengguna:</b> <i>{status}</i>
      <b>Prefixes :</b> <code>{prefix[0]}</code>
      <b>Tanggal Kedaluwarsa:</b> <code>{habis}</code>
      <b>Uptime Ubot:</b> <code>{uptime}</code>
</blockquote>
""",
        reply_markup=keyboard,
    )
