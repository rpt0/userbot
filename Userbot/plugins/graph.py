################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


import aiofiles
import aiohttp
from telegraph.aio import Telegraph

from Userbot import bot, nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Telegraph"


def help_string(org):
    return h_s(org, "help_graph")


async def post_to_telegraph(is_media: bool, title=None, content=None, media=None):
    telegraph = Telegraph()
    if telegraph.get_access_token() is None:
        await telegraph.create_account(short_name=bot.me.username)
    if is_media:
        # Create a Telegram Post Foto/Video
        response = await telegraph.upload_file(media)
        return f"https://img.yasirweb.eu.org{response[0]['src']}"
    # Create a Telegram Post using HTML Content
    response = await telegraph.create_page(
        title,
        html_content=content,
        author_url=f"https://t.me/{bot.me.username}",
        author_name=bot.me.username,
    )
    return f"https://graph.org/{response['path']}"


async def upload_media(m):
    media = await m.reply_to_message.download()
    base_url = "https://catbox.moe/user/api.php"
    async with aiohttp.ClientSession() as session:
        form_data = aiohttp.FormData()
        form_data.add_field("reqtype", "fileupload")

        async with aiofiles.open(media, mode="rb") as file:
            file_data = await file.read()
            form_data.add_field(
                "fileToUpload",
                file_data,
                filename=media,
                content_type="application/octet-stream",
            )

        async with session.post(base_url, data=form_data) as response:
            response.raise_for_status()
            return (await response.text()).strip()


@zb.ubot("tg")
async def _(client: nlx, message, _):
    emo = Emojik(client)
    emo.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    XD = await message.reply(_("proses").format(emo.proses, proses_))
    if not message.reply_to_message:
        return await XD.edit(_("grp_1").format(emo.gagal))
    if message.reply_to_message.text:
        page_title = f"{client.me.first_name} {client.me.last_name or ''}"
        page_text = message.reply_to_message.text
        page_text = page_text.replace("\n", "<br>")
        try:
            url = await post_to_telegraph(False, page_title, page_text)
        except Exception as exc:
            return await XD.edit(_("err").format(emo.gagal, exc))
        return await XD.edit(
            "{}**Successfully Uploaded: <a href='{}'>Click Here</a>**".format(
                emo.sukses, url
            ),
            disable_web_page_preview=True,
        )
    else:
        try:
            url = await upload_media(message)
        except Exception as exc:
            return await XD.edit(_("err").format(emo.gagal, exc))
        return await XD.edit(
            "{}**Successfully Uploaded: <a href='{}'>Click Here</a>**".format(
                emo.sukses, url
            ),
            disable_web_page_preview=True,
        )


@zb.ubot("upload|upl")
async def _(client: nlx, message, _):
    emo = Emojik(client)
    emo.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    XD = await message.reply(_("proses").format(emo.proses, proses_))
    rep = message.reply_to_message
    if not rep:
        return await XD.edit(_("grp_1").format(emo.gagal))
    try:
        url = await upload_media(message)
    except Exception as exc:
        return await XD.edit(_("err").format(emo.gagal, exc))
    return await XD.edit(
        "{}**Successfully Uploaded: <a href='{}'>Click Here</a>**".format(
            emo.sukses, url
        ),
        disable_web_page_preview=True,
    )
