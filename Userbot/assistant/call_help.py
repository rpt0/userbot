import asyncio
import os
import re
import sys
from gc import get_objects
from time import time

import psutil
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.helpers import InlineKeyboard, ikb
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            ReplyKeyboardRemove)

from config import CMD_HELP, log_userbot, nama_bot, owner_id
from Userbot import bot, nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (INLINE, Button, cek_tg,
                                  create_inline_keyboard, escape_tag,
                                  gens_font, get_msg_button, get_time, human,
                                  zb, org_kontol, paginate_modules,
                                  parse_words, query_fonts, start_time)
from Userbot.plugins.copy_con import COPY_ID
from Userbot.plugins.eval import cb_gitpull
from Userbot.plugins.pmpermit import DEFAULT_TEXT, LIMIT

from .buatub import cb_bahan, cb_bayar_dulu, cb_trial, cek_ubot
from .call_lang import atur_bahasa
from .call_prof import cb_start_profile, cb_support
from .inline import send_help
from .restart import restart_userbot
from .start import reset_emoji, reset_prefixes, start_private


async def send_owner(c, m, _):
    txt = await m.reply("Sebentar...", reply_markup=ReplyKeyboardRemove())
    await txt.delete()
    msg = "<b><blockquote>Kamu bisa menghubungi Owner saya dibawah ini"
    bt = ikb([[("Owner", f"{owner_id}", "user_id")]])
    return await m.reply(msg, reply_markup=bt)


async def reset_costumtext(c, m, _):
    txt = await m.reply(
        "**Reseting your costum text!!**", reply_markup=ReplyKeyboardRemove()
    )
    dB.set_var(m.from_user.id, "text_pong", "Pong")
    dB.set_var(m.from_user.id, "text_uptime", "Uptime")
    mmg = f"<a href=tg://user?id={m.from_user.id}>{m.from_user.first_name} {m.from_user.last_name or ''}</a>"
    dB.set_var(m.from_user.id, "text_owner", f"Owner: {mmg}")
    dB.set_var(m.from_user.id, "text_ubot", f"{nama_bot}")
    dB.set_var(m.from_user.id, "text_gcast", "Processing...")
    dB.set_var(m.from_user.id, "text_sukses", "Broadcast results")
    buttons = Button.start(m)
    return await txt.edit(
        "**Succesed reseting your costum text!!**",
        reply_markup=buttons,
        disable_web_page_preview=True,
    )


@zb.regex(
    r"^(🤖 Buat Userbot|⚙️ Status Akun|🛠️ Cek Fitur|🇲🇨 Bahasa|🧸 Owner|🚀 Updates|👥 Cek User|✅ Setuju|❌ Tidak|🏠 Menu Utama|📃 Saya Setuju|🛠️ Cek Fitur|Start|start|✅ Lanjutkan Buat Userbot|🆘 Dukungan|🔄 Reset Emoji|🔄 Reset Text|🔄 Reset Prefix|🔄 Restart Userbot|⬅️ Kembali)",
    human.pv,
)
@org_kontol
async def _(c, m, _):
    try:
        action = m.text
        if action == "🧸 Owner":
            return await send_owner(c, m, _)
        elif action in ["⬅️ Kembali", "Start", "start", "🏠 Menu Utama", "❌ Tidak"]:
            return await start_private(c, m, _)
        elif action == "🆘 Dukungan":
            return await cb_support(c, m, _)
        elif action == "🇲🇨 Bahasa":
            return await atur_bahasa(c, m, _)
        elif action == "✅ Setuju":
            return await cb_trial(c, m, _)
        elif action == "⚙️ Status Akun":
            return await cb_start_profile(c, m, _)
        elif action == "🛠️ Cek Fitur":
            return await send_help(c, m, _)
        elif action in ["🤖 Buat Userbot", "✅ Lanjutkan Buat Userbot"]:
            return await cb_bahan(c, m, _)
        elif action == "📃 Saya Setuju":
            return await cb_bayar_dulu(c, m, _)
        elif action == "👥 Cek User":
            return await cek_ubot(c, m, _)
        elif action == "🚀 Updates":
            return await cb_gitpull(c, m, _)
        elif action == "🔄 Reset Prefix":
            return await reset_prefixes(c, m, _)
        elif action == "🔄 Reset Emoji":
            return await reset_emoji(c, m, _)
        elif action == "🔄 Restart Userbot":
            return await restart_userbot(c, m, _)
        elif action == "🔄 Reset Text":
            return await reset_costumtext(c, m, _)
    except Exception as e:
        return await bot.send_message(
            log_userbot, f"Error {str(e)} di baris: {sys.exc_info()[-1].tb_lineno}"
        )


