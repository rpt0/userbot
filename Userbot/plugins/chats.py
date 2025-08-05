import asyncio

from pyrogram.errors import PeerIdInvalid

from Userbot import logger, nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb
from Userbot.plugins.vcs import get_group_call

__MODULES__ = "Chats"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_chates")


@zb.ubot("cekmember")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        o = await c.get_chat_members_count(chat_id)
        await asyncio.sleep(1)
        return await pros.edit("{}Total members group {}".format(em.sukses, o))
    except Exception as e:
        return await pros.edit(_("err").format(em.gagal, str(e)))


@zb.ubot("cekonline")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        o = await c.get_chat_online_count(chat_id)
        await asyncio.sleep(1)
        return await pros.edit("{}Total members online group {}".format(em.sukses, o))
    except Exception as e:
        return await pros.edit(_("err").format(em.gagal, str(e)))


@zb.ubot("cekmsg")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    chat_id = m.command[1] if len(m.command) > 1 else m.chat.id
    user_id = await c.extract_user(m)
    if not user_id:
        return await m.reply_text(_("glbl_2").format(em.gagal))
    try:
        umention = (await c.get_users(user_id)).mention
    except (PeerIdInvalid, KeyError):
        return await m.reply_text(_("peer").format(em.gagal))
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        o = await c.search_messages_count(chat_id, from_user=user_id)
        await asyncio.sleep(1)
        return await pros.edit(
            "{}Total message from user {} is {} messages".format(em.sukses, umention, o)
        )
    except Exception as e:
        return await pros.edit(_("err").format(em.gagal, str(e)))


@zb.ubot("cekos")
async def _(client: nlx, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    pros = await message.reply(_("proses").format(em.proses, proses_))

    chat = message.command[1] if len(message.command) > 1 else message.chat.id
    try:
        if isinstance(chat, int):
            chat_id = chat
        else:
            chat_info = await client.get_chat(chat)
            chat_id = chat_info.id

        try:
            info = await client.get_chat(chat_id)
            title = info.title if info.title else f"{chat_id}"
        except Exception:
            title = f"{chat_id}"
        group_call = await get_group_call(client, message, _, err_msg=", Error...")
        if not group_call:
            return await pros.edit(
                "{}<b>Voice chat group not found in {}</b>".format(em.gagal, title)
            )
        try:
            participants = await client.call_py.get_participants(chat_id)
            mentions = []
            for participant in participants:
                user_id = participant.user_id
                try:
                    user = await client.get_users(user_id)
                    mention = user.mention
                    status = "Unmuted" if participant.muted else "Muted"
                    volume = participant.volume
                    mentions.append(f"{mention}|Mic: {status}|Vol: {volume}%")
                except Exception as e:
                    logger.error(f"{e}")
                    mentions.append(f"{user_id} Status Unknown")

            total_participants = len(participants)
            if total_participants == 0:
                return await pros.edit(
                    "{}<b>No someone in voice chat group!!</b>".format(em.gagal)
                )
            mentions_text = "\n".join(
                [
                    (f"• {mention}" if i < total_participants - 1 else f"• {mention}")
                    for i, mention in enumerate(mentions)
                ]
            )
            text = f"""
{em.sukses}<b>Voice Chat Listener:</b>
{em.owner}Chat: <code>{title}</code>.
{em.profil}Total: <code>{total_participants}</code> Listener.

<b>People:</b>
{mentions_text}
"""
            return await pros.edit(f"<blockquote><b>{text}</b></blockquote>")
        except Exception as e:
            return await pros.edit(_("err").format(em.gagal, e))
    except Exception as e:
        return await pros.edit(_("err").format(em.gagal, e))
