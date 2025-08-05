import importlib

from pyrogram.helpers import kb

from config import bot_username
from Userbot import Userbot
from Userbot.helper.database import dB
from Userbot.helper.tools import zb, org_kontol
from Userbot.plugins import ALL_MODULES


async def restart_userbot(client, message, _):
    list_org = []
    for x in dB.get_userbots():
        list_org.append(int(x["name"]))
    msg = await message.reply("<b>Processing...</b>")
    if message.from_user.id not in list_org:
        return await msg.edit(f"<b>Anda bukan pengguna {bot_username}!!</b>")
    for X in dB.get_userbots():
        if message.from_user.id == int(X["name"]):
            try:
                ub = Userbot(**X)
                await ub.start()
                for mod in ALL_MODULES:
                    importlib.reload(importlib.import_module(f"Userbot.plugins.{mod}"))
                key = kb(
                    [[("⬅️ Kembali")]],
                    resize_keyboard=True,
                    one_time_keyboard=True,
                )
                await msg.delete()
                return await message.reply(
                    f"<b>✅ Berhasil Di Restart {ub.me.first_name} {ub.me.last_name or ''} | {ub.me.id}.</b>",
                    reply_markup=key,
                )
            except Exception as error:
                return await msg.edit(f"<b>{error}</b>")


@zb.bots("restart")
@zb.menten
@org_kontol
async def _(client, message, _):
    return await restart_userbot(client, message, _)