@zb.callback("^copymsg")
async def _(client, callback_query, _):
    try:
        q = int(callback_query.data.split("_", 1)[1])
        m = [obj for obj in get_objects() if id(obj) == q][0]
        await m._client.unblock_user(bot.me.username)
        await callback_query.edit_message_text("<b>Proses Upload...</b>")
        copy = await m._client.send_message(
            bot.me.username, f"/copy {m.text.split()[1]}"
        )
        msg = m.reply_to_message or m
        await asyncio.sleep(1.5)
        await copy.delete()
        async for get in m._client.search_messages(bot.me.username, limit=1):
            await m._client.copy_message(
                m.chat.id, bot.me.username, get.id, reply_to_message_id=msg.id
            )
            await m._client.delete_messages(m.chat.id, COPY_ID[m._client.me.id])
            await get.delete()
    except Exception as error:
        await callback_query.edit_message_text(f"<code>{error}</code>")


@zb.callback("^cb_gc_info")
async def _(c, cq, _):
    de = cq.from_user.id
    cek = dB.get_var(de, "gc_info")
    usr = cek["username"]
    if usr is None:
        keyb = ikb([[("Desc", f"cb_desc {cek['id']}")]])
    else:
        keyb = ikb(
            [[("Chat", f"https://t.me/{usr}", "url"), ("Desc", f"cb_desc {cek['id']}")]]
        )
    cdesc = cek["desc"]
    if cdesc is None:
        gc_desc = "No description in groups"
    else:
        gc_desc = cdesc
    desc_bh = {"id": cek["id"], "desc_gc": gc_desc, "org": de}
    dB.set_var(c.me.id, "desc_gc", desc_bh)
    # if cek['total_bot'] is None:
    msg = f"""
<b>ChatInfo:</b>
   <b>name:</b> <b>{cek['name']}</b>
      <b>id:</b> <code>{cek['id']}</code>
      <b>type:</b> <b>{cek['type']}</b>
      <b>dc_id:</b> <u>{cek['dc_id']}</u>
      <b>username:</b> <u>@{cek['username']}</u>
      <b>member:</b> <u>{cek['member']}</u>
      <b>protect:</b> <u>{cek['protect']}</u>
"""
    return await cq.edit_message_text(msg, reply_markup=keyb)


@zb.callback("^cb_desc")
async def cb_desc(c, cq, _):
    data = cq.data.split(None, 1)
    idnya = data[1]
    txt = dB.get_var(c.me.id, "desc_gc")
    org = txt["org"]
    cek = dB.get_var(int(org), "gc_info")
    bck = ikb([[(_("prev"), "cb_gc_info")]])
    if not (
        cek["total_bot"],
        cek["total_admin"],
        cek["total_bot_admin"],
        cek["total_banned"],
    ):
        bt = adm = bt_adm = bnd = "You're not admins"
    else:
        bt = cek["total_bot"]
        adm = cek["total_admin"]
        bt_adm = cek["total_bot_admin"]
        bnd = cek["total_banned"]
    msg = f"""
<b>Description:</b>
<blockquote>{txt['desc_gc']}</blockquote>
<b>bot:</b> <u>{bt}</u>
<b>admin:</b> <u>{adm}</u>
<b>bot_admin:</b> <u>{bt_adm}</u>
<b>users_banned:</b> <u>{bnd}</u>
"""
    if int(idnya) == int(txt["id"]):
        return await cq.edit_message_text(
            msg, reply_markup=bck, disable_web_page_preview=True
        )
    else:
        return await cq.answer("Tidak ada perasaan ini", True)


@zb.callback("^next_font")
@INLINE.data
async def next_font(client: bot, callback_query, _):
    try:
        get_id = callback_query.data.split()
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[1]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"click_font {get_id[1]} {query_fonts[1][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("⪻", callback_data=f"prev_font {get_id[1]}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@zb.callback("^prev_font")
@INLINE.data
async def prev_font(client: bot, callback_query, _):
    try:
        get_id = callback_query.data.split()
        buttons = InlineKeyboard(row_width=3)
        keyboard = []
        for X in query_fonts[0]:
            keyboard.append(
                InlineKeyboardButton(
                    X, callback_data=f"click_font {get_id[1]} {query_fonts[0][X]}"
                )
            )
        buttons.add(*keyboard)
        buttons.row(InlineKeyboardButton("⪼", callback_data=f"next_font {get_id[1]}"))
        return await callback_query.edit_message_reply_markup(reply_markup=buttons)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@zb.callback("^click_font")
