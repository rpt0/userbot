from Userbot import nlx
from Userbot.helper.tools import Emojik, zb


@zb.nocmd("REP_BLOCK", nlx)
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    return await message.reply_text(
        f"{em.block}**You've blocked me, don't reply or tag me fuvk it!!**"
    )
