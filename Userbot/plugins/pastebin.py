################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 @ CREDIT : NAN-DEV
"""
################################################################

import os
import re

import aiofiles

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, zb, paste

__MODULES__ = "Pastebin"


def help_string(org):
    return h_s(org, "help_paste")


from .webshot import ss

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


@zb.ubot("paste")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if not m.reply_to_message:
        return await m.reply_text(_("paste_1").format(em.gagal, m.text.split()[0]))
    r = m.reply_to_message
    if not r.text and not r.document:
        return await m.reply_text(_("paste_1").format(em.gagal))
    if r.text:
        content = str(r.text)
    else:
        if r.document.file_size > 40000:
            return await m.reply(_("paste_2").format(em.gagal))
        doc = await m.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = await paste(content)
    photo = await ss(link, True)
    try:
        await m.reply_document(photo, caption=_("paste_3").format(em.sukses, link))
        return
    except Exception:
        await m.reply(_("paste_3").format(em.sukses, link))
        return
