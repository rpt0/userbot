import os
import random

import requests
import wget
from pyrogram.enums import MessagesFilter
from pyrogram.types import InputMediaPhoto

from config import botcax_api, the_cegers
from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb, post

__MODULES__ = "Asupan"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_supan")


async def download_asupan_nya(c, m, _, em, value):
    if value == "hijaber":
        url = (
            f"https://api.botcahx.eu.org/api/asupan/hijaber?apikey={botcax_api}"  # jpg
        )
    elif value == "santuy":
        url = f"https://api.botcahx.eu.org/api/asupan/santuy?apikey={botcax_api}"  # mp4
    elif value == "ukhty":
        url = f"https://api.botcahx.eu.org/api/asupan/ukhty?apikey={botcax_api}"  # mp4
    elif value == "cecan":
        url = f"https://api.botcahx.eu.org/api/asupan/cecan?apikey={botcax_api}"  # jpg
    else:
        url = f"https://api.botcahx.eu.org/api/asupan/tiktok?query={value}&apikey={botcax_api}"  # mp4

    if value in ["hijaber", "cecan"]:
        response = requests.get(url)
        if response.status_code == 200:
            with open("ce.jpg", "wb") as file:
                file.write(response.content)
            await m.reply_photo(
                "ce.jpg",
                caption=f"{em.sukses}<blockquote><b>Search by {c.me.mention}</blockquote></b>",
            )
            os.remove("ce.jpg")
            return
        else:
            return f"Permintaan gagal. Status code: {response.status_code}"
    elif value in ["ukhty", "santuy"]:
        response = requests.get(url)
        if response.status_code == 200:
            with open("ce.mp4", "wb") as file:
                file.write(response.content)
            await m.reply_video(
                "ce.mp4",
                caption=f"{em.sukses}<blockquote><b>Search by {c.me.mention}</blockquote></b>",
            )
            os.remove("ce.mp4")
            return
        else:
            return f"Permintaan gagal. Status code: {response.status_code}"
    else:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if (
                "status" in data
                and data["status"]
                and "code" in data
                and data["code"] == 200
            ):
                if "result" in data and "data" in data["result"]:
                    videos = data["result"]["data"]
                    if not videos:
                        await m.reply(
                            f"{em.gagal}<b>Tidak ada video yang ditemukan!! Coba gunakan nama akun tiktok lain.</b>"
                        )
                        return

                    video_info = random.choice(videos)
                    video_url = video_info["play"]
                    video_title = video_info["title"]
                    video_link = video_info["play"]

                    video_response = requests.get(video_url)
                    if video_response.status_code == 200:
                        video_filename = f"{video_title}.mp4"
                        with open(video_filename, "wb") as video_file:
                            video_file.write(video_response.content)

                        caption = f"Judul: {video_title}\nLink: {video_link}"
                        await m.reply_video(
                            video_filename,
                            caption=caption
                            + f"{em.sukses}<blockquote><b>Search by {c.me.mention}</blockquote></b>",
                        )
                        os.remove(video_filename)
                        return
                    else:
                        return f"Gagal mendownload video. Status code: {video_response.status_code}"
                else:
                    return "Key 'result' atau 'data' tidak ditemukan dalam respons API."
            else:
                return "Tidak ada data video yang ditemukan atau status code salah."
        else:
            return f"Permintaan ke API gagal. Status code: {response.status_code}"


async def download_and_send_images(c, m, value):
    media_group = []
    payload = {"prompt": f"{value}"}
    url = "https://mirai-api.netlify.app/api/image-generator/bing-ai"
    res = await post(url, json=payload)
    try:
        data = res["url"]
        for num, i in enumerate(data, 1):
            pot = f"{num}.jpg"
            await c.bash(f"wget {i} -O {pot}")
            media_group.append(InputMediaPhoto(pot))
        await m.reply_media_group(media_group)
        for media in media_group:
            try:
                os.remove(media.media)
            except Exception as e:
                return f"Error deleting file {media.media}: {e}"
    except KeyError:
        return await m.reply(f"**Please try again!!**")


@zb.ubot("bing-img")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.command) < 2 and not m.reply_to_message:
        return await m.reply(
            f"{em.gagal}Silahkan gunakan contoh format: `{m.text.split()[0]} wanita cantik gaun putih`."
        )
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    value = nlx.get_text(m)
    await download_and_send_images(c, m, value)
    return await pros.delete()


@zb.ubot("asupan")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(
            f"{em.gagal}Silahkan gunakan contoh format: `{m.text.split()[0]} ukhty`."
        )
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    value = m.text.split()[1]
    await download_asupan_nya(c, m, _, em, value)
    return await pros.delete()


@zb.ubot("ppcp")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    all_foto = []
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    url = f"https://api.botcahx.eu.org/api/randomgambar/couplepp?apikey={botcax_api}"
    data = requests.get(url)
    if data.status_code == 200:
        file = data.json()
        a = file["result"]["male"]
        b = file["result"]["female"]
        foto_male = wget.download(a)
        foto_female = wget.download(b)
        all_foto.append(InputMediaPhoto(foto_male))
        all_foto.append(InputMediaPhoto(foto_female))
        await m.reply_media_group(all_foto)
        os.remove(foto_male)
        os.remove(foto_female)
        return await pros.delete()
    else:
        return await pros.edit("{}Maaf server sedang down".format(em.gagal))


@zb.ubot("meme")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    url = f"https://api.botcahx.eu.org/api/random/meme?apikey={botcax_api}"
    data = requests.get(url)
    if data.status_code == 200:
        with open("mm.jpg", "wb") as file:
            file.write(data.content)
        await m.reply_photo("mm.jpg")
        os.remove("mm.jpg")
        return await pros.delete()
    else:
        return await pros.edit("{}Maaf server sedang down".format(em.gagal))


@zb.ubot("bokep")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    pros = await message.reply(_("proses").format(em.proses, proses_))
    rep = message.reply_to_message or message
    try:
        await client.join_chat("https://t.me/+-mGIUzA6HvhmZGQx")
    except Exception:
        pass
        # return await message.reply(f"{em.gagal}**Server sedang down!!**")
    try:
        bokepnya = []
        async for bokep in client.search_messages(
            -1002482574579, filter=MessagesFilter.VIDEO
        ):
            bokepnya.append(bokep)
        video = random.choice(bokepnya)
        await video.copy(
            message.chat.id,
            caption=f"{em.sukses}<b>Bokep By <a href=tg://user?id={client.me.id}>{client.me.first_name} {client.me.last_name or ''}</a></b>",
            reply_to_message_id=rep.id,
        )
        return await pros.delete()
    except Exception as er:
        return await pros.edit(f"{em.gagal}<b>Error!!</b> `{str(er)}`")
    if client.me.id not in the_cegers:
        return await client.leave_chat(-1002482574579)
