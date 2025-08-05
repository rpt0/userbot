# LUCIFER

from config import bot_username
from Userbot import dB, nlx
from Userbot.helper.tools import Emojik, ReplyCheck, h_s, zb

__MODULES__ = "Calculator"


def help_string(org):
    return h_s(org, "help_calc")


@zb.ubot("calc|kalkulator")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    try:
        xi = await c.get_inline_bot_results(bot_username, f"calculator")
        dB.set_var(c.me.id, "kalku_inline", id(m))
        mmg = await m.reply_inline_bot_result(
            xi.query_id, xi.results[0].id, reply_to_message_id=ReplyCheck(m)
        )
        data = {"_id": c.me.id, "chat_id": m.chat.id, "message_id": mmg.updates[0].id}
        dB.set_var(c.me.id, "KALKU", data)
        dB.set_var(c.me.id, "CB_CALCU", c.me.id)
        return
    except Exception as e:
        return await m.edit(f"{em.gagal}**ERROR**: {str(e)}")
