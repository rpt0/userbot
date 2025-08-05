from asyncio import sleep

from pyrogram.errors import FloodWait
from pyrogram.raw.functions.messages import DeleteHistory

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Limited"


def help_string(org):
    return h_s(org, "help_limit")


@zb.ubot("limit")
@zb.deve("limit")
async def _(c: nlx, m, _):
    await spam_bot(c, m, _)


async def spam_bot(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    await c.unblock_user("SpamBot")
    xin = await c.resolve_peer("SpamBot")
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    msg = await m.reply(_("proses").format(em.proses, proses_))
    await c.send_message("SpamBot", "/start")
    await sleep(1)
    await msg.delete()
    async for status in c.search_messages("SpamBot", limit=1):
        isdone = status.text
        break
    else:
        isdone = None
    if isdone:
        result = status.text
        emoji = None
        if "Good news" in result or "Kabar baik" in result:
            emoji = f"{em.sukses}"
        if "We afraid" in result or "Kami khawatir" in result:
            emoji = f"{em.warn}"
        await c.send_message(
            m.chat.id, _("lmt_1").format(emoji, result, em.owner, c.me.first_name)
        )
        try:
            await c.invoke(DeleteHistory(peer=xin, max_id=0, revoke=True))
        except FloodWait as e:
            await sleep(e.value)
        await msg.delete()
        return
