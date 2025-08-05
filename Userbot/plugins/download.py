################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import os
import time
from datetime import timedelta
from time import time
from urllib.parse import urlparse

import aiohttp
import requests
import wget
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from youtubesearchpython import VideosSearch

from config import botcax_api
from Userbot import logger, nlx
from Userbot.helper.tools import (Emojik, YoutubeDownload, fetch, get, h_s,
                                  initial_ctext, zb, progress)

__MODULES__ = "Download"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_donlod")


def download_file(url, filename, stream: False = bool):
    response = requests.get(url, stream=stream)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        logger.info(f"Downloaded: {filename}")
    else:
        return f"Failed to download: {filename}"


async def download_tiktok_video(c, m, _, link, em, opsi):
    try:
        url = f"https://api.botcahx.eu.org/api/dowloader/tiktok?url={link}&apikey={botcax_api}"
        response = requests.get(url)
        data = response.json()
        if data["status"]:
            result = data["result"]
            title = result["title"]
            thumbnail_url = result["thumbnail"]
            download_file(thumbnail_url, "thumbnail.jpg")
            with open("title.txt", "w") as file:
                file.write(title)
            if opsi == "video":
                video_urls = result["video"]
                for i, video_url in enumerate(video_urls):
                    download_file(video_url, f"video_{i+1}.mp4", stream=True)
                    for i in range(len(video_urls)):
                        await c.send_video(
                            m.chat.id,
                            f"video_{i+1}.mp4",
                            thumb="thumbnail.jpg",
                            caption=title
                            + f"\n\n{em.sukses}**Successfully Download Tiktok Content by: {c.me.mention}**",
                        )
                    os.remove("thumbnail.jpg")
                    os.remove(f"video_{i+1}.mp4")
                    os.remove("title.txt")
                    return
            elif opsi == "audio":
                audio_urls = result["audio"]
                for i, audio_url in enumerate(audio_urls):
                    download_file(audio_url, f"audio_{i+1}.mp3", stream=False)
                    for i in range(len(audio_urls)):
                        await c.send_audio(
                            m.chat.id,
                            f"audio_{i+1}.mp3",
                            thumb="thumbnail.jpg",
                            caption=title
                            + f"\n\n{em.sukses}**Successfully Download Tiktok Content by: {c.me.mention}**",
                        )
                    os.remove("thumbnail.jpg")
                    os.remove(f"audio_{i+1}.mp3")
                    os.remove("title.txt")
                    return
            else:
                return await m.reply(
                    f"{em.gagal}Silakan gunakan format `{m.text.split()[0]}` video link-tiktok atau `{m.text.split()[0]}` audio link-tiktok."
                )
        else:
            return await m.reply(
                f"{em.gagal}**Failed to download TikTok video. Reason: {str(e)}**"
            )
    except Exception as e:

        return await m.reply(
            f"{em.gagal}**Failed to download TikTok video. Reason: {str(e)}**"
        )


@zb.ubot("dtik")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.command) < 3:
        return await m.reply(
            f"{em.gagal}Silakan gunakan format `{m.text.split()[0]}` video link-tiktok atau `{m.text.split()[0]}` audio link-tiktok."
        )
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    command, isi = m.command[:2]
    link = " ".join(m.command[2:])
    await download_tiktok_video(c, m, _, link, em, isi)
    return await pros.delete()


@zb.ubot("vtube")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(_("down_1").format(em.gagal, m.command))
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await m.reply_text(_("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await m.reply_text(_("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_video(
        m.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "VIDEO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            _("proses").format(em.proses, proses_),
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
    return


@zb.ubot("stube")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(_("down_1").format(em.gagal, m.command))
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.edit(_("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await pros.edit(_("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_audio(
        m.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "AUDIO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            _("proses").format(em.proses, proses_),
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
    return


def is_valid_twitter_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.endswith("x.com") and "/status/" in parsed_url.path


def download_media_from_twitter(tweet_url):
    endpoint = "https://twitter-x-media-download.p.rapidapi.com/media"
    payload = {"url": tweet_url, "proxy": ""}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "twitter-x-media-download.p.rapidapi.com",
    }

    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "tweetResult" in data:
            return data["tweetResult"]
        else:
            return None
    else:
        return None


@zb.ubot("twit|twitt")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    if len(m.command) < 2:
        await pros.edit(f"{em.gagal}<b>Silakan berikan tautan Twitter.</b>")
        return

    tweet_url = m.command[1]
    if not is_valid_twitter_url(tweet_url):
        await pros.edit(
            f"{em.gagal}<b>Tautan yang diberikan bukan tautan Twitter yang valid.</b>"
        )
        return
    media_info = download_media_from_twitter(tweet_url)

    if media_info:
        media_type = (
            media_info.get("result", {})
            .get("legacy", {})
            .get("entities", {})
            .get("media", [{}])[0]
            .get("type")
        )
        if media_type == "photo":
            media_url = (
                media_info.get("result", {})
                .get("legacy", {})
                .get("entities", {})
                .get("media", [{}])[0]
                .get("media_url_https")
            )
            if media_url:
                caption = (
                    f"{em.sukses}<b>Successfully Download Photo by : {c.me.mention}</b>"
                )
                await c.send_photo(chat_id=m.chat.id, photo=media_url, caption=caption)
                return await pros.delete()
        elif media_type == "video":
            video_info = (
                media_info.get("result", {})
                .get("legacy", {})
                .get("entities", {})
                .get("media", [{}])[0]
                .get("video_info", {})
            )
            if video_info:
                variants = video_info.get("variants", [])
                video_url = None
                for variant in variants:
                    content_type = variant.get("content_type", "")
                    if "video/mp4" in content_type:
                        video_url = variant.get("url", "")
                        break
                if video_url:
                    caption = f"{em.sukses}<b>Successfully Download Video by : {c.me.mention}</b>"
                    await c.send_video(
                        chat_id=m.chat.id, video=video_url, caption=caption
                    )
                    return await pros.delete()

            else:
                return await pros.edit(
                    f"{em.gagal}<b>Gagal mendapatkan URL video dari tautan Twitter.</b>"
                )

    else:
        return await pros.edit(
            f"{em.gagal}<b>Gagal mendapatkan informasi media dari Twitter.</b>"
        )


@zb.ubot("insta")
async def insta_handler(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    rep = m.reply_to_message or m

    try:
        url = m.text.split(None, 1)[1]
        api_url = f"https://api.botcahx.eu.org/api/dowloader/allin?url={url}&apikey={botcax_api}"
        response = await get(api_url)

        if response["code"] == 200:
            media_group = []
            file_paths = []

            async with aiohttp.ClientSession() as session:
                for num, media in enumerate(response["result"]["medias"], 1):
                    media_url = media["url"]
                    media_type = media["extension"]
                    if not media_url or not media_type:
                        continue

                    file_name = f"{num}.{media_type}"
                    async with session.get(media_url) as resp:
                        if resp.status == 200:
                            with open(file_name, "wb") as f:
                                f.write(await resp.read())
                            file_paths.append(file_name)
                            if media_type == "mp4":
                                media_group.append(
                                    InputMediaVideo(
                                        file_name,
                                        caption=f"{em.sukses}<b>Downloaded by: {c.me.mention}</b>",
                                    )
                                )
                            elif media_type in ["jpg", "jpeg"]:
                                media_group.append(
                                    InputMediaPhoto(
                                        file_name,
                                        caption=f"{em.sukses}<b>Downloaded by: {c.me.mention}</b>",
                                    )
                                )
                            else:
                                await pros.edit(
                                    f"{em.gagal}<b>Tipe media {media_type} tidak didukung.</b>"
                                )
                                return
                        else:
                            await pros.edit(
                                f"{em.gagal}<b>Gagal mengunduh {file_name} dari tautan yang diberikan.</b>"
                            )
                            return

            if media_group:
                await c.send_media_group(
                    m.chat.id,
                    media=media_group,
                    reply_to_message_id=rep.id,
                )

                for file_path in file_paths:
                    if os.path.exists(file_path):
                        os.remove(file_path)

                return await pros.delete()
            else:
                return await pros.edit(
                    f"{em.gagal}<b>Tidak ada media yang valid ditemukan.</b>"
                )
        else:
            return await pros.edit(
                f"{em.gagal}<b>Gagal mengunduh media dari tautan yang diberikan.</b>"
            )

    except Exception as er:
        return await pros.edit(f"{em.gagal}<b>Error</b>: {str(er)}")


@zb.ubot("ytdl")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    url = c.get_arg(m)
    if not url:
        return await m.reply(_("down_1").format(em.gagal, m.text.split()[0]))
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(url, as_video=True)
    except Exception as error:
        return await m.reply_text(_("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_video(
        m.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "Video",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        reply_to_message_id=m.id,
    )
    # file, title = await YtShort(url)
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)
    return


@zb.ubot("ccdl")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    text = c.get_arg(m)
    if len(m.command) < 2:
        return await m.reply(
            f"{em.gagal}Silakan gunakan format `{m.text.split()[0]}` link-capcut."
        )
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        url = f"https://api.botcahx.eu.org/api/dowloader/capcut?url={text}&apikey={botcax_api}"
        res = await fetch.get(url)
        if res.status_code == 200:
            data = res.json()["result"]
            titel = data["title"]
            desc = data["description"]
            url = data["video_ori"]
            dius = data["digunakan"]
            akun = data["author_profile"]
            video = f"cc_{c.me.id}.mp4"
            await c.bash(f"curl -L {url} -o {video}")
            await pros.delete()
            cap = """<blockquote><b>{} Berhasil mengunduh video!!
📌 Judul: {}
🪧 Deskripsi: {}
📈 Digunakan: {}
🔗 Tautan: <a href='{}'>Klik Disini</a>
👤 Creator: <a href='{}'>Klik Disini</a></b></blockquote>
""".format(
                em.sukses, titel, desc, dius, url, akun
            )
            await m.reply_video(video, caption=cap)
            if os.path.exists(video):
                os.remove(video)
            return
        else:
            return await pros.edit(_("err").format(em.gagal, res.text))
    except Exception as e:
        return await pros.edit(_("err").format(em.gagal, str(e)))
