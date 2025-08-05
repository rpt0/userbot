################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Misskaty
  • JANGAN DIHAPUS YA MONYET-MONYET SIALAN
 
 MIKIR GOBLOK, TOLOL, IDIOT, NGENTOT, KONTOL, BAJINGAN
"""
################################################################

import base64
import io
import json
import os
import random
from io import BytesIO

from config import DEVS
from Userbot import nlx
from Userbot.helper.tools import (Emojik, h_s, initial_ctext, zb, loanjing,
                                  quotly)

__MODULES__ = "Quotly"


def help_string(org):
    return h_s(org, "help_quot")


async def consu(dok):
    try:
        with open(dok, "rb") as file:
            data_bytes = file.read()
        json_data = json.loads(data_bytes)
        image_data_base64 = json_data.get("image")
        if not image_data_base64:
            raise ValueError("Tidak ada data gambar dalam JSON")
        image_data = base64.b64decode(image_data_base64)
        image_io = io.BytesIO(image_data)
        image_io.name = "quotly.webp"
        return image_io
    except Exception as e:
        raise e


@zb.ubot("qcolor")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    iymek = f"\n•".join(loanjing)
    jadi = _("qot_1").format(em.proses)
    if len(iymek) > 4096:
        with open("qcolor.txt", "w") as file:
            file.write(iymek)
        await m.reply_document("qcolor.txt", caption=_("qot_2").format(em.sukses))
        os.remove("qcolor.txt")
        return
    else:
        return await m.reply(jadi + iymek)


@zb.ubot("q|qr")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    acak = None
    messages = None
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    if not m.reply_to_message:
        return await pros.edit("{}Please reply to message!!".format(em.gagal))
    is_reply = bool(m.command[0].endswith("r"))
    rep = m.reply_to_message
    if len(m.command) > 1:
        tag = m.command[1].strip()
        if tag.startswith("@"):
            user_id = tag[1:]
            try:
                org = await c.get_users(user_id)
                if org.id in DEVS:
                    await pros.edit(_("qot_3").format(em.gagal))
                    return
                rep = await c.get_messages(m.chat.id, m.reply_to_message.id, replies=0)
                rep.from_user = org
                messages = [rep]
            except Exception as e:
                return await pros.edit(_("err").format(em.gagal, e))
            warna = m.text.split(None, 2)[2] if len(m.command) > 2 else None
            if warna:
                acak = warna
            else:
                acak = random.choice(loanjing)
            hasil = await quotly(messages, acak, is_reply=is_reply)
            bio_sticker = BytesIO(hasil)
            bio_sticker.name = "biosticker.webp"
            await m.reply_sticker(bio_sticker)
            return await pros.delete()
        elif not tag.startswith("@"):
            warna = m.text.split(None, 1)[1] if len(m.command) > 1 else None
            if warna:
                acak = warna
            else:
                acak = random.choice(loanjing)
            m_one = await c.get_messages(
                chat_id=m.chat.id, message_ids=m.reply_to_message.id, replies=0
            )
            messages = [m_one]
            hasil = await quotly(messages, acak, is_reply=is_reply)
            bio_sticker = BytesIO(hasil)
            bio_sticker.name = "biosticker.webp"
            await m.reply_sticker(bio_sticker)
            return await pros.delete()
        elif int(tag):
            if int(tag) > 10:
                return await pros.edit(_("qot_4").format(em.gagal))
            warna = m.text.split(None, 2)[2] if len(m.command) > 2 else None
            if warna:
                acak = warna
            else:
                acak = random.choice(loanjing)
            messages = [
                i
                for i in await c.get_messages(
                    chat_id=m.chat.id,
                    message_ids=range(
                        m.reply_to_message.id,
                        m.reply_to_message.id + int(tag),
                    ),
                    replies=0,
                )
                if not i.empty and not i.media
            ]
            hasil = await quotly(messages, acak, is_reply=is_reply)
            bio_sticker = BytesIO(hasil)
            bio_sticker.name = "biosticker.webp"
            await m.reply_sticker(bio_sticker)
            return await pros.delete()
    else:
        acak = random.choice(loanjing)
        m_one = await c.get_messages(
            chat_id=m.chat.id, message_ids=m.reply_to_message.id, replies=0
        )
        messages = [m_one]
    try:
        hasil = await quotly(messages, acak, is_reply=is_reply)
        bio_sticker = BytesIO(hasil)
        bio_sticker.name = "biosticker.webp"
        # with open("hasil.json", "w") as file:
        # file.write(hasil.decode())
        # stik = await consu("hasil.json")
        await m.reply_sticker(bio_sticker)
        await pros.delete()
        return
    except Exception as e:
        return await pros.edit(_("err").format(em.gagal, e))
