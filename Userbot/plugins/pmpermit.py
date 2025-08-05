################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################
import asyncio

from pyrogram.enums import ChatType, ParseMode

from config import DEVS, bot_username, nama_bot
from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (Emojik, capture_err, escape_tag, h_s,
                                  initial_ctext, zb, parse_words)

from .graph import upload_media

__MODULES__ = "PMPermit"


def help_string(org):
    return h_s(org, "help_pmpermit")


flood = {}
flood2 = {}

DEFAULT_TEXT = "Hey {mention} 👋.  Don't spam or you'll be blocked!!"
PM_WARN = "You've got {}/{} warnings !!"
LIMIT = 5
INLINE_WARN = """<blockquote><b>{}

You've got {}/{} warnings !!</b></blockquote>"""


@zb.ubot("pmpermit|antipm")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    jing = await m.reply(_("proses").format(em.proses, proses_))
    try:
        command, variable = m.command[:2]
    except ValueError:
        return await jing.delete()
    value = " ".join(m.command[2:])
    rep = m.reply_to_message
    if variable.lower() == "set":
        akt = ["on", "true"]
        mti = ["off", "false"]
        if value.lower() in akt:
            stat = dB.get_var(c.me.id, "PMPERMIT")
            if stat:
                return await jing.edit(
                    "{}PMPermit anda saat ini sudah aktif.".format(em.sukses)
                )
            else:
                dB.set_var(c.me.id, "PMPERMIT", value)
                await jing.edit(
                    "{}PMPermit anda berhasil diaktifkan.".format(em.sukses)
                )
                return
        elif value.lower() in mti:
            stat = dB.get_var(c.me.id, "PMPERMIT")
            if stat:
                dB.remove_var(c.me.id, "PMPERMIT")
                return await jing.edit(
                    "{}PMPermit anda saat ini berhasil dinonaktifkan.".format(em.gagal)
                )
            else:
                return await jing.edit(
                    "{}PMPermit anda saat ini memang tidak aktif.".format(em.gagal)
                )
        else:
            return await jing.edit(
                "{}Silahkan berikan value `on` atau `off`.".format(em.gagal)
            )
    elif variable.lower() == "pic":
        if value.lower() == "reset":
            dB.remove_var(c.me.id, "PMPIC")
            return await jing.edit(
                "{}PMPermit gambar kamu berhasil disetel default.".format(em.sukses)
            )
        if m.reply_to_message:
            pice = await upload_media(m)
        else:
            pice = value
            if not pice.startswith("https:"):
                return await jing.edit(
                    "{}Silahkan berikan link atau balas pesan berupa media".format(
                        em.gagal
                    )
                )
        dB.set_var(c.me.id, "PMPIC", pice)
        return await jing.edit(
            "{}PMPermit gambar disetel ke : {}".format(em.sukses, pice),
            disable_web_page_preview=True,
        )
    elif variable.lower() == "teks":
        if value.lower() == "reset":
            dB.remove_var(c.me.id, "PMTEXT")
            return await jing.edit(
                "{}PMPermit teks kamu berhasil disetel default.".format(em.sukses)
            )
        if m.reply_to_message:
            pice = c.new_arg(m)
        else:
            pice = value
        dB.set_var(c.me.id, "PMTEXT", pice)
        return await jing.edit(_("pmper_7").format(em.sukses, pice))
    elif variable.lower() == "limit":
        if value.lower() == "reset":
            dB.remove_var(c.me.id, "PMLIMIT")
            return await jing.edit(
                "{}PMPermit limit kamu berhasil disetel default.".format(em.sukses)
            )
        if not m.reply_to_message:
            pice = value
        else:
            pice = rep.text
        if not pice.isnumeric():
            return await jing.edit("{}Silahkan berikam angka untuk PMPermit limit.")
        dB.set_var(c.me.id, "PMLIMIT", pice)
        return await jing.edit(_("pmper_7").format(em.sukses, pice))
    elif variable.lower() == "get":
        if value.lower() == "teks":
            txt = dB.get_var(c.me.id, "PMTEXT")
            pmtext = txt if txt else DEFAULT_TEXT
            await m.reply(
                f"PMPermit teks anda:\n\n{pmtext}",
                disable_web_page_preview=True,
                parse_mode=ParseMode.DISABLED,
            )
            return await jing.delete()
        elif value.lower() == "limit":
            lmt = dB.get_var(c.me.id, "PMLIMIT")
            lmt if lmt else LIMIT
            return await jing.edit(
                "{}PMPermit limit anda:\n\n{}".format(em.sukses, lmt)
            )
        elif value.lower() == "pic":
            pick = dB.get_var(c.me.id, "PMPIC")
            if pick:
                return await jing.edit(
                    "{}PMPermit gambar anda:\n\n{}".format(em.sukses, pick)
                )
            else:
                return await jing.edit("{}Anda belum mengatur PMPermit gambar!!")
        elif value.lower() == "status":
            sts = dB.get_var(c.me.id, "PMPERMIT")
            if sts:
                return await jing.edit(
                    "{}PMPermit status anda:\n\n{}".format(em.sukses, sts)
                )
            else:
                return await jing.edit(
                    "{}Anda belum mengatur PMPermit!!".format(em.gagal)
                )
        else:
            return await jing.edit(_("dbs_6").format(em.gagal))
    else:
        await jing.edit(_("dbs_6").format(em.gagal))
        return


