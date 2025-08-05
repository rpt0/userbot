################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Gojo_Satoru || William Butcher
"""
################################################################

import asyncio

from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.errors import (BotChannelsNa, ChatAdminRequired, PeerIdInvalid,
                             RightForbidden, RPCError, UserAdminInvalid,
                             UserCreator)
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import ChatPermissions, ChatPrivileges

from config import DEVS
from Userbot import logger, nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb, mention_html

__MODULES__ = "Admin"


def help_string(org):
    return h_s(org, "help_rest")


async def admin_check(m, org):
    c = m._client
    status = (await c.get_chat_member(m.chat.id, org)).status
    adming = [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
    if status not in adming:
        return False
    return True


async def member_check(message, org) -> bool:
    client = message._client
    check_user = (
        await client.get_chat_member(message.chat.id, message.from_user.id)
    ).privileges
    user_type = check_user.status
    if user_type == ChatMemberStatus.MEMBER:
        return False
    if user_type == ChatMemberStatus.ADMINISTRATORS:
        add_adminperm = check_user.can_promote_members
        return bool(add_adminperm)
    return True


@zb.ubot("purge")
async def _(c: nlx, m, _):
    await m.delete()
    if not m.reply_to_message:
        return
    chat_id = m.chat.id
    message_ids = []
    for message_id in range(
        m.reply_to_message.id,
        m.id,
    ):
        message_ids.append(message_id)
        if len(message_ids) == 100:
            return await c.delete_messages(
                chat_id=chat_id,
                message_ids=message_ids,
                revoke=True,
            )
            message_ids = []
    if len(message_ids) > 0:
        return await c.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True,
        )


@zb.ubot("kick|delkick")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    user_id, reason = await c.extract_user_and_reason(m)
    if not user_id:
        return await m.reply_text(_("glbl_2").format(em.gagal))
    if user_id == c.me.id:
        return await m.reply_text(_("res_1").format(em.gagal))
    if user_id in DEVS:
        return await m.reply_text(_("glbl_3").format(em.gagal))
    try:
        mention = (await c.get_users(user_id)).mention
    except PeerIdInvalid:
        mention = user_id
    except KeyError:
        mention = user_id
    msg = _("res_2").format(
        em.profil,
        mention,
        em.warn,
        m.from_user.mention if m.from_user else "Anon",
        em.block,
        reason or "No Reason Provided.",
    )
    if m.command[0][0] == "d":
        await m.reply_to_message.delete()
        await m.delete()
    try:
        await m.chat.ban_member(user_id)
    except UserAdminInvalid:
        return await m.reply_text(_("res_3").format(em.gagal))
    except PeerIdInvalid:
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        return await m.reply_text(_("peer").format(em.gagal))
    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    await m.reply_text(msg)
    await asyncio.sleep(1)
    return await m.chat.unban_member(user_id)


@zb.ubot("ban|delban")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    user_id, reason = await c.extract_user_and_reason(m)
    if not user_id:
        return await m.reply_text(_("glbl_2").format(em.gagal))
    if user_id == c.me.id:
        return await m.reply_text(_("res_4").format(em.gagal))
    if user_id in DEVS:
        return await m.reply_text(_("glbl_3").format(em.gagal))
    try:
        mention = (await c.get_users(user_id)).mention
    except PeerIdInvalid:
        mention = user_id
    except KeyError:
        mention = user_id
    msg = _("res_5").format(
        em.profil,
        mention,
        em.warn,
        m.from_user.mention if m.from_user else "Anon",
        em.block,
        reason or "No Reason Provided.",
    )
    if m.command[0][0] == "d":
        await m.reply_to_message.delete()
        await m.delete()
    try:
        await m.chat.ban_member(user_id)
    except UserAdminInvalid:
        return await m.reply_text(_("res_3").format(em.gagal))
    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    except PeerIdInvalid:
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        return await m.reply_text(_("peer").format(em.gagal))
    return await m.reply_text(msg)


@zb.ubot("unban")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    reply = m.reply_to_message

    if reply and reply.sender_chat and reply.sender_chat != m.chat.id:
        return await m.reply_text(_("res_3").format(em.gagal))
    if len(m.command) == 2:
        user = m.text.split(None, 1)[1]
    elif len(m.command) == 1 and reply:
        user = m.reply_to_message.from_user.id
    else:
        return await m.reply_text(_("prof_1").format(em.gagal))
    try:
        await m.chat.unban_member(user)
    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    umention = (await c.get_users(user)).mention
    return await m.reply_text(_("res_6").format(em.sukses, umention))


@zb.ubot("del")
async def _(c: nlx, m, _):
    await m.delete()
    try:
        return await m.reply_to_message.delete()
    except:
        pass


@zb.ubot("pin|unpin")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if not m.reply_to_message:
        return await m.reply_text(_("res_7").format(em.gagal))
    r = m.reply_to_message
    if m.command[0][0] == "u":
        await r.unpin()
        return await m.reply_text(
            _("res_8").format(em.sukses, r.link), disable_web_page_preview=True
        )
    await r.pin(disable_notification=True)
    return await m.reply(
        _("res_9").format(em.sukses, r.link), disable_web_page_preview=True
    )


@zb.ubot("mute|delmute")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    user_id, reason = await c.extract_user_and_reason(m)
    if not user_id:
        return await m.reply_text(_("glbl_2").format(em.gagal))
    if user_id == c.me.id:
        return await m.reply_text(_("res_10").format(em.gagal))
    if user_id in DEVS:
        return await m.reply_text(_("glbl_3").format(em.gagal))
    try:
        mention = (await c.get_users(user_id)).mention
    except PeerIdInvalid:
        mention = user_id
    except KeyError:
        mention = user_id
    msg = _("res_11").format(
        em.profil,
        mention,
        em.warn,
        m.from_user.mention if m.from_user else "Anon",
        em.block,
        reason or "No Reason Provided.",
    )
    if m.command[0][0] == "d":
        await m.reply_to_message.delete()
        await m.delete()
    try:
        await m.chat.restrict_member(user_id, permissions=ChatPermissions())
        return await m.reply_text(msg)
    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    except RightForbidden:
        return await m.reply_text(_("res_13").format(em.gagal))
    except UserAdminInvalid:
        return await m.reply_text(_("res_3").format(em.gagal))
    except PeerIdInvalid:
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        return await m.reply_text(_("peer").format(em.gagal))
    except RPCError:
        return
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal, e))


@zb.ubot("unmute")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    user_id = await c.extract_user(m)
    if not user_id:
        return await m.reply_text(_("glbl_2").format(em.gagal))
    try:
        await m.chat.unban_member(user_id)
        umention = (await c.get_users(user_id)).mention
        return await m.reply_text(_("res_14").format(em.sukses, umention))
    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    except RightForbidden:
        return await m.reply_text(_("res_13").format(em.gagal))
    except UserAdminInvalid:
        return await m.reply_text(_("res_3").format(em.gagal))
    except PeerIdInvalid:
        return await m.reply_text(_("peer").format(em.gagal))
    except KeyError:
        return await m.reply_text(_("peer").format(em.gagal))
    except RPCError:
        return
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal, e))


@zb.ubot("zombies")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    chat_id = m.chat.id
    deleted_users = []
    banned_users = 0
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    mt = await m.reply(_("proses").format(em.proses, proses_))

    async for i in c.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if len(deleted_users) > 0:
        for deleted_user in deleted_users:
            try:
                await m.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        return await mt.edit(_("res_15").format(em.sukses, banned_users))
    else:
        return await mt.edit(_("res_16").format(em.gagal))


@zb.ubot("report")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if not m.reply_to_message:
        return await m.reply_text(_("res_18").format(em.gagal))

    reply = m.reply_to_message
    reply_id = reply.from_user.id if reply.from_user else reply.sender_chat.id
    user_id = m.from_user.id if m.from_user else m.sender_chat.id
    if reply_id == user_id:
        return await m.reply_text(_("res_19").format(em.gagal))

    list_of_admins = await admin_check(m, user_id)
    linked_chat = (await c.get_chat(m.chat.id)).linked_chat
    if linked_chat is not None:
        if (
            list_of_admins == True
            and reply_id == m.chat.id
            or reply_id == linked_chat.id
        ):
            return await m.reply_text(_("res_20").format(em.gagal))
    else:
        if list_of_admins == True and reply_id == m.chat.id:
            return await m.reply_text(_("res_20").format(em.gagal))

    user_mention = (
        reply.from_user.mention if reply.from_user else reply.sender_chat.title
    )
    text = _("res_21").format(em.warn, user_mention)
    admin_data = [
        i
        async for i in c.get_chat_members(
            chat_id=m.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]  # will it give floods ???
    for admin in admin_data:
        if admin.user.is_bot or admin.user.is_deleted:
            # return bots or deleted admins
            continue
        text += f"[\u2063](tg://user?id={admin.user.id})"
    return await m.reply_to_message.reply_text(text)


@zb.ubot("fullpromote")
@zb.devs("mfullpromote")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(_("prof_1").format(em.gagal))
        return
    user_id, ah = await c.extract_user_and_reason(m)
    user = await c.get_users(user_id)
    meko = await c.get_chat_member(m.chat.id, c.me.id)
    if user_id == c.me.id:
        await m.reply_text(_("res_22").format(em.gagal))
        return
    if not meko.privileges.can_promote_members:
        await m.reply_text(_("res_13").format(em.gagal))
        return
    try:
        title = "anak jembut"
        if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            if len(m.text.split()) == 3 and not m.reply_to_message:
                title = " ".join(m.text.split()[2:16])
            elif len(m.text.split()) >= 2 and m.reply_to_message:
                title = " ".join(m.text.split()[1:16])
        await c.promote_chat_member(
            chat_id=m.chat.id, user_id=user_id, privileges=meko.privileges
        )
        await c.set_administrator_title(m.chat.id, user_id, title)

        promoter = await mention_html(m.from_user.first_name, m.from_user.id)
        promoted = await mention_html(user.first_name, user.id)
        return await m.reply_text(
            _("res_23").format(em.profil, promoter, em.warn, promoted)
        )

    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    except UserAdminInvalid:
        return await m.reply_text(_("res_3").format(em.gagal))
    except RPCError:
        return
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal, e))


@zb.ubot("promote")
@zb.devs("mpromote")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(_("prof_1").format(em.gagal))
        return
    user_id, ah = await c.extract_user_and_reason(m)
    try:
        user = await c.get_users(user_id)
    except PeerIdInvalid:
        return await m.reply_text(_("peer").format(em.gagal))
    meko = await c.get_chat_member(m.chat.id, c.me.id)
    if user_id == c.me.id:
        await m.reply_text(_("res_22").format(em.gagal))
        return
    if not meko.privileges.can_promote_members:
        await m.reply_text(_("res_13").format(em.gagal))
        return
    try:
        title = "anak jembut"
        if m.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            if len(m.text.split()) >= 3 and not m.reply_to_message:
                title = " ".join(m.text.split()[2:16])
            elif len(m.text.split()) >= 2 and m.reply_to_message:
                title = " ".join(m.text.split()[1:16])
        await c.promote_chat_member(
            chat_id=m.chat.id,
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ),
        )
        await c.set_administrator_title(m.chat.id, user_id, title)
        promoter = await mention_html(m.from_user.first_name, m.from_user.id)
        promoted = await mention_html(user.first_name, user.id)
        return await m.reply_text(
            _("res_24").format(em.profil, promoter, em.warn, promoted)
        )

    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    except UserAdminInvalid:
        return await m.reply_text(_("res_3").format(em.gagal))
    except RPCError:
        return
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal, e))


@zb.ubot("demote")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(_("prof_1").format(em.gagal))
        return
    user_id, ah = await c.extract_user_and_reason(m)
    user = await c.get_users(user_id)
    if user_id == c.me.id:
        await m.reply_text(_("res_19").format(em.gagal))
        return
    botol = await admin_check(m, c.me.id)
    if not botol:
        await m.reply_text(_("res_25").format(em.gagal))
        return
    try:
        await m.chat.promote_member(
            user_id=user_id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            ),
        )
        demoter = await mention_html(m.from_user.first_name, m.from_user.id)
        demoted = await mention_html(user.first_name, user.id)
        return await m.reply_text(
            _("res_26").format(em.profil, demoter, em.warn, demoted)
        )
    except BotChannelsNa:
        return await m.reply_text(_("res_27").format(em.gagal))
    except ChatAdminRequired:
        return await m.reply_text(_("res_12").format(em.gagal))
    except UserAdminInvalid:
        return await m.reply_text(_("res_3").format(em.gagal))
    except RPCError:
        return
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal, e))


@zb.ubot("gctitle")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(_("gcs_1").format(em.gagal))
        return
    if m.reply_to_message:
        gtit = m.reply_to_message.text
    else:
        gtit = m.text.split(None, 1)[1]
    try:
        await m.chat.set_title(gtit)
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal), e)
    return await m.reply_text(_("res_28").format(em.sukses, m.chat.title, gtit))


@zb.ubot("gcdes")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.text.split()) == 1 and not m.reply_to_message:
        await m.reply_text(_("gcs_1").format(em.gagal))
        return
    if m.reply_to_message:
        desp = m.reply_to_message.text
    else:
        desp = m.text.split(None, 1)[1]
    try:
        await m.chat.set_description(desp)
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal), e)
    return await m.reply_text(_("res_29").format(em.sukses, m.chat.description, desp))


@zb.ubot("title")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.text.split()) == 1 and not m.reply_to_message:
        return await m.reply_text(_("prof_1").format(em.gagal))
    if m.reply_to_message:
        if len(m.text.split()) >= 2:
            reason = m.text.split(None, 1)[1]
    else:
        if len(m.text.split()) >= 3:
            reason = m.text.split(None, 2)[2]
    user_id, aw = await c.extract_user_and_reason(m)
    if not user_id:
        return await m.reply_text(_("glbl_2").format(em.gagal))
    if user_id == c.me.id:
        return await m.reply_text(_("res_19").format(em.gagal))
    if not reason:
        return await m.reply_text(_("res_30").format(em.gagal))
    from_user = await c.get_users(user_id)
    title = reason
    try:
        await c.set_administrator_title(m.chat.id, from_user.id, title)
    except Exception as e:
        return await m.reply_text(_("err").format(em.gagal, e))
    except UserCreator:
        return await m.reply_text(_("res_31").format(em.gagal))
    return await m.reply_text(_("res_32").format(em.sukses, from_user.mention, title))


@zb.ubot("gcpic")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if not m.reply_to_message:
        return await m.reply_text(_("res_33").format(em.gagal))
    if (
        not m.reply_to_message.photo
        and not m.reply_to_message.document
        and not m.reply_to_message.video
    ):
        return await m.reply_text(_("res_33").format(em.gagal))

    if m.reply_to_message:
        if m.reply_to_message.photo:
            await c.set_chat_photo(m.chat.id, photo=m.reply_to_message.photo.file_id)
            return await m.reply_text(_("res_34").format(em.sukses))
        if m.reply_to_message.document:
            await c.set_chat_photo(m.chat.id, photo=m.reply_to_message.document.file_id)
            return await m.reply_text(_("res_35").format(em.sukses))
        elif m.reply_to_message.video:
            await c.set_chat_photo(m.chat.id, video=m.reply_to_message.video.file_id)
            return await m.reply_text(_("res_36").format(em.sukses))
    else:
        return await m.reply_text(_("res_33").format(em.gagal))


@zb.ubot("hantu")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    total_deleted_messages = 0
    total_remaining_messages = 0
    async for dialog in c.get_dialogs():
        chat_id = dialog.chat.id
        if dialog.chat.type == ChatType.PRIVATE:
            deleted_messages_count = 0
            remaining_messages_count = 0
            async for hantunya in c.get_chat_history(chat_id, limit=100):
                if hantunya.from_user and hantunya.from_user.is_deleted:
                    try:
                        user_id = hantunya.from_user.id
                        info = await c.resolve_peer(user_id)
                        await c.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))
                        deleted_messages_count += 1
                    except PeerIdInvalid:
                        logger.error("ID peer tidak valid atau tidak dikenal")
                else:
                    remaining_messages_count += 1
            total_deleted_messages += deleted_messages_count
            total_remaining_messages += remaining_messages_count
    await m.reply(
        f"{em.sukses}**Berhasil menghapus : `{total_deleted_messages}`\n{em.gagal}Tersisa yang berlum terhapus : `{total_remaining_messages}`**"
    )
    return await pros.delete()
