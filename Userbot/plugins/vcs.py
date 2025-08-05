from random import randint
from typing import Optional

from pyrogram import enums
from pyrogram.errors import Forbidden
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import (CreateGroupCall, DiscardGroupCall,
                                          EditGroupCallTitle)
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pytgcalls.exceptions import (AlreadyJoinedError, GroupCallNotFound,
                                  NoActiveGroupCall, NotInCallError)

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "VideoChat"

USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_vcs")


async def get_group_call(c: nlx, m, _, err_msg: str = "") -> Optional[InputGroupCall]:
    em = Emojik(c)
    em.initialize()
    chat_peer = await c.resolve_peer(m.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await c.invoke(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await c.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await m.reply(_("vc_1").format(em.gagal, err_msg))
    return False


@zb.ubot("startvc")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    flags = " ".join(m.command[1:])
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    zb = await m.reply(_("proses").format(em.proses, proses_))
    if flags == enums.ChatType.CHANNEL:
        chat_id = m.chat.title
    else:
        chat_id = m.chat.id
    args = _("vc_2").format(em.sukses)
    try:
        await c.invoke(
            CreateGroupCall(
                peer=(await c.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
            )
        )
        await zb.edit(args)
        return
    except Exception as e:
        await zb.edit(_("err").format(em.gagal, e))
        return


@zb.ubot("stopvc")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    zb = await m.reply(_("proses").format(em.proses, proses_))
    if not (group_call := (await get_group_call(c, m, _, err_msg=", Error..."))):
        return
    await c.invoke(DiscardGroupCall(call=group_call))
    await zb.edit(_("vc_3").format(em.sukses))
    return


"""
Ini Gw Bikin Dewek Ya Anj, Kalo Masih Dikata Copas Coba Cari Jing. ANAK KONTOL EMANG LOE PADA !!
"""


@zb.ubot("vctitle")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    txt = c.get_arg(m)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    zb = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.command) < 2:
        await zb.edit(_("vc_4").format(em.gagal, m.command))
        return
    if not (group_call := (await get_group_call(c, m, _, err_msg=", Error..."))):
        return
    try:
        await c.invoke(EditGroupCallTitle(call=group_call, title=f"{txt}"))

    except Forbidden:
        await zb.edit(_("vc_5").format(em.gagal))
        return
    await zb.edit(_("vc_6").format(em.sukses, txt))
    return


@zb.ubot("joinos")
@zb.thecegers
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    zb = await m.reply(_("proses").format(em.proses, proses_))
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    sk = 0
    gl = 0
    if "/+" in str(chat_id):
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        for X in nlx._ubot:
            try:
                await X.call_py.play(chat_id)
                await X.call_py.mute_stream(chat_id)
                sk += 1
            except:
                gl += 1
                continue
        await zb.delete()
        return await m.reply(
            "<b>{} Berhasil Naik Os:\nChat ID: `{}`\nSukses `{}`\nGagal `{}`\nDari Total Userbot: {}</b>".format(
                em.sukses, chat_id, sk, gl, len(nlx._ubot)
            )
        )
    except Exception as e:
        await zb.delete()
        return await m.reply(_("err").format(em.gagal, e))


@zb.ubot("turunos")
@zb.thecegers
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    zb = await m.reply(_("proses").format(em.proses, proses_))
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    sk = 0
    gl = 0
    if "/+" in str(chat_id):
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        for X in nlx._ubot:
            try:
                await X.call_py.leave_call(chat_id)
                sk += 1
            except:
                gl += 1
                continue
        await zb.delete()
        return await m.reply(
            "<b>{} Berhasil Turun Os:\nChat ID: `{}`\nSukses `{}`\nGagal `{}`\nDari Total Userbot: {}</b>".format(
                em.sukses, chat_id, sk, gl, len(nlx._ubot)
            )
        )
    except Exception as e:
        await zb.delete()
        return await m.reply(_("err").format(em.gagal, e))


@zb.ubot("joinvc")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    zb = await m.reply(_("proses").format(em.proses, proses_))
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    if "/+" in str(chat_id):
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        chat = await c.get_chat(chat_id)
        title = chat.title
    except:
        title = "Private"
    if chat_id:
        try:
            await c.call_py.play(chat_id)
            await c.call_py.mute_stream(chat_id)
            await m.reply(_("vc_7").format(em.sukses, title))

        except NoActiveGroupCall:
            await m.reply(_("vc_10").format(em.gagal, title))
        except AlreadyJoinedError:
            await m.reply(_("vc_10").format(em.sukses, title))
        except GroupCallNotFound:
            await c.call_py.play(chat_id)
            await c.call_py.mute_stream(chat_id)
            await m.reply(_("vc_7").format(em.sukses, title))

        except Exception as e:
            await m.reply(_("err").format(em.gagal, e))
        return await zb.delete()
    else:
        return


@zb.ubot("leavevc")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    zb = await m.reply(_("proses").format(em.proses, proses_))
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    if "/+" in str(chat_id):
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    elif "t.me/" in str(chat_id) or "@" in str(chat_id):
        chat_id = chat_id.replace("https://t.me/", "")
        gid = await c.get_chat(str(chat_id))
        chat_id = int(gid.id)
    else:
        chat_id = int(chat_id)
    try:
        chat = await c.get_chat(chat_id)
        title = chat.title
    except:
        title = "Private"
    if chat_id:
        try:
            await c.call_py.leave_call(chat_id)
            await zb.edit(_("vc_9").format(em.sukses, title))
            return
        except NotInCallError:
            return await zb.edit(_("vc_13").format(em.gagal, title))
        except Exception as e:
            await zb.edit(_("err").format(em.gagal, e))
            return
    else:
        return
