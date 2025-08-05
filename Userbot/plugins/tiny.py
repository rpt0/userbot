# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/Otan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/Otan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import os

import cv2
from PIL import Image

from Userbot import nlx
from Userbot.helper.tools import (Emojik, ReplyCheck, dl_font, h_s,
                                  initial_ctext, zb)

__MODULES__ = "Tiny"


def help_string(org):
    return h_s(org, "help_tiny")


@zb.ubot("tiny")
async def memify(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    await dl_font()
    rep = m.reply_to_message
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    if not rep:
        return await pros.edit(_("st_7").format(em.gagal))
    doc = await c.download_media(rep)
    im1 = Image.open("font-module/bahan2.png")
    if doc.endswith(".tgs"):
        await c.download_media(rep, "man.tgs")
        await c.bash("lottie_convert.py man.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        jsn = jsn.replace("512", "2000")
        ("json.json", "w").write(jsn)
        await c.bash("lottie_convert.py json.json man.tgs")
        file = "man.tgs"
        os.remove("json.json")
    elif doc.endswith((".gif", ".mp4")):
        idoc = cv2.VideoCapture(doc)
        busy = idoc.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(doc)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await asyncio.gather(
        pros.delete(),
        c.send_sticker(
            m.chat.id,
            sticker=file,
            reply_to_message_id=ReplyCheck(m),
        ),
    )
    os.remove(file)
    os.remove(doc)
    return
