import asyncio
import sys
from datetime import datetime
from enum import IntEnum, unique

from pyrogram import enums
from pyrogram.errors import (ChannelPrivate, ChatForwardsRestricted,
                             ChatWriteForbidden, FloodWait, MessageEmpty,
                             MessageIdInvalid)
from pyrogram.helpers import ikb
from pytz import timezone

from config import dump
from Userbot import bot, logger, nlx
from Userbot.helper.database import dB, state
from Userbot.helper.tools import (Emojik, capture_err, create_logs, h_s,
                                  initial_ctext, zb)

__MODULES__ = "Logger"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_gruplog")


logger_cache = {}
reply_cache = []


@unique
class Types(IntEnum):
    TEXT = 1
    DOCUMENT = 2
    PHOTO = 3
    VIDEO = 4
    STICKER = 5
    AUDIO = 6
    VOICE = 7
    VIDEO_NOTE = 8
    ANIMATION = 9
    ANIMATED_STICKER = 10
    CONTACT = 11


async def send_media(c, msgtype: int):
    GET_FORMAT = {
        Types.TEXT.value: c.send_message,
        Types.DOCUMENT.value: c.send_document,
        Types.PHOTO.value: c.send_photo,
        Types.VIDEO.value: c.send_video,
        Types.STICKER.value: c.send_sticker,
        Types.AUDIO.value: c.send_audio,
        Types.VOICE.value: c.send_voice,
        Types.VIDEO_NOTE.value: c.send_video_note,
        Types.ANIMATION.value: c.send_animation,
        Types.ANIMATED_STICKER.value: c.send_sticker,
        Types.CONTACT.value: c.send_contact,
    }
    return GET_FORMAT[msgtype]


async def message_mapping(client, message):
    type_mapping = {
        "text": {"media": message.text, "send_function": bot.send_message},
        "photo": {"media": message.photo, "send_function": bot.send_photo},
        "voice": {"media": message.voice, "send_function": bot.send_voice},
        "audio": {"media": message.audio, "send_function": bot.send_audio},
        "video": {"media": message.video, "send_function": bot.send_video},
        "video_note": {
            "media": message.video_note,
            "send_function": bot.send_video_note,
        },
        "animation": {"media": message.animation, "send_function": bot.send_animation},
        "sticker": {"media": message.sticker, "send_function": bot.send_sticker},
        "document": {"media": message.document, "send_function": bot.send_document},
    }

    message_type = None
    send_function = None
    file_path = None

    for media_type, media_info in type_mapping.items():
        if media_info["media"]:
            message_type = media_type
            send_function = media_info["send_function"]
            if media_type != "text":
                file_path = await client.download_media(media_info["media"])
            break
    return media_type, message_type, send_function, file_path


@zb.ubot("gruplog")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    proses = await message.reply(f"{em.proses}**{proses_}**")
    cek = client.get_arg(message)
    status = dB.get_var(client.me.id, "NEW_LOG")
    if cek.lower() == "on":
        if not status:
            try:
                link = await create_logs(client)
                return await proses.edit(
                    f"{em.sukses}**Succesfully enabled pm and tag logs!! Please check {link}**",
                    disable_web_page_preview=True,
                )
            except Exception as er:
                return await proses.edit(
                    f"{em.gagal}**ERROR: `{str(er)}`, Silahkan lapor ke admins.**"
                )
        else:
            return await proses.edit(
                f"{em.sukses}<b>Pm and tag logs already enable!!</b>"
            )
    if cek.lower() == "off":
        if status:
            dB.remove_var(client.me.id, "NEW_LOG")
            return await proses.edit(
                f"{em.sukses}<b>Succesfully disabled pm and tag logs!!</b>"
            )
        else:
            return await proses.edit(
                f"{em.gagal}<b>Pm and tag logs already disabled!!</b>"
            )

    else:
        return await proses.edit(f"{em.gagal}<b>Please give query on or off!!</b>")



