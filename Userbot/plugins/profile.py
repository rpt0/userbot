import os
from io import BytesIO

from pyrogram.enums import ChatMemberStatus, ChatType

from Userbot import logger, nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Profile"


def help_string(org):
    return h_s(org, "help_prof")


@zb.ubot("unblock")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    user_id = await c.extract_user(m)
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    tex = await m.reply(_("proses").format(em.proses, proses_))
    if not user_id:
        return await tex.edit(_("prof_1").format(em.gagal))
    if user_id == c.me.id:
        await tex.delete()
        return
    await c.unblock_user(user_id)
    umention = (await c.get_users(user_id)).mention
    await tex.edit(_("prof_2").format(em.sukses, umention))
    return


@zb.ubot("block")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    user_id = await c.extract_user(m)
    if not user_id:
        return await m.reply(_("prof_1").format(em.gagal))
    if user_id == c.me.id:
        return
    await c.block_user(user_id)
    umention = (await c.get_users(user_id)).mention
    await m.reply(_("prof_3").format(em.sukses, umention))
    return


@zb.ubot("setname")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    tex = await m.reply(_("proses").format(em.proses, proses_))
    direp = m.reply_to_message
    if direp:
        name = direp.text
        await c.update_profile(first_name=name)
        await tex.edit(_("prof_4").format(em.sukses, name))
        return
    if len(m.command) == 2:
        name = m.text.split(None, 1)[1]
        await c.update_profile(first_name=name)
        await tex.edit(_("prof_4").format(em.sukses, name))
        return
    elif len(m.command) == 3:
        name = m.text.split(None, 2)[1]
        last = m.text.split(None, 2)[2]
        await c.update_profile(first_name=name, last_name=last)
        await tex.edit(_("prof_5").format(em.sukses, name, last))
        return
    else:
        await tex.edit(_("gcs_1").format(em.gagal))
        return


@zb.ubot("setbio")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    tex = await m.reply(_("proses").format(em.proses, proses_))
    direp = m.reply_to_message
    if direp:
        bio = direp.text
    else:
        bio = m.text.split(None, 1)[1]
    try:
        await c.update_profile(bio=bio)
        await tex.edit(_("prof_6").format(em.sukses, bio))
        return
    except Exception as e:
        await tex.edit(_("err").format(em.gagal, e))
        return


@zb.ubot("meadmin")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    bacot = await m.reply(_("proses").format(em.proses, proses_))
    a_chats = []
    me = await c.get_me()

    try:
        async for dialog in c.get_dialogs():
            try:
                if dialog.chat.type == ChatType.SUPERGROUP:
                    gua = await dialog.chat.get_member(int(me.id))
                    if gua.status in (
                        ChatMemberStatus.OWNER,
                        ChatMemberStatus.ADMINISTRATOR,
                    ):
                        a_chats.append(dialog.chat)
            except Exception as e:
                logger.error(f"An error occurred while processing dialog: {e}")
                continue

        text = ""
        j = 0
        for chat in a_chats:
            try:
                title = chat.title
            except Exception:
                title = "Private Group"
            if chat.username:
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{chat.username})[`{chat.id}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{chat.id}`]\n"
            j += 1

        if not text:
            await bacot.edit_text(_("prof_7").format(em.gagal))
            return
        elif len(text) > 4096:
            with BytesIO(str.encode(text)) as out_file:
                out_file.name = "adminlist.txt"
                await m.reply_document(document=out_file)
                await bacot.delete()
                return
        else:
            await bacot.edit_text(
                _("prof_8").format(em.sukses, len(a_chats), text),
                disable_web_page_preview=True,
            )
            return
    except Exception as e:
        logger.error(f"An error occurred while fetching dialogs: {e}")
        return


@zb.ubot("setpp")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    replied = m.reply_to_message
    try:
        pat = await replied.download()
        if replied.photo:
            await c.set_profile_photo(photo=pat)
        elif replied.video:
            await c.set_profile_photo(video=pat)
        os.remove(pat)
        return await m.reply(_("prof_9").format(em.sukses))
    except Exception as e:
        return await m.reply(_("err").format(em.gagal, e))


@zb.ubot("purgeme")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.command) != 2:
        return await m.delete()
    n = m.reply_to_message if m.reply_to_message else m.text.split(None, 1)[1].strip()
    if not n.isnumeric():
        return
    n = int(n)
    if n < 1:
        return
    chat_id = m.chat.id
    message_ids = [
        m.id
        async for m in c.search_messages(
            chat_id,
            from_user=int(m.from_user.id),
            limit=n,
        )
    ]
    if not message_ids:
        return
    to_delete = [message_ids[i : i + 999] for i in range(0, len(message_ids), 999)]
    for hundred_messages_or_less in to_delete:
        return await c.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )
