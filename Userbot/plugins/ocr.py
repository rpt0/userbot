import os
from io import BytesIO

import requests

from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

from .graph import upload_media

__MODULES__ = "Ocr"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_ocr")


async def dl_pic(client, download):
    path = await client.download_media(download)
    with open(path, "rb") as f:
        content = f.read()
    os.remove(path)
    get_photo = BytesIO(content)
    return get_photo


@zb.ubot("ocr|read")
async def read_cmd(client, message, _):
    em = Emojik(client)
    em.initialize()
    reply = message.reply_to_message
    if not reply or not reply.photo and not reply.sticker and not reply.animation:
        return await message.reply_text(
            f"{em.gagal}{message.text.split()[0]} balas media"
        )
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    msg = await message.reply(_("proses").format(em.proses, proses_))
    try:
        # file_path = await dl_pic(client, reply)
        url = await upload_media(message)
        req = requests.get(
            f"https://script.google.com/macros/s/AKfycbwURISN0wjazeJTMHTPAtxkrZTWTpsWIef5kxqVGoXqnrzdLdIQIfLO7jsR5OQ5GO16/exec?url={url}"
        ).json()
        return await msg.edit(f"{em.sukses}<code>{req['text']}</code>")
    except Exception as e:
        return await msg.edit(_("err").format(em.gagal, str(e)))