@zb.nocmd("LOGS_GROUP", nlx)
@capture_err
async def _(client, message, _):
    
    log = dB.get_var(client.me.id, "NEW_LOG")
    if not log or message.chat.id == 777000:
        return
    from_user = (
        message.chat
        if message.chat.type == enums.ChatType.PRIVATE
        else message.from_user
    )
    if message.sender_chat:
        if message.sender_chat.username is None:
            user_link = f"{message.sender_chat.title}"
        else:
            user_link = f"[{message.sender_chat.title}](https://t.me/{message.sender_chat.username}"
    else:
        user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
    message_link = (
        message.link
        if message.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP)
        else f"tg://openmessage?user_id={from_user.id}&message_id={message.id}"
    )
    tanggal = datetime.now(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
    txt = message.text or message.caption or ""
    media_type, message_type, send_function, file_path = await message_mapping(
        client, message
    )
    state.set(from_user.id, "BEFORE", txt)
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        text = f"""
📨 <b><u>Group Notifications</u></b>

• <b>Name Group: {message.chat.title}</b>
• <b>ID Group:</b> <code>{message.chat.id}</code>
• <b>From User: {user_link}</b>

• <b>From User ID: `{from_user.id}`</b>
• <b>Message:</b> <blockquote>{txt}</blockquote>
• <b>Message Type:</b> <u><b>{message_type}</b></u>

• <b>Date:</b> <b>{tanggal}</b>
"""
        try:
            await asyncio.sleep(0.5)
            sent = await bot.send_message(
                int(log),
                text,
                disable_web_page_preview=True,
                reply_markup=ikb([[("Link Message", f"{message_link}", "url")]]),
            )
            data = {"chat": message.chat.id, "id": message.id}
            state.set(sent.id, "REPLY", data)

            return

        except ChatForwardsRestricted:
            return f"Error ChatForwardsRestricted {message.chat.id}"
        except MessageIdInvalid:
            return f"Error MessageIdInvalid {message.chat.id}"
        except ChannelPrivate:
            return f"Error ChannelPrivate {message.chat.id}"
        except FloodWait as e:
            await asyncio.sleep(e.value)
            sent = await bot.send_message(
                int(log),
                text,
                disable_web_page_preview=True,
                reply_markup=ikb([[("Link Message", f"{message_link}", "url")]]),
            )
            data = {"chat": message.chat.id, "id": message.id}
            state.set(sent.id, "REPLY", data)

    else:
        text = f"""
📨 <b><u>Private Notifications</u></b>

• <b>From: {user_link}</b>
• <b>From User ID: `{from_user.id}`</b>

• <b>Message:</b> <blockquote>{txt}</blockquote>
• <b>Message Type:</b> <u><b>{message_type}</b></u>

• <b>Date:</b> <b>{tanggal}</b>
"""
        if send_function is not None:
            return await send_to_pm(
                client,
                message,
                text,
                log,
                message_link,
                media_type,
                file_path,
                send_function,
            )


def get_reply_data(reply):
    data = state.get(reply.id, "REPLY")
    if data:
        chat_id = int(data["chat"])
        message_id = int(data["id"])
        return chat_id, message_id
    else:
        return None, None


@zb.nocmd("REPLY", nlx)
@zb.is_log
async def _(client, message, _):
    log = dB.get_var(client.me.id, "NEW_LOG")
    if log is None:
        return
    reply = message.reply_to_message
    chat_id, reply_message_id = get_reply_data(reply)
    if chat_id is None:
        return
    args = {
        "photo": message.photo,
        "voice": message.voice,
        "audio": message.audio,
        "video": message.video,
        "video_note": message.video_note,
        "animation": message.animation,
        "sticker": message.sticker,
        "document": message.document,
    }
    kwargs = {
        "photo": client.send_photo,
        "voice": client.send_voice,
        "audio": client.send_audio,
        "video": client.send_video,
        "video_note": client.send_video_note,
        "animation": client.send_animation,
        "document": client.send_document,
        "sticker": client.send_sticker,
    }
    if message.text:
        await client.send_message(
            chat_id, message.text, reply_to_message_id=reply_message_id
        )
    elif message.sticker:
        await client.send_sticker(
            chat_id, message.sticker.file_id, reply_to_message_id=reply_message_id
        )
    elif message.video_note:
        await client.send_video_note(
            chat_id,
            message.video_note.file_id,
            reply_to_message_id=reply_message_id,
        )
    else:
        media_type = next((key for key, value in args.items() if value), None)
        if media_type:
            await kwargs[media_type](
                chat_id,
                args[media_type].file_id,
                caption=message.caption or "",
                reply_to_message_id=reply_message_id,
            )


@zb.edited()
async def _(client, message):
    log = dB.get_var(client.me.id, "NEW_LOG")
    if not log or message.chat.id == 777000:
        return
    media_type, message_type, send_function, file_path = await message_mapping(
        client, message
    )
    tanggal = datetime.now(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
    txt = message.text or message.caption or ""
    from_user = (
        message.chat
        if message.chat.type == enums.ChatType.PRIVATE
        else message.from_user
    )
    user_link = f"[{from_user.first_name} {from_user.last_name or ''}](tg://user?id={from_user.id})"
    message_link = (
        message.link
        if message.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP)
        else f"tg://openmessage?user_id={from_user.id}&message_id={message.id}"
    )
    edited = state.get(from_user.id, "BEFORE")
    text = f"""
📨 <b><u>Edited Message</u></b>

• <b>From: {user_link}</b>
• <b>From User ID: `{from_user.id}`</b>

• <b>Before:</b> <blockquote>{edited}</blockquote>
• <b>After:</b> <blockquote>{txt}</blockquote>

• <b>Message Type:</b> <u><b>{message_type}</b></u>
• <b>Date:</b> <b>{tanggal}</b>"""
    button = ikb([[("Link Message", f"{message_link}", "url")]])
    return await bot.send_message(
        int(log), text, disable_web_page_preview=True, reply_markup=button
    )


@zb.deleted()
async def _(client, messages):
    log = dB.get_var(client.me.id, "NEW_LOG")
    for message in messages:
        try:
            if not log or not message or not message.chat:
                continue

            is_private = message.chat.type == enums.ChatType.PRIVATE
            mentions = bool(
                message.entities
                and any(entity.type == "mention" for entity in message.entities)
            )
            tanggal = datetime.now(timezone("Asia/Jakarta")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if not (is_private or mentions):
                continue

            text = f"""
📨 **Deleted Message** 
- Chat: {"Private" if is_private else "Group"} 
- Chat ID: `{message.chat.id}`
- Date: `{tanggal}`
"""
            await bot.send_message(int(log), text)

        except AttributeError:
            continue


async def send_to_pm(
    client, message, text, log, message_link, media_type, file_path, send_function
):
    button = ikb([[("Link Message", f"{message_link}", "url")]])
    try:
        await asyncio.sleep(0.5)

        if media_type == "text":
            sent = await send_function(
                int(log),
                text,
                disable_web_page_preview=True,
                reply_markup=button,
            )

            data = {"chat": message.chat.id, "id": message.id}
            state.set(sent.id, "REPLY", data)

        elif media_type in ["sticker", "video_note"]:
            kwargs = {
                "chat_id": int(log),
                media_type: file_path,
                "reply_markup": button,
            }
            send = await send_function(**kwargs)
            sent = await bot.send_message(
                int(log),
                text,
                reply_markup=button,
                reply_to_message_id=send.id,
            )

            data = {"chat": message.chat.id, "id": message.id}
            state.set(sent.id, "REPLY", data)

            return

        else:
            kwargs = {
                "chat_id": int(log),
                media_type: file_path,
                "caption": text,
                "reply_markup": button,
            }
            sent = await send_function(**kwargs)

            data = {"chat": message.chat.id, "id": message.id}
            state.set(sent.id, "REPLY", data)

    except (
        ChatForwardsRestricted,
        MessageIdInvalid,
        ChatWriteForbidden,
        MessageEmpty,
    ) as err:
        return f"Error: {str(err)}"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_to_pm(
            client,
            message,
            text,
            log,
            message_link,
            media_type,
            file_path,
            send_function,
        )