@INLINE.data
async def click_font(client: bot, callback_query, _):
    try:
        new = callback_query.data.split()
        self = callback_query.from_user.id
        text = dB.get_var(self, "gens_font")
        get_new_font = gens_font(str(new[2]), text)
        dB.remove_var(self, "gens_font")
        return await callback_query.edit_message_text(get_new_font)
    except Exception as error:
        return await callback_query.answer(f"❌ Error: {error}", True)


@zb.callback("^pm_")
async def cb_pm(c, cq, _):

    data, sapa = (
        cq.data.split(None, 2)[1],
        cq.data.split(None, 2)[2],
    )
    gw = dB.get_var(c.me.id, "cb_flood2")
    dia = dB.get_var(c.me.id, "cb_flood")
    plood = dB.get_flood(gw, dia)
    lim = dB.get_var(gw, "PMLIMIT") or LIMIT
    if data == "warn_org":
        return await cq.answer(f"❗ You have {plood}/{lim} warnings !!", True)


@zb.callback(("^cb_pmpermit"))
async def _(c, cq, _):
    # dia = cq.data.split()
    me = cq.from_user.id
    item = [x for x in nlx._ubot if me == x.me.id]
    for gw in item:
        pmtok = dB.get_var(gw.me.id, "PMTEXT")
        pm_text = pmtok if pmtok else DEFAULT_TEXT
        pm_warns = dB.get_var(gw.me.id, "PMLIMIT") or LIMIT
        dia = dB.get_var(c.me.id, "cb_flood")
        Flood = dB.get_flood(gw.me.id, dia)
        teks, button = get_msg_button(pm_text)
        button = create_inline_keyboard(button, gw.me.id)
        def_keyb = ikb(
            [
                [
                    (
                        f"{_('pmper_2').format(Flood, pm_warns)}",
                        f"pm_ warn_org {int(dia)}",
                    )
                ]
            ]
        )
        if button:
            for row in def_keyb.inline_keyboard:
                button.inline_keyboard.append(row)
        else:
            button = def_keyb
        tekss = await escape_tag(c, int(dia), teks, parse_words)
        cekpic = dB.get_var(gw.me.id, "PMPIC")
        costum_cq = cq.edit_message_caption if cekpic else cq.edit_message_text
        costum_text = "caption" if cekpic else "text"
        return await costum_cq(**{costum_text: tekss}, reply_markup=button)


@zb.callback(("^stats_mix"))
async def cb_stats(c, cq, _):

    uptime = await get_time((time() - start_time))
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    btn = ikb([[(_("prev"), f"help_back(0)")]])
    cekpic = dB.get_var(cq.from_user.id, "HELP_PIC")
    costum_cq = cq.edit_message_caption if cekpic else cq.edit_message_text
    costum_text = "caption" if cekpic else "text"
    stats = f"""
**Uptime:** `{uptime}`
**Bot:** `{round(process.memory_info()[0] / 1024 ** 2)} MB`
**Cpus:** `{cpu}%`
**Ram:** `{mem}%`
**Disk:** `{disk}%`
**Modules:** `{len(CMD_HELP)}`
"""
    return await costum_cq(**{costum_text: stats}, reply_markup=btn)


top_text = "<b>Commands Menu!\n  Prefixes: <code>{}</code>\n  User: {}</b>"


