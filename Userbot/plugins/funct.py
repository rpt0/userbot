import asyncio
import io
import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
from pyrogram import filters
from pyrogram.errors import (FloodWait, InputUserDeactivated, PeerIdInvalid,
                             UserIsBlocked)
from pyrogram.helpers import ikb, kb
from pytz import timezone

from config import CMD_HELP, bot_username, owner_id
from Userbot import bot, nlx
from Userbot.assistant.buatub import setExpiredUser
from Userbot.helper.database import dB, db_path
from Userbot.helper.tools import Emojik, zb, unpacked4


@zb.bots("restore")
@zb.thecegers
async def _(c, m, _):
    user_id = m.from_user.id
    msg_text = await c.ask(
        user_id,
        "<blockquote><b>Silahkan kirim document file .db!! Dan pastikan nama db_name sesuai dengan config.py</b></blockquote>",
        filters=filters.document,
    )
    document = msg_text.document
    if os.path.exists(db_path):
        os.remove(db_path)
    await c.download_media(document, "./")
    return await m.reply(
        f"<blockquote><b>Sukses melakukan restore database, Silahkan ketik /reboot</blockquote></b>"
    )


@zb.callback("^close")
async def cb_close_hlp(c, cq, _):
    try:
        unPacked = unpacked4(cq.inline_message_id)
        return await c.delete_messages(unPacked.chat_id, unPacked.message_id)
    except:
        pass


@zb.callback("^close_mbot")
async def cb_close(c, cq, _):
    return await cq.message.delete()


@zb.bots("addprem")
@zb.seller
async def _(c: bot, m, _):
    return await add_prem_user(c, m, _)


@zb.ubot("addprem")
@zb.thecegers
async def _(c: nlx, m, _):
    kon = m.from_user.id
    seles = dB.get_list_from_var(bot.me.id, "seller", "user")
    if kon not in seles:
        return
    return await add_prem_user(c, m, _)


