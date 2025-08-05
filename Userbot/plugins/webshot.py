################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 @ CREDIT : NAN-DEV
"""
################################################################


from base64 import b64decode
from io import BytesIO

from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb, post

__MODULES__ = "Webshot"

USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_webshot")


async def ss(url, full: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    payload = {
        "url": url,
        "width": 1920,
        "height": 1080,
        "scale": 1,
        "format": "jpeg",
    }
    if full:
        payload["full"] = True
    data = await post(
        "https://webscreenshot.vercel.app/api",
        data=payload,
    )
    if "image" not in data:
        return None
    b = data["image"].replace("data:image/jpeg;base64,", "")
    file = BytesIO(b64decode(b))
    file.name = "webss.jpg"
    return file


@zb.ubot("webss|webshot")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(_("webs_1").format(em.gagal, m.text.split()[0]))

    if len(m.command) == 2:
        url = m.text.split(None, 1)[1]
        full = False
    elif len(m.command) == 3:
        url = m.text.split(None, 2)[1]
        full = m.text.split(None, 2)[2].lower().strip() in [
            "yes",
            "y",
            "1",
            "true",
        ]
    else:
        return await m.reply(_("webs_1").format(em.gagal, m.text.split()[0]))
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    tit = await m.reply(_("proses").format(em.proses, proses_))
    try:
        photo = await ss(url, full)
        if not photo:
            await tit.edit(_("webs_2").format(em.gagal))
            return await tit.delete()
        await tit.delete()
        tot = await m.reply(_("upload").format(em.proses))

        if not full:
            await m.reply_photo(photo)
        else:
            await m.reply_document(photo)
        return await tot.delete()
    except Exception as r:
        return await tot.edit(_("err").format(em.gagal, r))
