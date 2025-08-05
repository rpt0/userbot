from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Create"


def help_string(org):
    return h_s(org, "help_create")


@zb.ubot("create")
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    if len(message.command) < 3:
        return await message.reply(
            f"{em.gagal}<b>Silakan ketik `{message.text.split()[0]}` `gc` => untuk membuat grup, atau `ch` => untuk membuat channel.</b>"
        )
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    zb = await message.reply(_("proses").format(em.proses, proses_))
    desc = "Welcome To My " + ("Group" if group_type == "gc" else "Channel")
    if group_type == "gc":
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id.id)
        await zb.edit(
            f"{em.sukses}<b>Berhasil membuat Telegram Grup : [{group_name}]({link.invite_link})</b>",
            disable_web_page_preview=True,
        )
    elif group_type == "ch":
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id.id)
        await zb.edit(
            f"{em.sukses}<b>Berhasil membuat Telegram Channel : [{group_name}]({link.invite_link})</b>",
            disable_web_page_preview=True,
        )
