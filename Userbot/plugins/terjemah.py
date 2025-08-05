################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import os

import gtts
from gpytranslate import Translator

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, kode_bahasa, zb

__MODULES__ = "Translate"

USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_terjemah")


@zb.ubot("tts")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)

    pros = await m.reply(_("proses").format(em.proses, proses_))
    if m.reply_to_message:
        bhs = c._translate[c.me.id]["negara"]
        kata = m.reply_to_message.text or m.reply_to_message.caption
    else:
        if len(m.command) < 2:
            return await pros.edit(_("tr_1").format(em.gagal, m.command))
        else:
            bhs = c._translate[c.me.id]["negara"]
            kata = m.text.split(None, 1)[1]
    gts = gtts.gTTS(kata, lang=bhs)
    gts.save("trs.oog")
    rep = m.reply_to_message or m
    try:
        await c.send_voice(
            chat_id=m.chat.id,
            voice="trs.oog",
            reply_to_message_id=rep.id,
        )
        await pros.delete()
        os.remove("trs.oog")
        return
    except Exception as er:
        return await pros.edit(_("err").format(em.gagal, er))

    except FileNotFoundError:
        return


@zb.ubot("tr")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    trans = Translator()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    if m.reply_to_message:
        bhs = c._translate[c.me.id]["negara"]
        txt = m.reply_to_message.text or m.reply_to_message.caption
        src = await trans.detect(txt)
    else:
        if len(m.command) < 2:
            return await m.reply(_("tr_1").format(em.gagal, m.command))

        else:
            bhs = c._translate[c.me.id]["negara"]
            txt = m.text.split(None, 1)[1]
            src = await trans.detect(txt)
    trsl = await trans(txt, sourcelang=src, targetlang=bhs)
    reply = _("tr_2").format(em.sukses, trsl.text)
    rep = m.reply_to_message or m
    await pros.delete()
    return await c.send_message(m.chat.id, reply, reply_to_message_id=rep.id)


@zb.ubot("lang")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    try:
        bhs_list = "\n".join(
            f"- **{lang}**: `{code}`" for lang, code in kode_bahasa.items()
        )
        return await m.reply(_("tr_3").format(em.sukses, bhs_list))

    except Exception as e:
        return await m.reply(_("err").format(em.gagal, e))


@zb.ubot("setlang")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.command) < 2:
        return await pros.edit(_("tr_4").format(em.gagal, m.text))

    for lang, code in kode_bahasa.items():
        kd = m.text.split(None, 1)[1]
        if kd.lower() == code.lower():
            c._translate[c.me.id] = {"negara": kd}
            return await pros.edit(_("tr_5").format(em.sukses, kd, lang))

    return await pros.edit(_("tr_6").format(em.gagal))
