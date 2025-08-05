################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


import os

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, zb

__MODULES__ = "Curi"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_spy")


@zb.ubot("curi|spy")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    dia = m.reply_to_message
    if not dia:
        return
    gclog = c.get_logger(c.me.id)
    logs = gclog if gclog else "me"
    anjing = dia.caption or ""
    await m.delete()

    if dia.photo or dia.video or dia.audio or dia.voice or dia.document:
        anu = await c.download_media(dia)

        if os.path.getsize(anu) == 0:
            os.remove(anu)
            return await c.send_message(logs, _("spy_1").format(em.gagal))
        try:
            if dia.photo:
                return await c.send_photo(logs, anu, anjing)
            elif dia.video:
                return await c.send_video(logs, anu, anjing)

            elif dia.audio:
                return await c.send_audio(logs, anu, anjing)

            elif dia.voice:

                return await c.send_voice(logs, anu, anjing)

            elif dia.document:

                return await c.send_document(logs, anu, anjing)
        except Exception as e:

            return await c.send_message(logs, _("err").format(em.gagal, e))
    else:

        return await c.send_message(logs, _("spy_2").format(em.sukses))
