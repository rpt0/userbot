################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


import asyncio
from io import BytesIO

from pyrogram.errors import FloodWait, MessageTooLong, PeerIdInvalid
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import ChatPermissions

from config import DEVS
from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (Emojik, h_s, initial_ctext, zb,
                                  remove_markdown_and_html)

__MODULES__ = "Global"


def help_string(org):
    return h_s(org, "help_global")


@zb.ubot("gban")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    nyet, nt = await c.extract_user_and_reason(m)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.text.split()) == 1:
        await xx.edit(_("glbl_2").format(em.gagal))
        return
    if nyet in DEVS:
        await xx.edit(_("glbl_3").format(em.gagal))
        return
    alasan = nt if nt else "Anak Dajjal 🗿"
    bs = 0
    gg = 0
    chats = await c.get_chats_dialog("global")
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = m.reply_to_message.sender_chat.title if m.reply_to_message else "Anon"
    except PeerIdInvalid:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    db_gban = dB.get_list_from_var(c.me.id, "GBANNED")
    for chat in chats:
        if nyet in db_gban:
            await xx.edit(_("glbl_5").format(em.gagal))
            return
        try:
            await c.ban_chat_member(chat, nyet)
            bs += 1
            await asyncio.sleep(0.1)
        except Exception:
            gg += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
            await c.ban_chat_member(chat, nyet)
            bs += 1
            await asyncio.sleep(0.1)

    dB.add_to_var(c.me.id, "GBANNED", nyet)
    await c.block_user(nyet)
    await c.invoke(
        DeleteHistory(peer=(await c.resolve_peer(nyet)), max_id=0, revoke=True)
    )
    mmg = _("glbl_6").format(
        em.warn, em.sukses, bs, em.gagal, gg, em.profil, mention, em.block, alasan
    )
    await xx.delete()
    return await m.reply(mmg)


@zb.ubot("ungban")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    nyet, nt = await c.extract_user_and_reason(m)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.text.split()) == 1:
        await xx.edit(_("glbl_2").format(em.gagal))
        return
    bs = 0
    gg = 0
    chats = await c.get_chats_dialog("global")
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = m.reply_to_message.sender_chat.title if m.reply_to_message else "Anon"
    except PeerIdInvalid:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    db_gban = dB.get_list_from_var(c.me.id, "GBANNED")
    for chat in chats:
        if nyet not in db_gban:
            await xx.edit(_("glbl_7").format(em.gagal))
            return
        try:
            await c.unban_chat_member(chat, nyet)
            bs += 1
            await asyncio.sleep(0.1)
        except Exception:
            gg += 1
            await asyncio.sleep(0.1)
    dB.remove_from_var(c.me.id, "GBANNED", nyet)
    await c.unblock_user(nyet)
    mmg = _("glbl_8").format(em.warn, em.sukses, bs, em.gagal, gg, em.profil, mention)
    await xx.delete()
    return await m.reply(mmg)


@zb.ubot("gmute")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    nyet, nt = await c.extract_user_and_reason(m)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.text.split()) == 1:
        await xx.edit(_("glbl_2").format(em.gagal))
        return
    if nyet in DEVS:
        await xx.edit(_("glbl_3").format(em.gagal))
        return
    alasan = nt if nt else "Anak Dajjal 🗿"
    bs = 0
    gg = 0
    chats = await c.get_common_chats(nyet)
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = m.reply_to_message.sender_chat.title if m.reply_to_message else "Anon"
    except PeerIdInvalid:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    db_gmute = dB.get_list_from_var(c.me.id, "GMUTE")
    for chat in chats:
        if nyet in db_gmute:
            await xx.edit(_("glbl_10").format(em.gagal))
            return
        try:
            await c.restrict_chat_member(chat.id, nyet, ChatPermissions())
            bs += 1
            await asyncio.sleep(0.1)
        except Exception:
            gg += 1
            await asyncio.sleep(0.1)
    dB.add_to_var(c.me.id, "GMUTE", nyet)
    mmg = _("glbl_11").format(
        em.warn, em.sukses, bs, em.gagal, gg, em.profil, mention, em.block, alasan
    )
    await xx.delete()
    return await m.reply(mmg)


@zb.ubot("ungmute")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    nyet, nt = await c.extract_user_and_reason(m)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    xx = await m.reply(_("proses").format(em.proses, proses_))
    await c.get_users(nyet)
    if len(m.text.split()) == 1:
        await xx.edit(_("glbl_2").format(em.gagal))
        return
    bs = 0
    gg = 0
    chats = await c.get_common_chats(nyet)
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = m.reply_to_message.sender_chat.title if m.reply_to_message else "Anon"
    except PeerIdInvalid:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        await xx.delete()
        return await m.reply_text(_("peer").format(em.gagal))
    db_gmute = dB.get_list_from_var(c.me.id, "GMUTE")
    for chat in chats:
        if nyet not in db_gmute:
            await xx.edit(_("glbl_12").format(em.gagal))
            return
        try:
            await c.unban_member(chat.id, nyet, ChatPermissions())
            bs += 1
            await asyncio.sleep(0.1)
        except Exception:
            gg += 1
            await asyncio.sleep(0.1)
    dB.remove_from_var(c.me.id, "GMUTE", nyet)
    mmg = _("glbl_13").format(em.warn, em.sukses, bs, em.gagal, gg, em.profil, mention)
    await xx.delete()
    return await m.reply(mmg)


@zb.ubot("gbanlist|listgban")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    db_gban = dB.get_list_from_var(c.me.id, "GBANNED")
    msg = await m.reply(_("proses").format(em.proses, proses_))

    if db_gban is None:
        return await msg.edit(_("glbl_22").format(em.gagal))
    dftr = _("glbl_14").format(em.profil)
    for ii in db_gban:
        dftr += _("glbl_15").format(em.block, ii)
    try:
        await m.reply_text(dftr)
    except MessageTooLong:
        with BytesIO(str.encode(await remove_markdown_and_html(dftr))) as f:
            f.name = "gbanlist.txt"
            await m.reply_document(document=f, caption=_("glbl_17").format(em.profil))
    return await msg.delete()


@zb.ubot("gmutelist|listgmute")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    gmnu = dB.get_list_from_var(c.me.id, "GMUTE")
    msg = await m.reply(_("proses").format(em.proses, proses_))
    if gmnu is None:
        await msg.edit(_("glbl_2").format(em.gagal))
        return
    dftr = _("glbl_18").format(em.profil)
    for ii in gmnu:
        dftr += _("glbl_19").format(em.warn, ii)
    try:
        await m.reply_text(dftr)
    except MessageTooLong:
        with BytesIO(str.encode(await remove_markdown_and_html(dftr))) as f:
            f.name = "gmutelist.txt"
            await m.reply_document(document=f, caption=_("glbl_21").format(em.profil))
    return await msg.delete()
