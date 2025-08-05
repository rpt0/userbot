from Userbot import nlx
from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Archive"

USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_archive")


@zb.ubot("archive|arsip")
async def _(client: nlx, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    if len(message.command) < 2:
        return await message.reply(
            f"<b>{em.gagal}Mohon gunakan query: grup, bot, user, ch.</b>"
        )
    rx = await message.reply(_("proses").format(em.proses, proses_))
    memeg = message.command[1]
    raxxy = await client.get_chats_dialog(memeg)
    for ktl in raxxy:
        await client.archive_chats(ktl)

    return await rx.edit(
        f"<b>{em.sukses}Berhasil mengarsipkan semua {len(raxxy)} {memeg}.</b>"
    )


@zb.ubot("unarchive|unarsip")
async def unarchive_user(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    if len(message.command) < 2:
        return await message.reply(
            f"<b>{em.gagal}Mohon gunakan query: grup, bot, user, ch.</b>"
        )
    rx = await message.reply(_("proses").format(em.proses, proses_))
    memeg = message.command[1]
    raxxy = await client.get_chats_dialog(memeg)
    for ktl in raxxy:
        await client.unarchive_chats(ktl)

    return await rx.edit(
        f"<b>{em.sukses}Berhasil meng-unarsipkan semua {len(raxxy)} {memeg}.</b>"
    )
