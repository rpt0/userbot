import asyncio
import os
import re
import subprocess

import assemblyai as aai
from pyrogram import enums
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import InputMediaPhoto

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

from .ocr import dl_pic

__MODULES__ = "Convert"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_convert")


aai.settings.api_key = "e28239cb6ecc4d0090f36711b11e247a"


user_last_command_time = {}


@zb.ubot("toanime")
async def convert_anime(client, message, _):
    emo = Emojik(client)
    emo.initialize()
    client.me.id
    botol = "@PicToAnimeRobot"
    pros = await message.reply(f"{emo.proses}<b>Proses mengunduh gambar ..</b>")

    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                file = "foto"
                get_photo = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
                file = "sticker"
                get_photo = await dl_pic(client, message.reply_to_message)
            elif message.reply_to_message.animation:
                file = "gift"
                get_photo = await dl_pic(client, message.reply_to_message)
            else:
                return await pros.edit(
                    f"{emo.gagal}<b>Silakan balas ke foto/sticker/gift</b>"
                )
        else:
            if message.command[1] in ["foto", "profil", "photo"]:
                chat = (
                    message.reply_to_message.from_user
                    or message.reply_to_message.sender_chat
                )
                file = "foto profil"
                get = await client.get_chat(chat.id)
                photo = get.photo.big_file_id
                get_photo = await dl_pic(client, photo)
    else:

        try:
            file = "foto"
            get = await client.get_chat(message.command[1])
            photo = get.photo.big_file_id
            get_photo = await dl_pic(client, photo)
        except Exception as error:
            return await pros.edit(f"{emo.gagal}<b>Error:</b>\n<code>{error}</code>")

    await pros.edit(f"{emo.proses}<b>Sedang memproses <code>{file}</code> ..</b>")
    await client.unblock_user(botol)
    send_photo = await client.send_photo(botol, get_photo)
    await asyncio.sleep(2)
    await pros.edit(f"{emo.proses}<b>Proses convert <code>{file}</code></b>")
    await asyncio.sleep(30)
    await send_photo.delete()
    await pros.delete()
    info = await client.resolve_peer(botol)
    anime_photo = []
    async for anime in client.search_messages(
        botol, filter=enums.MessagesFilter.PHOTO, limit=3
    ):
        if anime.photo:
            pic = anime.photo.file_id
            anime_photo.append(InputMediaPhoto(media=pic))
    if anime_photo:
        await client.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))

    else:
        await client.send_message(
            message.chat.id,
            f"{emo.gagal}<b>Gagal merubah gambar {file}.</b>",
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))


