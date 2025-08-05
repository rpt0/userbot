import random
from datetime import datetime
from gc import get_objects
from time import time

from pyrogram.helpers import InlineKeyboard, ikb
from pyrogram.raw.functions import Ping
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InlineQueryResultPhoto,
                            InlineQueryResultVideo, InputTextMessageContent)

from config import CMD_HELP, DEVS, bot_id, bot_username, log_pic, nama_bot
from Userbot import bot, logger, nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (cek_tg, create_inline_keyboard, escape_tag,
                                  get_msg_button, get_time, zb,
                                  paginate_modules, parse_words, query_fonts,
                                  start_time)
from Userbot.plugins.graph import upload_media
from Userbot.plugins.pmpermit import DEFAULT_TEXT, LIMIT

from .call_calc import calc_help
from .call_mark import markdown_help

__MODULES__ = "Inline"
__HELPERS__ = "See inline for help related to inline."

keywords_list = [
    "help",
    "alive",
    "calculator",
]


async def all_inline(__HELPERS__, q, _):
    answerss = [
        InlineQueryResultArticle(
            title=nama_bot,
            description="Get Of Bot.",
            input_message_content=InputTextMessageContent(
                "Click A Button To Get Started."
            ),
            thumb_url=log_pic,
            reply_markup=ikb([[("Click Here", f"https://t.me/KingzUserbotPro_bot", "url")]]),
        )
    ]
    answerss = await inline_help(answerss, q, _)
    return answerss


