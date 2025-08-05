import os
import shutil

import requests
import wget
from pyrogram.types import InputMediaPhoto

from config import botcax_api
from Userbot import nlx
from Userbot.helper.tools import Emojik, ReplyCheck, h_s, initial_ctext, zb

__MODULES__ = "Pinterest"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_pinter")


@zb.ubot("pinter|pinterest")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    value = c.get_text(m)
    if not value:
        return await m.reply(f"{em.gagal}<b>Silahkan berikan query untuk dicari!!</b>")
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    all_photo = []
    url = f"https://api.botcahx.eu.org/api/search/pinterest?text1={value}&apikey={botcax_api}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        images = data["result"][:7]
        folder_name = "img_pinterest"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        for img_url in images:
            img_filename = wget.download(img_url, out=folder_name)
            all_photo.append(
                InputMediaPhoto(
                    img_filename,
                    caption=f"{em.sukses}<b>Query: <u>{value}</u>\n{em.profil}Search by {c.me.mention}</b>",
                )
            )
        if all_photo:
            await m.reply_media_group(all_photo, reply_to_message_id=ReplyCheck(m))
            if os.path.exists(folder_name):
                shutil.rmtree(folder_name)
        else:
            await m.reply(f"{em.gagal}<b>Tidak ada gambar yang berhasil diunduh.</b>")
    else:
        await m.reply(_("err").format(em.gagal, res.text))
    return await pros.delete()