async def add_prem_user(c, message, _):
    user_id, get_bulan = await c.extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"<b>{message.text} [user_id/username - bulan]</b>")
    try:
        get_id = (await c.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_bulan:
        get_bulan = 1
    premium = dB.get_list_from_var(bot.me.id, "PREM", "USERS")
    if get_id in premium:
        return await message.reply(
            f"Pengguna denga ID : `{get_id}` sudah memiliki akses !"
        )
    triala = dB.get_list_from_var(bot.me.id, "user_trial", "user")

    dB.add_to_var(bot.me.id, "PREM", get_id, "USERS")
    if get_id in triala:
        dB.remove_from_var(bot.me.id, "user_trial", get_id, "user")
    if not dB.get_expired_date(get_id):
        await setExpiredUser(get_id)
    await message.reply(
        f"✅  <b>Akses diberikan kepada {get_id}!!. Silahkan ke {bot_username} untuk membuat userbot</b>"
    )
    try:
        await bot.send_message(
            get_id,
            f"Selamat ! Akun anda sudah memiliki akses untuk pembuatan userbot",
            reply_markup=kb(
                [[("✅ Lanjutkan Buat Userbot")]],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
    except:
        pass
    return await bot.send_message(
        owner_id,
        f"• {message.from_user.id} ─> {get_id} •",
        reply_markup=ikb(
            [
                [
                    ("👤 Account", f"profil {message.from_user.id}"),
                    ("Account 👤", f"profil {get_id}"),
                ]
            ]
        ),
    )


@zb.bots("unprem")
@zb.seller
async def _(c: bot, m, _):
    return await un_prem_user(c, m, _)


@zb.ubot("unprem")
@zb.thecegers
async def _(c: nlx, m, _):
    kon = m.from_user.id
    seles = dB.get_list_from_var(bot.me.id, "seller", "user")
    if kon not in seles:
        return
    return await un_prem_user(c, m, _)


async def un_prem_user(c, message, _):
    user_id = await c.extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await c.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    delpremium = dB.get_list_from_var(bot.me.id, "PREM", "USERS")

    if user.id not in delpremium:
        return await message.reply("Tidak ditemukan")
    dB.remove_from_var(bot.me.id, "PREM", user.id, "USERS")
    return await message.reply(f" ✅ {user.mention} berhasil dihapus")


@zb.bots("listprem")
@zb.thecegers
async def get_prem_user(c: bot, message, _):
    text = ""
    count = 0
    for user_id in dB.get_list_from_var(bot.me.id, "PREM", "USERS"):
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        return await message.reply_text("Tidak ada pengguna yang ditemukan")
    else:
        return await message.reply_text(text)


@zb.bots("addseller")
@zb.thecegers
async def _(c: bot, m, _):
    return await add_seller(c, m, _)


@zb.ubot("addseller")
@zb.thecegers
async def _(c: nlx, m, _):
    kon = m.from_user.id
    seles = dB.get_list_from_var(bot.me.id, "seller", "user")
    if kon not in seles:
        return
    return await add_seller(c, m, _)


async def add_seller(c, message, _):
    user = None
    user_id = await c.extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await c.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    seles = dB.get_list_from_var(bot.me.id, "seller", "user")
    if user.id in seles:
        return await message.reply("Sudah menjadi reseller.")

    dB.add_to_var(bot.me.id, "seller", user.id, "user")
    return await message.reply(f"✅ {user.mention} telah menjadi reseller")


@zb.bots("unseller")
@zb.thecegers
async def _(c: bot, m, _):
    return await un_seller(c, m, _)


@zb.ubot("unseller")
@zb.thecegers
async def _(c: nlx, m, _):
    kon = m.from_user.id
    seles = dB.get_list_from_var(bot.me.id, "seller", "user")
    if kon not in seles:
        return
    return await un_seller(c, m, _)


async def un_seller(c, message, _):
    user = None
    user_id = await c.extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await c.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    seles = dB.get_list_from_var(bot.me.id, "seller", "user")
    if user.id not in seles:
        return await message.reply("Tidak ditemukan")
    dB.remove_from_var(bot.me.id, "seller", user.id, "user")
    return await message.reply(f"{user.mention} berhasil dihapus")


@zb.bots("listseller")
@zb.thecegers
async def get_seles_user(c: bot, message, _):
    text = ""
    count = 0
    seles = dB.get_list_from_var(bot.me.id, "seller", "user")
    for user_id in seles:
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        return await message.reply_text("Tidak ada pengguna yang ditemukan")
    else:
        return await message.reply_text(text)


@zb.bots("setexpired")
@zb.seller
async def _(c: bot, message, _):
    user_id, get_day = await c.extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"{message.text} user_id/username - hari")
    try:
        get_id = (await c.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    dB.set_expired_date(user_id, expire_date)
    return await message.reply(f"{get_id} telah diaktifkan selama {get_day} hari.")


@zb.bots("cek|cekexpired")
@zb.seller
async def _(c: bot, message, _):
    user_id = await c.extract_user(message)
    if not user_id:
        return await message.reply("Pengguna tidak ditemukan")
    expired_date = dB.get_expired_date(user_id)
    if not expired_date:
        return await message.reply(f"{user_id} belum diaktifkan.")
    expir = expired_date.astimezone(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
    return await message.reply(f"{user_id} aktif hingga {expir}.")


@zb.bots("unexpired")
@zb.seller
async def _(c: bot, message, _):
    user = None
    user_id = await c.extract_user(message)
    if not user_id:
        return await message.reply("User tidak ditemukan")
    try:
        user = await c.get_users(user_id)
    except Exception as error:
        return await message.reply(str(error))
    dB.rem_expired_date(user.id)
    return await message.reply(f"✅ {user.id} expired telah dihapus")


@zb.bots("bcast|broadcast|bacot")
@zb.thecegers
async def bacotan(c, message, _):
    await message.delete()
    brod = dB.get_list_from_var(bot.me.id, "BROADCAST")
    y = None
    x = None
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    if len(message.command) > 1:
        return await message.reply(
            "<b>Silakan sertakan pesan atau balas pesan yang ingin disiarkan.</b>"
        )
    gl = 0
    kntl = 0
    jmbt = len(brod)
    for i in brod:
        try:
            m = (
                await bot.forward_messages(i, y, x)
                if message.reply_to_message
                else await bot.send_message(i, y, x)
            )
            kntl += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            m = (
                await bot.forward_messages(i, y, x)
                if message.reply_to_message
                else await bot.send_message(i, y, x)
            )
            kntl += 1
        except UserIsBlocked:
            dB.remove_from_var(bot.me.id, "BROADCAST", i)
            gl += 1
            continue
        except PeerIdInvalid:
            dB.remove_from_var(bot.me.id, "BROADCAST", i)
            gl += 1
            continue
        except InputUserDeactivated:
            dB.remove_from_var(bot.me.id, "BROADCAST", i)
            gl += 1
            continue
    return await message.reply(
        f"<b>Berhasil mengirim pesan ke `{kntl}` pengguna, gagal ke `{gl}` pengguna, dari `{jmbt}` pengguna.</b>",
    )


@zb.bots("top")
# @zb.thecegers
async def _(c: bot, m, _):
    return await get_top_module(c, m, _)


@zb.ubot("top")
# @zb.thecegers
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    return await get_top_module(c, m, _)


"""
async def get_top_module(client, message, _):
    vars = dB.all_var(bot.me.id, "MODULES")
    # Convert string counts to integers
    sorted_vars = sorted(vars.items(), key=lambda item: int(item[1]), reverse=True)

    command_count = 999
    text = message.text.split()

    if len(text) == 2:
        try:
            command_count = min(max(int(text[1]), 1), 10)
        except ValueError:
            pass
    # Sum the integer values now
    total_count = sum(int(count) for _, count in sorted_vars[:command_count])

    txt = "<b>📊 Top Command</b>\n\n"
    for command, count in sorted_vars[:command_count]:
        txt += f"<b> •> {command} : {count}</b>\n"

    txt += f"\n<b>📈 Total: {total_count} Commands</b>"

    return await message.reply(txt)
"""


async def get_top_module(client, message, _):
    vars = dB.all_var(bot.me.id, "MODULES")
    sorted_vars = sorted(vars.items(), key=lambda item: int(item[1]), reverse=True)
    filtered_vars = [
        (command, count) for command, count in sorted_vars if int(count) > 50
    ]

    command_count = 999
    text = message.text.split()
    if len(text) == 2:
        try:
            command_count = min(max(int(text[1]), 1), 10)
        except ValueError:
            pass

    top_commands = filtered_vars[:command_count]
    total_count = sum(int(count) for i, count in sorted_vars[:command_count])

    txt = "<b>📊 Top Command</b>\n\n"
    txt += f"\n➡️ Diatas adalah data dari banyak nya command yang digunakan dari {len(CMD_HELP)} Module"
    txt += f"\n<b>📈 Total: {total_count} Commands</b>"

    if top_commands:
        graph = create_graph(top_commands)
        return await client.send_photo(
            chat_id=message.chat.id,
            photo=graph,
            caption=f"<b><blockquote>{txt}</blockquote></b>",
        )
    else:
        return await message.reply("<b>No commands with count greater than 50.</b>")


def create_graph(data):
    commands = [item[0].capitalize() for item in data]
    counts = [int(item[1]) for item in data]
    max_count = max(counts)
    colors = []

    for count in counts:
        if count == max_count:
            colors.append("blue")  # Warna biru untuk count tertinggi
        elif count > max_count * 0.5:
            colors.append("green")  # Warna hijau untuk count di atas 70% dari max
        elif count > max_count * 0.3:
            colors.append("yellow")  # Warna kuning untuk count di atas 40% dari max
        else:
            colors.append("red")  # Warna merah untuk count yang paling rendah

    plt.figure(figsize=(12, 8))
    bars = plt.bar(commands, counts, color=colors)
    plt.ylabel("Counts")
    plt.xlabel("Commands")
    plt.title("Top Command")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Mengatur label agar berada di atas batang
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2, yval, int(yval), va="bottom", ha="center"
        )

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    plt.close()
    return buf


@zb.bots("addultra")
@zb.seller
async def _(c: bot, m, _):
    return await add_ultra_user(c, m, _)


@zb.ubot("addultra")
@zb.seller
async def _(c: nlx, m, _):
    return await add_ultra_user(c, m, _)


async def add_ultra_user(c, message, _):
    user_id, get_bulan = await c.extract_user_and_reason(message)
    if not user_id:
        return await message.reply(f"<b>{message.text} [user_id/username - bulan]</b>")
    try:
        get_id = (await c.get_users(user_id)).id
    except Exception as error:
        return await message.reply(str(error))
    if not get_bulan:
        get_bulan = 1
    ultraium = dB.get_list_from_var(bot.me.id, "PREM", "USERS")
    if get_id in ultraium:
        return await message.reply(
            f"Pengguna denga ID : `{get_id}` sudah memiliki akses !"
        )
    triala = dB.get_list_from_var(bot.me.id, "user_trial", "user")

    dB.add_to_var(bot.me.id, "PREM", get_id, "USERS")
    dB.add_to_var(bot.me.id, "USER_PREMIUM", get_id)
    if get_id in triala:
        dB.remove_from_var(bot.me.id, "user_trial", get_id, "user")
    if not dB.get_expired_date(get_id):
        await setExpiredUser(get_id)
    await message.reply(f"✅  <b>Akses diberikan kepada {get_id}!!")
    try:
        await bot.send_message(
            get_id,
            f"Selamat ! Akun anda sudah memiliki akses untuk pembuatan userbot",
            reply_markup=kb(
                [[("✅ Lanjutkan Buat Userbot")]],
                resize_keyboard=True,
                one_time_keyboard=True,
            ),
        )
    except:
        pass
    return await bot.send_message(
        owner_id,
        f"• {message.from_user.id} ─> {get_id} •",
        reply_markup=ikb(
            [
                [
                    ("👤 Account", f"profil {message.from_user.id}"),
                    ("Account 👤", f"profil {get_id}"),
                ]
            ]
        ),
    )


@zb.bots("unultra")
@zb.seller
async def _(c: bot, m, _):
    return await un_ultra_user(c, m, _)


@zb.ubot("unultra")
@zb.seller
async def _(c: nlx, m, _):
    return await un_ultra_user(c, m, _)


async def un_ultra_user(c, message, _):
    user_id = await c.extract_user(message)
    if not user_id:
        return await message.reply("Balas pesan pengguna atau berikan user_id/username")
    try:
        user = await c.get_users(user_id)
    except Exception as error:
        await message.reply(str(error))
    delultraium = dB.get_list_from_var(bot.me.id, "USER_PREMIUM")

    if user.id not in delultraium:
        return await message.reply("Tidak ditemukan")
    dB.remove_from_var(bot.me.id, "USER_PREMIUM", user.id)
    return await message.reply(f" ✅ {user.mention} berhasil dihapus")


@zb.bots("listultra")
@zb.thecegers
async def get_ultra_user(c: bot, message, _):
    text = ""
    count = 0
    for user_id in dB.get_list_from_var(bot.me.id, "USER_PREMIUM"):
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"{userlist}\n"
    if not text:
        return await message.reply_text("Tidak ada pengguna yang ditemukan")
    else:
        return await message.reply_text(text)

@zb.bots("joinseller")
async def _(c: bot, m, _):
    await m.reply( 
        f"""
<blockquote><b>Rules For Reseller!</b>
 - Memiliki basic dasar untuk berjualan.
 - Bertanggung jawab.
 - Tidak menjual(Seller) Userbot ditempat lain Only KingUserVip.
 - Dilarang keras melakukan penipuan mengatas namakan KingUserVip.
 - Memiliki Bank / E-wallet / Allpayy untuk transaksi.

Keuntungan Reseller:
 - Mendapatkan harga seller yang lebih under yaitu Rp. 25.000/perbulan | Rp. 60.000/permanen dan anda bisa menjual Userbot di harga Rp.10.000 - Rp.15.000.
 - Diberi akses seller Userbot jadi tidak perlu ribet menunggu owner Userbot untuk memberi akses pembeli.
 - Diajari cara kerja Userbot ini digrup khusus seller jika anda belum mengerti.
 - Dalam grup tidak hanya menjual Userbot saja banyak bot lain lain dan jajanan telegram yang bisa kalian sharing antara seller Userbot.

Jika Setuju dengan seluruh rules
Hubungi contact untuk mendaftar
Contact : @Priaindiareal</b></blockquote>""")
