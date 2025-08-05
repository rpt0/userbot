from Userbot import *
from Userbot.helper.tools import AFK_, capture_err, h_s, zb

__MODULES__ = "AFK"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_afk")


@zb.ubot("afk")
async def _(client: nlx, message, _):
    reason = client.get_arg(message)
    afk_handler = AFK_(client, message, reason)
    return await afk_handler.set_afk()


@zb.nocmd("AFK", nlx)
@capture_err
async def _(client, message, _):
    afk_handler = AFK_(client, message)
    return await afk_handler.get_afk()


@zb.ubot("unafk")
async def _(client, message, _):
    afk_handler = AFK_(client, message)
    return await afk_handler.unset_afk()
