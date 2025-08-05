################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Gojo_Satoru
"""
################################################################


from config import bot_username
from Userbot import nlx
from Userbot.helper.tools import ReplyCheck, h_s, zb

__MODULES__ = "Markdown"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_mark")
    # return (org, "Markdown")


@zb.ubot("markdown")
async def _(c: nlx, m, _):
    try:
        xi = await c.get_inline_bot_results(bot_username, "mark_in")
        await m.delete()
        return await c.send_inline_bot_result(
            m.chat.id, xi.query_id, xi.results[0].id, reply_to_message_id=ReplyCheck(m)
        )

    except Exception as e:
        return await m.edit(f"{e}")
