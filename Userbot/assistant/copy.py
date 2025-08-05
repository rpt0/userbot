################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

from Userbot import bot, nlx
from Userbot.helper.tools import zb
from Userbot.plugins.copy_con import gas_download


@zb.bots("copy")
async def _(c: bot, m, _):
    if m.from_user.id not in nlx._my_id:
        return
    xx = await m.reply("Tunggu Sebentar...")
    link = c.get_arg(m)
    if not link:
        return await xx.edit(f"<b><code>{m.text}</code> [link]</b>")
    # if "?single" in link:
    # link = link.replace("?single", "")
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1])
        if "t.me/c/" in link:
            chat = int("-100" + str(link.split("/")[-2]))
        else:
            chat = str(link.split("/")[-2])
        try:
            g = await c.get_messages(chat, msg_id)
            try:
                await g.copy(m.chat.id)
                return await xx.delete()
            except Exception:
                return await gas_download(g, c, xx, m)
        except Exception as er:
            return await xx.edit(str(er))
    else:
        return await xx.edit("Link tidak valid.")
