"""
CREATE BY: NORSODIKIN.T.ME
UPDATE BY: KENAPANAN.T.ME
"""

from pyrogram.enums import ParseMode

from config import bot_username
from Userbot import logger, nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (Emojik, ReplyCheck, get_msg_button, h_s,
                                  initial_ctext, zb)

__MODULES__ = "Notes"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_notes")


def kontol_siapa(xi, tipe):
    return f"Userbot/{xi}.{tipe}"


@zb.ubot("save")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    rep = m.reply_to_message
    if len(m.command) < 2 or not rep:
        return await xx.edit(_("nts_1").format(em.gagal, m.text.split()[0]))
    nama = m.text.split()[1]

    logs = "me"
    getnotes = dB.get_var(c.me.id, nama, "notes")
    if getnotes:
        return await xx.edit(_("nts_12").format(em.gagal, nama))
    value = None
    # txt = rep.text if rep.text else rep.caption
    type_mapping = {
        "text": rep.text,
        "photo": rep.photo,
        "voice": rep.voice,
        "audio": rep.audio,
        "video": rep.video,
        "video_note": rep.video_note,
        "animation": rep.animation,
        "sticker": rep.sticker,
        "document": rep.document,
        "contact": rep.contact,
    }
    for media_type, media in type_mapping.items():
        if media:
            send = await rep.copy(logs)
            value = {
                "type": media_type,
                "message_id": send.id,
            }
            break
    if value:
        dB.set_var(c.me.id, nama, value, "notes")
        return await xx.edit(_("nts_3").format(em.sukses, nama))
    else:
        return await xx.edit(_("nts_1").format(em.gagal, m.text.split()[0]))


@zb.ubot("get")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()

    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))

    logs = "me"

    try:
        if len(m.text.split()) == 2:
            note = m.text.split()[1]
            data = dB.get_var(c.me.id, note, "notes")
            if not data:
                return await xx.edit(_("nts_10").format(em.gagal, note))
            msg_id = await c.get_messages(logs, int(data["message_id"]))
            return await getnotes_(c, m, _, xx, note, data, msg_id)
        elif len(m.text.split()) == 3 and (m.text.split())[2] in ["noformat", "raw"]:
            note = m.text.split()[1]
            data = dB.get_var(c.me.id, note, "notes")
            if not data:
                return await xx.edit(_("nts_10").format(em.gagal, note))
            msg_id = await c.get_messages(logs, int(data["message_id"]))
            return await get_raw_note(c, m, _, xx, note, data, msg_id)
        else:
            return await xx.edit(_("nts_4").format(em.gagal))
    except Exception as e:
        return await xx.edit(_("err").format(em.gagal, str(e)))


async def getnotes_(c, m, _, xx, note, data, msg_id):
    em = Emojik(c)
    em.initialize()
    thetext = msg_id.text if msg_id.text else msg_id.caption or ""
    teks, button = get_msg_button(thetext)
    if button:
        try:
            a = await c.get_inline_bot_results(bot_username, f"get_note_ {note}")
            logger.info(f"{note}")
            # await m.delete()
            await xx.delete()
            return await c.send_inline_bot_result(
                m.chat.id,
                a.query_id,
                a.results[0].id,
                reply_to_message_id=ReplyCheck(m),
            )
        except Exception as e:
            return await m.reply(_("err").format(em.gagal, e))
    else:
        await xx.delete()
        return await msg_id.copy(m.chat.id, reply_to_message_id=ReplyCheck(m))


async def get_raw_note(c, m, _, xx, note, data, msg_id):
    em = Emojik(c)
    em.initialize()
    await msg_id.copy(
        m.chat.id, reply_to_message_id=ReplyCheck(m), parse_mode=ParseMode.DISABLED
    )
    return await xx.delete()


@zb.ubot("notes")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    getnotes = dB.all_var(c.me.id, "notes")
    if not getnotes:
        await xx.edit(_("nts_6").format(em.gagal))
        return
    rply = _("nts_7").format(em.sukses)
    for x, data in getnotes.items():
        rply += _("nts_8").format(x)
    return await xx.edit(rply)


@zb.ubot("clear")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    args = c.get_arg(m).split(",")

    logs = "me"
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))

    if len(args) == 0 or (len(args) == 1 and args[0].strip() == ""):
        return await xx.edit(_("nts_9").format(em.gagal))

    gagal_list = []
    sukses_list = []

    for arg in args:
        arg = arg.strip()
        if not arg:
            continue
        data = dB.get_var(c.me.id, arg, "notes")
        if not data:
            gagal_list.append(arg)
        else:
            dB.remove_var(c.me.id, arg, "notes")
            await c.delete_messages(logs, int(data["message_id"]))
            sukses_list.append(arg)

    if sukses_list:
        return await xx.edit(_("nts_11").format(em.sukses, ", ".join(sukses_list)))

    if gagal_list:
        return await xx.edit(_("nts_10").format(em.gagal, ", ".join(gagal_list)))
