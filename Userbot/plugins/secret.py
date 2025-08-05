from config import bot_username
from Userbot.helper.tools import h_s, zb

__MODULES__ = "SecretMsg"
USER_PREMIUM = True


def help_string(org):
    return h_s(org, "help_secret")


@zb.ubot("msg")
async def msg_cmd(client, message, _):
    if not message.reply_to_message:
        return await message.reply(_("sct_1").format(message.text.split()[0]))
    text = f"secret {id(message)}"
    await message.delete()
    try:
        x = await client.get_inline_bot_results(bot_username, text)
        return await message.reply_to_message.reply_inline_bot_result(
            x.query_id, x.results[0].id
        )
    except:
        return
