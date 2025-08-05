from pyrogram import Client, filters
from pyrogram.raw.functions.contacts import AddContact, DeleteContacts
from pyrogram.errors import RPCError
from pyrogram.raw.types import InputUser

from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "SaveKontak"

def help_string(org):
    return h_s(org, "help_savekontak")

@zb.ubot("savekon")
async def save_contact(client, message, *args):
    user_id = None
    custom_name = ""

    reply_message = message.reply_to_message
    if reply_message and reply_message.from_user:
        user_id = reply_message.from_user.id
        custom_name = message.text.split(maxsplit=1)[1] if len(message.text.split(maxsplit=1)) > 1 else ""
    else:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.reply_text("❎ Mohon reply ke pengguna atau masukkan nama custom untuk menyimpan kontak.")

        custom_name = args[1]
        args = message.command
        if len(args) < 3:
            return await message.reply_text("❎ Mohon reply ke pengguna atau masukkan ID pengguna/username dan nama custom untuk menyimpan kontak.")

        user_id_or_username = args[1]

        try:
            user = await client.get_users(user_id_or_username)
            user_id = user.id
        except Exception as e:
            return await message.reply_text(f"❎ Terjadi kesalahan: {e}")

    if not custom_name.strip():
        return await message.reply_text("❎ Nama custom tidak boleh kosong.")

    first_name = custom_name.strip()
    chat_id = await client.resolve_peer(user_id)

    try:
        response = await client.invoke(
            AddContact(
                id=chat_id,
                first_name=first_name,
                last_name="",
                phone=""
            )
        )
        if response.users and response.users[0].contact:
            await message.reply_text(f"✅ Berhasil menyimpan kontak dengan nama <code>{first_name}</code>")
        else:
            await message.reply_text("❎ Terjadi kesalahan saat menyimpan kontak.")
    except RPCError as e:
        await message.reply_text(f"❎ Terjadi kesalahan: {e}")

@zb.ubot("delkon")
async def delete_contact(client, message, *args):
    user_id = None

    reply_message = message.reply_to_message
    if reply_message and reply_message.from_user:
        user_id = reply_message.from_user.id
    else:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            return await message.reply_text("❎ Mohon reply ke pengguna atau masukkan ID pengguna/username untuk menghapus kontak.")

        user_id_or_username = args[1]

        try:
            user = await client.get_users(user_id_or_username)
            user_id = user.id
        except Exception as e:
            return await message.reply_text(f"❎ Terjadi kesalahan: {e}")

    try:
        response = await client.delete_contacts([user_id])
        if response:
            await message.reply_text(f"✅ Berhasil menghapus kontak dengan ID {user_id}")
        else:
            await message.reply_text("❎ Terjadi kesalahan saat menghapus kontak.")
    except RPCError as e:
        await message.reply_text(f"❎ Terjadi kesalahan: {e}")
