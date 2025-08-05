import os
import random
from io import BytesIO

import aiofiles
import aiohttp

from config import nama_bot
from Userbot import nlx
from Userbot.helper.tools import (Emojik, ReplyCheck, h_s, initial_ctext, zb,
                                  loanjing)

__MODULES__ = "Carbon"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_carbon")


async def buat_bon(code, bgne, theme, language):
    url = "https://carbonara.solopov.dev/api/cook"
    json_data = {
        "code": code,
        "paddingVertical": "56px",
        "paddingHorizontal": "56px",
        "backgroundMode": "color",
        "backgroundColor": bgne,
        "theme": theme,
        "language": language,
        "fontFamily": "Cascadia Code",
        "fontSize": "14px",
        "windowControls": True,
        "widthAdjustment": True,
        "lineNumbers": True,
        "firstLineNumber": 1,
        "name": f"{nama_bot}-Carbon",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@zb.ubot("carbon|carbonara")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    rep = m.reply_to_message
    text = None
    if rep:
        text = m.reply_to_message.text or m.reply_to_message.caption
    if not text:
        return await m.reply(
            _("crbn_1").format(em.gagal, m.text, m.text, m.text, m.text)
        )
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    ex = await m.reply(_("proses").format(em.proses, proses_))
    try:
        if rep:
            if len(m.command) == 1:
                acak = random.choice(loanjing)
                tem = random.choice(loanjing)
                meg = await buat_bon(text, acak, "python", tem)
                with open("carbon.png", "wb") as f:
                    f.write(meg.getvalue())
                await m.reply_photo(
                    "carbon.png",
                    caption=_("crbn_2").format(
                        em.sukses, c.me.mention, reply_to_message_id=ReplyCheck(m)
                    ),
                )
                os.remove("carbon.png")
            elif len(m.command) == 2:
                warna = m.text.split(None, 1)[1] if len(m.command) > 1 else None
                if warna:
                    acak = warna
                else:
                    acak = random.choice(loanjing)
                tem = random.choice(loanjing)
                meg = await buat_bon(text, acak, "python", tem)
                with open("carbon.png", "wb") as f:
                    f.write(meg.getvalue())
                await m.reply_photo(
                    "carbon.png",
                    caption=_("crbn_2").format(
                        em.sukses, c.me.mention, reply_to_message_id=ReplyCheck(m)
                    ),
                )
                os.remove("carbon.png")
            else:
                warna = (
                    m.text.split(None, len(m.command) - 1)[1]
                    if len(m.command) > 1
                    else None
                )
                if warna:
                    acak = warna
                else:
                    acak = random.choice(loanjing)
                tema = (
                    m.text.split(None, len(m.command) - 1)[2]
                    if len(m.command) > 2
                    else None
                )
                if tema:
                    tem = tema
                else:
                    tem = random.choice(loanjing)
                lague = (
                    m.text.split(None, len(m.command) - 1)[3]
                    if len(m.command) > 3
                    else "python"
                )
                meg = await buat_bon(text, acak, lague, tem)
                with open("carbon.png", "wb") as f:
                    f.write(meg.getvalue())
                await m.reply_photo(
                    "carbon.png",
                    caption=_("crbn_2").format(
                        em.sukses, c.me.mention, reply_to_message_id=ReplyCheck(m)
                    ),
                )
                os.remove("carbon.png")

        else:
            doc = await rep.download()
            async with aiofiles.open(doc, mode="r") as f:
                content = await f.read()
            os.remove(doc)
            acak = random.choice(loanjing)
            tem = random.choice(loanjing)
            meg = await buat_bon(content, acak, "python", tem)
            with open("carbon.png", "wb") as f:
                f.write(meg.getvalue())
            await m.reply_photo(
                "carbon.png",
                caption=_("crbn_2").format(
                    em.sukses, c.me.mention, reply_to_message_id=ReplyCheck(m)
                ),
            )
            os.remove("carbon.png")
    except Exception as e:
        return await m.reply(f"Terjadi kesalahan: {str(e)}")
    finally:
        await ex.delete()
        if "meg" in locals():
            meg.close()
    return


@zb.ubot("bglist")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    jadi = _("qot_1").format(em.sukses) + "\n".join(
        [f"<b>{i+1}</b> <code>{theme}</code>" for i, theme in enumerate(loanjing)]
    )
    if len(jadi) > 4096:
        with open("bglist.txt", "w") as file:
            file.write("\n".join(loanjing))
        await m.reply_document("bglist.txt", caption=_("qot_2").format(em.sukses))
        os.remove("bglist.txt")
        return
    else:
        return await pros.edit(jadi)


@zb.ubot("temlist")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    jadi = _("them_1").format(em.sukses) + "\n".join(
        [f"<b>{i+1}</b> <code>{theme}</code>" for i, theme in enumerate(loanjing)]
    )
    if len(jadi) > 4096:
        with open("temlist.txt", "w") as file:
            file.write("\n".join(loanjing))
        await m.reply_document("temlist.txt", caption=_("them_2").format(em.sukses))
        os.remove("temlist.txt")
        return
    else:
        return await pros.edit(jadi)
