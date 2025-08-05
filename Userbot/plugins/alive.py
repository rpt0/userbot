################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from config import bot_username
from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import Emojik, zb

from .graph import upload_media


@zb.ubot("alive")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    query = c.get_arg(m)
    if not query:
        try:
            x = await c.get_inline_bot_results(bot_username, "alive")
            await m.reply_inline_bot_result(x.query_id, x.results[0].id)
        except Exception as error:
            await m.reply(error)
        return
    else:
        m.reply_to_message
        if query == "pic":
            value = await upload_media(m)
            dB.set_var(c.me.id, "ALIVE_PIC", value)
            return await m.reply(f"{em.sukses}Done set alive pic")
        elif query == "reset":
            dB.remove_var(c.me.id, "ALIVE_PIC")
            return await m.reply(f"{em.sukses}Done remove alive pic")
        else:
            return
