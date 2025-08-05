from pyrogram.enums import ChatType

from Userbot import bot, nlx, owner_id

from ..database import dB


async def load_user_allchats(client):
    private = []
    group = []
    globall = []
    all = []
    bots = []
    async for dialog in client.get_dialogs():
        try:
            if dialog.chat.type == ChatType.PRIVATE:
                private.append(dialog.chat.id)
                if dialog.chat.id not in dB.get_list_from_var(client.me.id, "private"):
                    dB.add_to_var(client.me.id, "private", dialog.chat.id)
            elif dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                group.append(dialog.chat.id)
                if dialog.chat.id not in dB.get_list_from_var(client.me.id, "group"):
                    dB.add_to_var(client.me.id, "group", dialog.chat.id)
            elif dialog.chat.type in (
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ):
                globall.append(dialog.chat.id)
                if dialog.chat.id not in dB.get_list_from_var(client.me.id, "global"):
                    dB.add_to_var(client.me.id, "global", dialog.chat.id)
            elif dialog.chat.type in (
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.PRIVATE,
            ):
                all.append(dialog.chat.id)
                if dialog.chat.id not in dB.get_list_from_var(client.me.id, "all"):
                    dB.add_to_var(client.me.id, "all", dialog.chat.id)
            if dialog.chat.type == ChatType.BOT:
                bots.append(dialog.chat.id)
                if dialog.chat.id not in dB.get_list_from_var(client.me.id, "bot"):
                    dB.add_to_var(client.me.id, "bot", dialog.chat.id)
        except Exception:
            continue
    return private, group, globall, all, bots


async def installing_user(client):
    try:
        private, group, globall, all, bots = await load_user_allchats(client)
        client_id = client.me.id
        nlx._my_peer[client_id] = {
            "private": private,
            "group": group,
            "global": globall,
            "all": all,
            "bot": bots,
        }
    except Exception:
        pass


async def installPeer():
    try:
        for client in nlx._ubot:
            await installing_user(client)
    except Exception:
        pass
    try:
        return await bot.send_message(owner_id, "✅ Sukses Install Data Pengguna.")
    except Exception:
        pass