@zb.ubot("toimg")
async def _(c: nlx, message, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    try:
        pros = await message.reply(_("proses").format(em.proses, proses_))
        file_io = await dl_pic(c, message.reply_to_message)
        file_io.name = "sticker.png"
        await c.send_photo(
            message.chat.id,
            file_io,
            caption=_("konpert_5").format(em.sukses, c.me.mention),
            reply_to_message_id=message.id,
        )
        return await pros.delete()
    except Exception as e:
        await pros.delete()
        return await c.send_message(
            message.chat.id,
            _("err").format(em.gagal, e),
            reply_to_message_id=message.id,
        )


@zb.ubot("tosticker|tostick")
async def _(c: nlx, message, _):
    em = Emojik(c)
    em.initialize()
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.reply_text(_("konpert_1").format(em.gagal))
        sticker = await c.download_media(
            message.reply_to_message.photo.file_id,
            f"sticker_{message.from_user.id}.webp",
        )
        await message.reply_sticker(sticker)
        os.remove(sticker)
        return
    except Exception as e:
        return await message.reply(_("err").format(em.gagal, e))


@zb.ubot("togif")
async def _(c: nlx, message, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await message.reply(_("proses").format(em.proses, proses_))
    if not message.reply_to_message.sticker:
        return await pros.edit(_("konpert_6").format(em.gagal))
    await pros.edit(_("konpert_2").format(em.proses))
    file = await c.download_media(
        message.reply_to_message,
        f"gift_{message.from_user.id}.mp4",
    )
    try:
        await c.send_animation(message.chat.id, file, reply_to_message_id=message.id)
        os.remove(file)
        return await pros.delete()

    except Exception as error:
        return await pros.edit(_("err").format(em.gagal, str(error)))


@zb.ubot("toaudio")
async def _(c: nlx, message, _):
    em = Emojik(c)
    em.initialize()
    file = None
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    replied = message.reply_to_message
    pros = await message.reply(_("proses").format(em.proses, proses_))
    if not replied:
        return await pros.edit(_("konpert_7").format(em.gagal))
    if replied.video:
        await pros.edit(_("konpert_2").format(em.proses))
        file = await c.download_media(
            message=replied,
            file_name=f"toaudio_{replied.id}",
        )
        out_file = f"{file}.mp3"
        try:
            await pros.edit(_("konpert_8").format(em.proses))
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await c.run_cmd(cmd)
            await pros.edit(_("konpert_9").format(em.proses))
            await c.send_voice(
                message.chat.id,
                voice=out_file,
                caption=_("konpert_5").format(em.sukses, c.me.mention),
                reply_to_message_id=message.id,
            )
            os.remove(file)
            os.remove(out_file)
            return await pros.delete()
        except Exception as error:
            os.remove(file)
            os.remove(out_file)
            return await pros.edit(str(error))
    else:
        if os.path.exists(file):
            os.remove(file)
        if os.path.exists(out_file):
            os.remove(out_file)
        return await pros.edit(_("konpert_7").format(em.gagal))


@zb.ubot("efek|effect|voifek")
async def _(client: nlx, message, _):
    emo = Emojik(client)
    emo.initialize()
    pros = await message.reply(f"{emo.proses}<b>Proses convert efek ...</b>")
    helo = client.get_arg(message).lower()

    rep = message.reply_to_message
    if rep and helo:
        tau = [
            "chipmunk",
            "robot",
            "jedug",
            "ancur",
            "cepat",
            "echo",
            "reverb",
            "tinggi",
            "distorsi",
            "chorus",
            "flanger",
            "bass",
            "8d",
            "treble",
        ]
        if any(effect in helo for effect in tau):
            await pros.edit(
                f"{emo.proses}<b>Proses merubah suara menjadi : <code>{helo}</code></b>"
            )
            indir = await client.download_media(rep)
            KOMUT = {
                "chipmunk": '-filter_complex "rubberband=pitch=1.5"',
                "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
                "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
                "ancur": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
                "cepat": '-filter_complex "atempo=2.0"',
                "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
                "reverb": '-filter_complex "aecho=0.8:0.88:60:0.4"',
                "tinggi": '-filter_complex "asetrate=44100*1.25,aresample=44100,atempo=1.25"',
                "distorsi": '-filter_complex "acrusher=bits=8:mode=log"',
                "chorus": '-filter_complex "chorus=0.5:0.9:50:0.4:0.25:2"',
                "flanger": '-filter_complex "flanger"',
                "bass": '-filter_complex "lowpass=f=3000"',
                "treble": '-filter_complex "highpass=f=200"',
                "8d": '-filter_complex "pan=stereo|FL<0.5*c0+0.5*c1|FR<0.5*c0+0.5*c1, aecho=0.8:0.9:1000:0.5"',
            }

            result = subprocess.run(
                f"ffmpeg -i '{indir}' {KOMUT.get(helo, '')} audio.mp3",
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if result.returncode == 0:
                await rep.reply_voice(
                    "audio.mp3",
                    caption=f"{emo.sukses}<b>Berhasil mengubah efek audio menjadi: <code>{helo}</code>\nDiubah oleh: {client.me.mention}</b>",
                )
                os.remove("audio.mp3")
                return await pros.delete()
            else:
                os.remove(indir)
                return await pros.edit(
                    f"{emo.gagal}<b>Gagal mengkonversi audio: <code>{result.stderr.decode()}</code>"
                )
        else:
            return await pros.edit(
                f"{emo.gagal}<b>Silakan masukkan efek yang valid: <code>{', '.join(tau)}</code></b>"
            )
    else:
        return await pros.edit(
            f"{emo.gagal}<b>Silakan balas audio.\n\nContoh: <code>{message.text.split()[0]}efek chipmunk</code> [balas audio]</b>"
        )


async def stt_cmd(c, m, _, upload_url, pros):
    em = Emojik(c)
    em.initialize()
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(upload_url)
    if transcript.text:
        await pros.edit(
            _("konpert_21").format(em.sukses, c.me.mention, transcript.text)
        )
        os.remove(upload_url)
        return
    else:
        await pros.edit(_("konpert_22").format(em.gagal))
        os.remove(upload_url)
        return


@zb.ubot("stt")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))

    if m.reply_to_message and (m.reply_to_message.audio or m.reply_to_message.voice):
        if m.reply_to_message.audio:
            upload_url = await c.download_media(
                m.reply_to_message.audio.file_id, file_name="stt.mp3"
            )
        elif m.reply_to_message.voice:
            upload_url = await c.download_media(
                m.reply_to_message.voice.file_id, file_name="stt.ogg"
            )
        await stt_cmd(c, m, _, upload_url, pros)
    elif m.command and len(m.command) > 1:
        url = m.command[1]
        if re.match(r"^https?://.*\.(mp3|ogg)$", url):
            return await stt_cmd(c, m, _, url, pros)
        else:
            return await pros.edit(
                f"{em.gagal}URL yang diberikan bukan URL audio yang valid."
            )
    else:
        return await pros.edit(
            f"{em.gagal}Mohon balas pesan dengan audio atau berikan URL audio yang valid untuk mentranskripsinya."
        )