@zb.inline()
async def _(c, q, _):
    try:
        text = q.query.strip().lower()
        answers = []
        if text.strip() == "":
            answerss = await all_inline(__HELPERS__, q, _)
            return await c.answer_inline_query(q.id, results=answerss, cache_time=5)
        elif text.split()[0] == "help":
            answerss = await inline_help(answers, q, _)
            return await c.answer_inline_query(q.id, results=answerss, cache_time=0)
        elif text.split()[0] == "get_teks_but":
            answerss = await teks_button(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "get_msg_copy":
            answerss = await copy_inline_msg(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "get_font":
            answerss = await font_inline(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "alive":
            answerss = await alive_inline(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )

        elif text.split()[0] == "ambil_tombolpc":
            answerss = await inline_pmpermit(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "get_note_":
            answerss = await inline_notes(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "buat_button2":
            answerss = await button_inline(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "mark_in":
            answerss = await inline_mark(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "user_info":
            answerss = await user_inline(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "gc_info":
            answerss = await gc_inline(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "calculator":
            answerss = await inline_calc(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "secret":
            answerss = await secret_inline(answers, q, _)
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "_send_":
            tuju = text.split()[1]
            answerss = await send_inline(answers, q, _, int(tuju))
            return await c.answer_inline_query(
                q.id,
                results=answerss,
                cache_time=0,
            )

    except Exception as e:
        return f"{e}"


async def inline_calc(j, iq, _):
    txt = f"<b>{nama_bot} Calculator</b>"
    berak = calc_help()
    j.append(
        InlineQueryResultArticle(
            title="Calculator!",
            description="Get Calculator.",
            thumb_url=log_pic,
            reply_markup=berak,
            input_message_content=InputTextMessageContent(txt),
        )
    )
    return j


async def copy_inline_msg(j, inline_query, _):
    j.append(
        InlineQueryResultArticle(
            title="get message!",
            reply_markup=ikb(
                [
                    [
                        (
                            "🔐 Buka Konten 🔐",
                            f"copymsg_{int(inline_query.query.split()[1])}",
                        )
                    ]
                ]
            ),
            input_message_content=InputTextMessageContent("<b>🔒 Klik Tombol Ini</b>"),
        )
    )
    return j


async def inline_help(j, iq, _):
    user_id = iq.from_user.id
    prefix = nlx.get_prefix(user_id)
    full = f"<b><blockquote><a href=tg://user?id={iq.from_user.id}>{iq.from_user.first_name} {iq.from_user.last_name or ''}</a>"
    msg = "**Commands Menu!\n  Prefixes: `{}`\n  User: {}**</blockquote></b>".format(
        " ".join(prefix), full
    )
    cekpic = dB.get_var(user_id, "HELP_PIC")
    if not cekpic:
        j.append(
            InlineQueryResultArticle(
                title="Help Menu!",
                description="Help Command",
                thumb_url=log_pic,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CMD_HELP, "help")
                ),
                input_message_content=InputTextMessageContent(msg),
            )
        )
    else:
        filem = (
            InlineQueryResultVideo
            if cekpic.endswith(".mp4")
            else InlineQueryResultPhoto
        )
        url_ling = (
            {"video_url": cekpic, "thumb_url": cekpic}
            if cekpic.endswith(".mp4")
            else {"photo_url": cekpic}
        )
        j.append(
            filem(
                **url_ling,
                title=nama_bot,
                description="Get Help.",
                thumb_url=log_pic,
                caption=msg,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CMD_HELP, "help")
                ),
            )
        )
    return j


async def secret_inline(j, q, _):
    m = [obj for obj in get_objects() if id(obj) == int(q.query.split()[1])][0]
    j.append(
        InlineQueryResultArticle(
            title="pesan rahasia!",
            reply_markup=ikb(
                [
                    [
                        (
                            "📨 Private Message",
                            f"https://t.me/{bot.me.username}?start=secretMsg_{int(q.query.split(None, 1)[1])}",
                            "url",
                        )
                    ]
                ]
            ),
            input_message_content=InputTextMessageContent(
                f"<b>Pesan Untuk Anda :</b> <a href=tg://user?id={m.reply_to_message.from_user.id}>{m.reply_to_message.from_user.first_name} {m.reply_to_message.from_user.last_name or ''}</a>"
            ),
        )
    )
    return j


async def gc_inline(j, iq, _):
    de = iq.from_user.id
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
    dB.set_var(bot_id, "desc_gc", desc_bh)
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
    j.append(
        InlineQueryResultArticle(
            title="gc info!",
            input_message_content=InputTextMessageContent(
                msg, disable_web_page_preview=True
            ),
            reply_markup=keyb,
        )
    )
    return j


def cek_gban(org):
    gw = next((x for x in nlx._ubot), None)
    gban_db = dB.get_list_from_var(gw.me.id, "GBANNED")
    if org in gban_db:
        return True
    return False


async def user_inline(j, iq, _):
    de = iq.from_user.id
    cek = dB.get_var(de, "user_info")
    gb = cek_gban(cek["id"])
    try:
        org = await bot.get_users(int(cek["id"]))
        keyb = ikb([[("UserLink", f"{org.id}", "user_id")]])
    except:
        org = f"tg://openmessage?user_id={int(cek['id'])}"
        keyb = ikb([[("UserLink", f"{org}", "url")]])
    msg = f"""
<b>UserInfo:</b>
   <b>name:</b> <b>{cek['name']}</b>
      <b>id:</b> <code>{cek['id']}</code>
      <b>is_contact:</b> <u>{cek['contact']}</u>
      <b>is_premium:</b> <u>{cek['premium']}</u>
      <b>is_deleted:</b> <u>{cek['deleted']}</u>
      <b>is_bot:</b> <u>{cek['isbot']}</u>
      <b>is_gbanned:</b> <u>{gb}</u>
      <b>dc_id:</b> <u>{cek['dc_id']}</u>
      <b>created_acc:</b> <code>{cek['create']}</code>"""
    dB.remove_var(de, "user_info")
    j.append(
        InlineQueryResultArticle(
            title="user info!",
            input_message_content=InputTextMessageContent(
                msg, disable_web_page_preview=True
            ),
            reply_markup=keyb,
        )
    )
    return j


async def teks_button(jawab, iq, _):
    gw = iq.from_user.id
    getpm_txt = dB.get_var(gw, "PMTEXT")
    pm_text = getpm_txt if getpm_txt else DEFAULT_TEXT
    teks, button = get_msg_button(pm_text)
    if button:
        button = create_inline_keyboard(button)
    jawab.append(
        InlineQueryResultArticle(
            title="Tombol Teks!",
            input_message_content=InputTextMessageContent(
                teks,
                disable_web_page_preview=True,
            ),
            reply_markup=button,
        )
    )
    return jawab


async def font_inline(jawab, inline_query, _):
    get_id = inline_query.query.split()
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
    jawab.append(
        InlineQueryResultArticle(
            title="get font!",
            reply_markup=buttons,
            input_message_content=InputTextMessageContent(
                "👇 Silahkan pilih salah satu font di bawah"
            ),
        )
    )
    return jawab


async def button_inline(jawab, iq, _):
    dia = iq.from_user.id
    rep = dB.get_var(dia, "id_button")
    text, keyboard = get_msg_button(rep)
    if keyboard:
        keyboard = create_inline_keyboard(keyboard)
    pic = dB.get_var(dia, "id_button_pic")
    if pic:
        filem = (
            InlineQueryResultVideo if pic.endswith(".mp4") else InlineQueryResultPhoto
        )
        url_ling = (
            {"video_url": pic, "thumb_url": pic}
            if pic.endswith(".mp4")
            else {"photo_url": pic}
        )
        jawab.append(
            filem(
                **url_ling, title="PIC Buttons !", caption=text, reply_markup=keyboard
            )
        )
    else:
        jawab.append(
            InlineQueryResultArticle(
                title="Tombol Teks!",
                input_message_content=InputTextMessageContent(
                    text, disable_web_page_preview=True
                ),
                reply_markup=keyboard,
            )
        )
    dB.remove_var(dia, "id_button_pic")
    dB.remove_var(dia, "id_button")
    return jawab


async def inline_mark(jawab, iq, _):
    txt = "Untuk melihat format markdown silahkan klik tombol dibawah."
    jawab.append(
        InlineQueryResultArticle(
            title="Marketing!",
            reply_markup=markdown_help(),
            input_message_content=InputTextMessageContent(txt),
        )
    )
    return jawab


# @zb.inline("^help")
async def send_help(client, m, _):
    user_id = m.from_user.id
    prefix = nlx.get_prefix(user_id)
    full = f"<a href=tg://user?id={m.from_user.id}>{m.from_user.first_name} {m.from_user.last_name or ''}</a>"
    msg = "<b>✰ Commands Menu Kingz!\n ♕ Prefixes: `{}`\n ✭ User: {}</b>".format(
        " ".join(prefix), full
    )
    return await m.reply(
        msg, reply_markup=InlineKeyboardMarkup(paginate_modules(0, CMD_HELP, "help"))
    )


# send
async def send_inline(jawab, iq, _, user_id):
    try:
        _id = dB.get_var(user_id, "inline_send")
        m = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
        if m:
            if m.reply_to_message.media:
                photo_tg = await upload_media(m)
                cp = m.reply_to_message.caption
                text = cp if cp else ""
                jawab.append(
                    InlineQueryResultPhoto(
                        photo_url=photo_tg,
                        title="kon",
                        reply_markup=m.reply_to_message.reply_markup,
                        caption=text,
                    )
                )
            else:
                jawab.append(
                    InlineQueryResultArticle(
                        title="kon",
                        reply_markup=m.reply_to_message.reply_markup,
                        input_message_content=InputTextMessageContent(
                            m.reply_to_message.text
                        ),
                    )
                )
            return jawab
    except Exception as e:
        logger.error(f"Error: {e}")


async def alive_inline(jawab, iq, _):
    self = iq.from_user.id
    pmper = None
    stutas = None
    start = datetime.now()
    pink = (datetime.now() - start).microseconds / 1000
    upnya = await get_time((time() - start_time))
    gw = next((x for x in nlx._ubot), None)
    try:
        peer = nlx._my_peer[self]
        users = len(peer["private"])
        group = len(peer["group"])
    except Exception:
        users = random.randrange(await gw.get_dialogs_count())
        group = random.randrange(await gw.get_dialogs_count())
    await gw.invoke(Ping(ping_id=0))
    if self in DEVS:
        stutas = _("alv_1")
    else:
        stutas = _("alv_2")
    cekpr = dB.get_var(self, "PMPERMIT")
    if cekpr:
        pmper = "enable"
    else:
        pmper = "disable"
    get_exp = dB.get_expired_date(self)
    exp = get_exp.strftime("%d-%m-%Y")
    txt = f"""
<b>{nama_bot}</b>
    <b>status:</b> {stutas} 
      <b>dc_id:</b> <code>{gw.me.dc_id}</code>
      <b>ping_dc:</b> <code>{str(pink).replace('.', ',')} ms</code>
      <b>anti_pm:</b> <code>{pmper}</code>
      <b>peer_users:</b> <code>{users} users</code>
      <b>peer_group:</b> <code>{group} group</code>
      <b>peer_ubot:</b> <code>{len(nlx._ubot)}</code>
      <b>zb_uptime:</b> <code>{upnya}</code>
      <b>expires_on:</b> <code>{exp}</code>
"""
    msge = f"<blockquote>{txt}</blockquote>"
    bo_ol = ikb([[("stats", "stats_mix")]])
    cekpic = dB.get_var(self, "ALIVE_PIC")
    if not cekpic:
        jawab.append(
            InlineQueryResultArticle(
                title=nama_bot,
                description="Get Alive Of Bot.",
                input_message_content=InputTextMessageContent(msge),
                thumb_url=log_pic,
                reply_markup=bo_ol,
            )
        )
    else:
        filem = (
            InlineQueryResultVideo
            if cekpic.endswith(".mp4")
            else InlineQueryResultPhoto
        )
        url_ling = (
            {"video_url": cekpic, "thumb_url": cekpic}
            if cekpic.endswith(".mp4")
            else {"photo_url": cekpic}
        )
        jawab.append(
            filem(
                **url_ling,
                title=nama_bot,
                description="Get Alive Of Bot.",
                thumb_url=log_pic,
                caption=msge,
                reply_markup=bo_ol,
            )
        )
    return jawab


async def inline_pmpermit(jawab, iq, _):
    dia = iq.query.split()
    gw = iq.from_user.id
    pmtok = dB.get_var(gw, "PMTEXT")
    pm_text = pmtok if pmtok else DEFAULT_TEXT
    pm_warns = dB.get_var(gw, "PMLIMIT") or LIMIT
    Flood = dB.get_flood(gw, int(dia[1]))
    dB.set_var(bot_id, "cb_flood", int(dia[1]))
    dB.set_var(bot_id, "cb_flood2", gw)
    teks, button = get_msg_button(pm_text)
    # button = create_inline_keyboard(button)
    button = create_inline_keyboard(button, gw)
    def_keyb = ikb(
        [
            [
                (
                    f"{_('pmper_2').format(Flood, pm_warns)}",
                    f"pm_ warn_org {int(dia[1])}",
                )
            ]
        ]
    )
    if button:
        for row in def_keyb.inline_keyboard:
            button.inline_keyboard.append(row)
    else:
        button = def_keyb
    tekss = await escape_tag(bot, int(dia[1]), teks, parse_words)
    lah = dB.get_var(gw, "PMPIC")
    if lah:
        filem = (
            InlineQueryResultVideo if lah.endswith(".mp4") else InlineQueryResultPhoto
        )
        url_ling = (
            {"video_url": lah, "thumb_url": lah}
            if lah.endswith(".mp4")
            else {"photo_url": lah}
        )
        jawab.append(
            filem(
                **url_ling,
                title="PIC Buttons !",
                caption=tekss,
                reply_markup=button,
            )
        )
    else:
        jawab.append(
            InlineQueryResultArticle(
                title="Tombol PM!",
                input_message_content=InputTextMessageContent(
                    tekss,
                    disable_web_page_preview=True,
                ),
                reply_markup=button,
            )
        )
    return jawab


async def inline_notes(jawab, iq, _):
    q = iq.query.split(None, 1)
    note = q[1]
    logger.info(f"{note}")
    gw = iq.from_user.id
    noteval = dB.get_var(gw, note, "notes")
    if not noteval:
        return
    item = [x for x in nlx._ubot if gw == x.me.id]
    gclog = nlx.get_logger(gw)
    logs = gclog if gclog else "me"
    for me in item:
        msg = await me.get_messages(logs, int(noteval["message_id"]))
        tks = msg.caption if msg.caption else msg.text
        tg, nontg = cek_tg(tks)
        if tg:
            note, button = get_msg_button(nontg)
            button = create_inline_keyboard(button, gw)
            filem = (
                InlineQueryResultVideo
                if tg.endswith(".mp4")
                else InlineQueryResultPhoto
            )
            url_ling = (
                {"video_url": tg, "thumb_url": tg}
                if tg.endswith(".mp4")
                else {"photo_url": tg}
            )
            jawab.append(
                filem(
                    **url_ling,
                    title="notes buttons media !!",
                    caption=note,
                    reply_markup=button,
                )
            )
        else:
            note, button = get_msg_button(tks)

            button = create_inline_keyboard(button, gw)

            jawab.append(
                InlineQueryResultArticle(
                    title="Tombol Notes!",
                    input_message_content=InputTextMessageContent(
                        note, disable_web_page_preview=True
                    ),
                    reply_markup=button,
                )
            )
    return jawab