@zb.ubot("ok|setuju")
async def _(c: nlx, m, _):
    pm_ok = dB.get_list_from_var(c.me.id, "PM_OKE")
    em = Emojik(c)
    em.initialize()
    chat_type = m.chat.type
    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if m.reply_to_message:
            dia = m.reply_to_message.from_user.id
        else:
            return await m.delete()
    elif chat_type == ChatType.PRIVATE:
        dia = m.chat.id
    else:
        return await m.delete()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    babi = await m.reply(_("proses").format(em.proses, proses_))
    getc_pm_warns = dB.get_var(c.me.id, "PMLIMIT")
    custom_pm_warns = getc_pm_warns if getc_pm_warns else LIMIT
    if dia in pm_ok:
        await babi.edit(_("pmper_3").format(em.sukses))
        return
    try:
        async for uh in c.get_chat_history(dia, limit=int(custom_pm_warns)):
            if uh.reply_markup:
                await uh.delete()
            else:
                try:
                    await c.delete_messages("me", message_ids=flood[dia])
                except KeyError:
                    pass
    except:
        pass

    dB.add_to_var(c.me.id, "PM_OKE", dia)
    await babi.edit(_("pmper_4").format(em.sukses))
    return


@zb.ubot("no|tolak")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pm_ok = dB.get_list_from_var(c.me.id, "PM_OKE")
    babi = await m.reply(_("proses").format(em.proses, proses_))
    await asyncio.sleep(2)
    chat_type = m.chat.type
    if chat_type in [ChatType.GROUP, ChatType.SUPERGROUP]:
        if m.reply_to_message:
            user_id = m.reply_to_message.from_user.id
        else:
            return await m.delete()
    elif chat_type == ChatType.PRIVATE:
        user_id = m.chat.id
    else:
        return await m.delete()

    if user_id not in pm_ok:
        await babi.edit(_("pmper_5").format(em.sukses))
        return
    dB.remove_from_var(c.me.id, "PM_OKE", user_id)
    await babi.edit(_("pmper_6").format(em.sukses))
    return


@zb.nocmd("PMPERMIT", nlx)
@capture_err
# @manage_handlers
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    gw = c.me.id
    dia = m.from_user

    pm_oke = dB.get_list_from_var(c.me.id, "PM_OKE")
    ong = dB.get_var(gw, "PMPERMIT")
    if not ong or dia.id in pm_oke:
        return
    if dia.is_fake or dia.is_scam:
        return await c.block_user(dia.id)
    if dia.is_support or dia.is_verified or dia.is_self:
        return
    if dia.id in DEVS:
        try:
            await c.send_message(
                dia.id,
                f"<b>Menerima Pesan Dari {dia.mention} !!\nTerdeteksi Developer Dari {nama_bot}.</b>",
                parse_mode=ParseMode.HTML,
            )
            dB.add_to_var(c.me.id, "PM_OKE", dia.id)
        except BaseException:
            pass
        return
    pmtok = dB.get_var(gw, "PMTEXT")
    pm_text = pmtok if pmtok else DEFAULT_TEXT
    pm_warns = dB.get_var(gw, "PMLIMIT") or LIMIT
    async for aks in c.get_chat_history(dia.id, limit=int(pm_warns)):
        if aks.reply_markup:
            await aks.delete()
    if str(dia.id) in flood:
        flood[str(dia.id)] += 1
    else:
        flood[str(dia.id)] = 1
    if flood[str(dia.id)] > int(pm_warns):
        del flood[str(dia.id)]
        await m.reply_text(
            f"{em.sukses}**SPAM DETECTED, {em.block}BLOCKED USER AUTOMATICALLY!**"
        )
        return await c.block_user(dia.id)
    dB.set_flood(gw, dia.id, flood[str(dia.id)])
    full = f"<a href=tg://user?id={dia.id}>{dia.first_name} {dia.last_name or ''}</a>"
    dB.add_userdata(
        dia.id, dia.first_name, dia.last_name, dia.username, dia.mention, full, dia.id
    )
    try:
        x = await c.get_inline_bot_results(
            bot_username, f"ambil_tombolpc {str(dia.id)}"
        )
        xx = await c.send_inline_bot_result(dia.id, x.query_id, x.results[0].id)
        flood2[str(dia.id)] = int(xx.updates[0].id)
        return
    except:
        lah = dB.get_var(gw, "PMPIC")
        tekss = await escape_tag(c, dia.id, pm_text, parse_words)
        if lah:
            kok_poto = m.reply_video if lah.endswith(".mp4") else m.reply_photo
            rplied_msg = await kok_poto(
                lah, caption=INLINE_WARN.format(tekss, flood[str(dia.id)], pm_warns)
            )
        else:
            rplied_msg = await m.reply(
                INLINE_WARN.format(tekss, flood[str(dia.id)], pm_warns)
            )
        flood2[str(dia.id)] = rplied_msg.id
        return
