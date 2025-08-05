import asyncio
import sys
from datetime import timedelta

import wget
from pytgcalls.exceptions import NotInCallError

from config import log_pic
from Userbot import logger, nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import (Emojik, Telegram, YoutubeDownload,
                                  cek_file_ada, cleanup_files, demus_data,
                                  get_judul, h_s, initial_ctext, zb, plere,
                                  queues, run_stream)

__MODULES__ = "Streaming"
USER_PREMIUM = True

play_task = {}


def help_string(org):
    return h_s(org, "help_stream")


async def play_next_song(c: nlx, m, type, mode):
    global play_task

    chat_id = dB.get_var(c.me.id, "CHANNEL_PLAY") if mode == "ch" else m.chat.id
    chat_id = int(chat_id)
    type2 = "Channel Mode" if mode == "ch" else "Group Mode"

    if not queues.get((chat_id, c.me.id)):
        await c.call_py.leave_call(chat_id)
        queues.pop((chat_id, c.me.id), None)
        demus_data.pop((chat_id, c.me.id), None)
        return

    file_name, duration = queues[(chat_id, c.me.id)][0]
    data = demus_data.get((chat_id, c.me.id), [{}])[0]
    songname, channel, durasi, url, file, thumbnail = (
        data.get("judul"),
        data.get("mik"),
        data.get("dur"),
        data.get("url"),
        data.get("type"),
        data.get("thumb"),
    )
    user = m.sender_chat.title if m.sender_chat else m.from_user.mention
    emok = "5258077307985207053" if file == "Video" else "5258020476977946656"

    stream = await run_stream(file_name, type)
    try:
        await c.call_py.play(chat_id, stream)
        await send_song_info(
            m, thumbnail, type2, type, emok, songname, channel, durasi, url, user
        )
        play_task[chat_id] = c.loop.create_task(
            handle_song_duration(c, m, chat_id, file_name, duration, type, mode)
        )

    except Exception as e:
        await m.reply(f"Error Music {str(e)} di baris: {sys.exc_info()[-1].tb_lineno}")
        logger.error(f"Error Music {str(e)} di baris: {sys.exc_info()[-1].tb_lineno}")


async def handle_song_duration(c, m, chat_id, file_name, duration, type, mode):
    await asyncio.sleep(duration)
    queues[(chat_id, c.me.id)].pop(0)
    demus_data[(chat_id, c.me.id)].pop(0)
    cleanup_files(file_name)

    if queues.get((chat_id, c.me.id)):
        await play_next_song(c, m, type, mode)
    else:
        queues.pop((chat_id, c.me.id), None)
        demus_data.pop((chat_id, c.me.id), None)
        await c.call_py.leave_call(chat_id)


def get_chatid_mode(c, m):
    if m.command[0].startswith("c"):
        chat_id = (
            dB.get_var(c.me.id, "CHANNEL_PLAY")
            if dB.get_var(c.me.id, "CHANNEL_PLAY")
            else None
        )
        mode = "ch"
    else:
        chat_id = m.chat.id
        mode = "gc"
    return int(chat_id) if chat_id else None, mode


async def send_song_info(
    m, thumbnail, type2, type, emok, songname, channel, durasi, url, user
):
    try:
        await m.reply_photo(
            photo=thumbnail,
            caption=plere.format(
                type2, type, emok, songname, channel, durasi, url, channel, user
            ),
        )
    except:
        await m.reply(
            plere.format(
                type2, type, emok, songname, channel, durasi, url, channel, user
            ),
            disable_web_page_preview=True,
        )