@zb.callback("help_(.*?)")
async def _(c, cq, _):
    home_match = re.match(r"help_home\((.+?)\)", cq.data)
    mod_match = re.match(r"help_module\((.+?),(.+?)\)", cq.data)
    prev_match = re.match(r"help_prev\((.+?)\)", cq.data)
    next_match = re.match(r"help_next\((.+?)\)", cq.data)
    back_match = re.match(r"help_back\((\d+)\)", cq.data)
    create_match = re.match(r"help_create", cq.data)
    user_id = cq.from_user.id
    prefix = nlx.get_prefix(user_id)
    full = f"<a href=tg://user?id={cq.from_user.id}>{cq.from_user.first_name} {cq.from_user.last_name or ''}</a>"
    cekpic = dB.get_var(user_id, "HELP_PIC")
    costum_cq = cq.edit_message_caption if cekpic else cq.edit_message_text
    costum_text = "caption" if cekpic else "text"
    if mod_match:
        module = mod_match.group(1)
        prev_page_num = int(mod_match.group(2))
        bot_text = f"{CMD_HELP[module].help_string(user_id)}\n".format(
            next((p) for p in prefix)
        )
        try:
            button = ikb([[("↩️", f"help_back({prev_page_num})")]])
            return await costum_cq(
                **{
                    costum_text: bot_text
                    + f"<b>🤖 {nama_bot} </b>"
                },
                reply_markup=button,
            )
        except FloodWait as e:
            return await cq.answer(f"FloodWait {e}, Please Waiting!!", True)

        except MessageNotModified:
            return
    elif prev_match:
        curr_page = int(prev_match.group(1))
        try:
            return await costum_cq(
                **{costum_text: top_text.format(" ".join(prefix), full)},
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page, CMD_HELP, "help")
                ),
            )
        except FloodWait as e:
            return await cq.answer(f"FloodWait {e}, Please Waiting!!", True)

        except MessageNotModified:
            return
    elif next_match:
        next_page = int(next_match.group(1))
        try:
            return await costum_cq(
                **{costum_text: top_text.format(" ".join(prefix), full)},
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page, CMD_HELP, "help")
                ),
            )
        except FloodWait as e:
            return await cq.answer(f"FloodWait {e}, Please Waiting!!", True)

        except MessageNotModified:
            return
    elif back_match:
        prev_page_num = int(back_match.group(1))
        try:
            return await costum_cq(
                **{costum_text: top_text.format(" ".join(prefix), full)},
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(prev_page_num, CMD_HELP, "help")
                ),
            )
        except FloodWait as e:
            return await cq.answer(f"FloodWait {e}, Please Waiting!!", True)

        except MessageNotModified:
            return
    elif create_match:
        try:
            return await costum_cq(
                **{costum_text: top_text.format(" ".join(prefix), full)},
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CMD_HELP, "help")
                ),
            )
        except FloodWait as e:
            return await cq.answer(f"FloodWait {e}, Please Waiting!!", True)

        except MessageNotModified:
            return


@zb.callback("^#")
async def cb_notes(c: bot, cq, _):
    ii = cq.data.split("_")
    dia = cq.from_user
    try:
        notetag = ii[-2].replace("#", "")
        gw = ii[-1]
        item = [x for x in nlx._ubot if int(gw) == x.me.id]
        gclog = nlx.get_logger(int(gw))
        logs = gclog if gclog else "me"
        noteval = dB.get_var(int(gw), notetag, "notes")
        cekpic = dB.get_var(int(gw), "PMPIC")
        costum_cq = cq.edit_message_caption if cekpic else cq.edit_message_text
        costum_text = "caption" if cekpic else "text"
        full = (
            f"<a href=tg://user?id={dia.id}>{dia.first_name} {dia.last_name or ''}</a>"
        )
        dB.add_userdata(
            dia.id,
            dia.first_name,
            dia.last_name,
            dia.username,
            dia.mention,
            full,
            dia.id,
        )
        if not noteval:
            await cq.answer("Catatan tidak ditemukan.", True)
            return
        for me in item:
            msg = await me.get_messages(logs, int(noteval["message_id"]))
            tks = msg.caption if msg.caption else msg.text
            tg, nontg = cek_tg(tks)
            if noteval["type"] in ["photo", "video"]:
                note, button = get_msg_button(nontg)
                teks = await escape_tag(bot, dia.id, note, parse_words)

                button = create_inline_keyboard(button, int(gw))
                try:
                    return await costum_cq(**{costum_text: note}, reply_markup=button)
                except FloodWait as e:
                    return await cq.answer(f"FloodWait {e}, Please Waiting!!", True)
            else:
                note, button = get_msg_button(nontg)
                teks = await escape_tag(bot, dia.id, note, parse_words)
                button = create_inline_keyboard(button, int(gw))
                try:
                    return await costum_cq(**{costum_text: teks}, reply_markup=button)
                except FloodWait as e:
                    return await cq.answer(f"FloodWait {e}, Please Waiting!!", True)
                except MessageNotModified:
                    return

    except Exception as e:
        return await bot.send_message(
            log_userbot,
            f"CQ Notes Error user_id {str(e)} di baris: {sys.exc_info()[-1].tb_lineno}",
        )