@zb.ubot("play|vplay|cplay|cvplay")
async def play_command(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    replied = m.reply_to_message
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    huehue = await m.reply(_("proses").format(em.proses, proses_))
    type, file_name, duration, thumbnail, songname, link, channel = (
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )
    chat_id, mode = get_chatid_mode(c, m)
    is_channel = mode == "ch"
    if not chat_id:
        await huehue.edit(f"{em.gagal}**Channel not linked or invalid chat ID.**")
        return
    try:
        if replied:
            if replied.audio:
                songname = replied.audio.file_name or "Audio"
                durasi = timedelta(seconds=replied.audio.duration)
                file_path = await cek_file_ada(audio=replied.audio)
                media_type = "Audio"
                duration = replied.audio.duration
            elif replied.voice:
                songname = "Voice Message"
                durasi = timedelta(seconds=replied.voice.duration)
                file_path = await cek_file_ada(audio=replied.voice)
                media_type = "Audio"
                duration = replied.voice.duration
            elif replied.video:
                songname = replied.video.file_name or "Video"
                durasi = timedelta(seconds=replied.video.duration)
                file_path = await cek_file_ada(audio=replied.video)
                media_type = "Video"
                duration = replied.video.duration
            elif replied.document:
                songname = "Document"
                durasi = timedelta(seconds=replied.document.duration)
                file_path = await cek_file_ada(audio=replied.document)
                media_type = "Video"
                duration = replied.document.duration

            if await Telegram.download(c, m, huehue, file_path):
                file_name = file_path
            else:
                file_name = file_path

            thumbnail = (
                await c.download_media(
                    replied.audio.thumbs[-1].file_id
                    if replied.audio and replied.audio.thumbs
                    else (
                        replied.video.thumbs[-1].file_id
                        if replied.video and replied.video.thumbs
                        else None
                    )
                )
                if replied and (replied.audio or replied.video)
                else wget.download(log_pic)
            )
            channel = (
                await c.get_chat(
                    dB.get_var(c.me.id, "CHANNEL_PLAY") if is_channel else m.chat.id
                )
            ).title
            link = replied.link
        else:
            if len(m.command) < 2:
                await huehue.edit(
                    f"{em.gagal}**Please provide a query or reply to media!!**"
                )
                return

            query = " ".join(m.command[1:])
            url = get_judul(query)
            is_video = m.command[0].endswith("vplay")
            file_name, songname, link, duration, _, channel, thumbnail, _ = (
                await YoutubeDownload(url, as_video=is_video)
            )
            durasi = timedelta(seconds=duration)
            media_type = "Video" if is_video else "Audio"
        # demus_data.get((chat_id, c.me.id))
        music_data = {
            "judul": songname,
            "file": file_name,
            "mik": channel,
            "dur": durasi,
            "url": link,
            "thumb": thumbnail,
            "type": media_type,
        }
        queues.setdefault((chat_id, c.me.id), []).append((file_name, duration))
        if len(queues[(chat_id, c.me.id)]) == 1:
            demus_data[(chat_id, c.me.id)] = [music_data]
            await huehue.delete()
            await play_next_song(c, m, media_type, mode)
        else:
            queue_pos = len(queues[(chat_id, c.me.id)])
            demus_data[(chat_id, c.me.id)].append(music_data)
            await huehue.edit(
                f"{em.sukses}<b>Added to queue #{queue_pos}:</b> {songname} | {media_type}"
            )

    except Exception as error:
        await huehue.edit(f"{em.gagal}Error: {str(error)}")


@zb.ubot("skip|cskip")
async def _(c: nlx, m, _):
    global play_task
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    huehue = await m.reply(_("proses").format(em.proses, proses_))

    chat_id, mode = get_chatid_mode(c, m)
    data = demus_data.get((chat_id, c.me.id))
    if not data:
        await huehue.edit(f"{em.gagal}**No active streaming found to skip.**")
        return
    type = data[0]["type"]
    if not chat_id:
        await m.reply(f"{em.gagal}**Channel not linked or invalid chat ID.**")
        return

    if queues.get((chat_id, c.me.id)) and len(queues[(chat_id, c.me.id)]) > 1:
        queues[(chat_id, c.me.id)].pop(0)
        demus_data[(chat_id, c.me.id)].pop(0)
        if play_task.get(chat_id):
            play_task[chat_id].cancel()
        await huehue.edit(f"<b>{em.sukses}Music skipped, getting new playlist.</b>")
        await asyncio.sleep(1)
        await play_next_song(c, m, type, mode)
    else:
        await huehue.edit(f"<b>{em.gagal}No more songs in the queue to skip.</b>")


@zb.ubot("pause|cpause")
async def _(c: nlx, m, _):
    global play_task
    em = Emojik(c)
    em.initialize()

    chat_id, mode = get_chatid_mode(c, m)
    if not chat_id:
        await m.reply(f"{em.gagal}**Channel not linked or invalid chat ID.**")
        return

    try:
        if play_task.get(chat_id):
            play_task[chat_id].cancel()
        await c.call_py.pause_stream(chat_id)
        await m.reply_text(f"<b>{em.sukses}Music successfully paused.</b>")
    except Exception as e:
        await m.reply_text(f"**Error when pausing: `{str(e)}`**")


@zb.ubot("end|cend")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    chat_id, mode = get_chatid_mode(c, m)
    if not chat_id:
        await m.reply(f"{em.gagal}**Channel not linked or invalid chat ID.**")
        return

    try:
        await c.call_py.leave_call(chat_id)
        queues.pop((chat_id, c.me.id), None)
        demus_data.pop((chat_id, c.me.id), None)
        await m.reply_text(f"<b>{em.sukses}Music stopped and left the voice chat.</b>")
    except NotInCallError:
        await m.reply_text(f"<b>{em.gagal}No active streaming found to stop.</b>")


@zb.ubot("resume|cresume")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    chat_id, mode = get_chatid_mode(c, m)
    if not chat_id:
        await m.reply(f"{em.gagal}**Channel not linked or invalid chat ID.**")
        return
    try:
        await c.call_py.resume_stream(chat_id)
        await m.reply_text(f"<b>{em.sukses}Music resumed.</b>")
    except NotInCallError:
        await m.reply_text(f"<b>{em.gagal}No active streaming found.</b>")


@zb.ubot("playlist|cplaylist")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    huehue = await m.reply(_("proses").format(em.proses, proses_))
    chat_id, mode = get_chatid_mode(c, m)
    if not chat_id:
        await m.reply(f"{em.gagal}**Channel not linked or invalid chat ID.**")
        return
    if queues.get((chat_id, c.me.id)):
        data = demus_data.get((chat_id, c.me.id), [])
        song_list = f"<emoji id=5296385246579670377>📋</emoji> **Playlist Songs**:\n\n"
        panah = "<emoji id=5257991477358763590>▶</emoji>"
        for count, song in enumerate(data, start=1):
            song_list += f"**{count}. {panah} [{song['judul']}]({song['url']}) - `{song['dur']}` | {song['type']}**\n"
        await huehue.edit(song_list, disable_web_page_preview=True)
    else:
        await huehue.edit(f"{em.gagal}**No active streaming found!**")


@zb.ubot("channelplay")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    chat_id = m.command[1]
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
        dB.set_var(c.me.id, "CHANNEL_PLAY", chat_id)
        await m.reply_text(
            "<b>{} ChannelPlay Linked set to `{}`.</b>".format(em.sukses, chat_id)
        )
    except Exception as e:
        await m.reply_text(
            "<b>{} Error when set channelplay: {}.</b>".format(em.gagal, str(e))
        )
