import traceback

from Userbot import bot, logger, owner_id
from Userbot.helper.tools import zb


async def send_to_user(client, text):
    return await bot.send_message(client, text)


@zb.reconnect()
async def _(client):
    try:
        if not client.is_connected:
            logger.warning(
                f"Koneksi terputus {client.me.id} ! Mencoba menyambung kembali..."
            )
            await send_to_user(
                client.me.id,
                "**Akun kamu sepertinya beban dan delay !! Karena terputus dari koneksi userbot. Silahkan ketik /restart untuk menyalakan kembali userbot.**",
            )
            try:
                await client.stop()
                await client.start()
                return await send_to_user(
                    owner_id,
                    f"**Akun dengan id `{client.me.id}` diputuskan dari koneksi!!**",
                )
            except Exception as e:
                logger.error(f"{traceback.format_exc()}")
                return await send_to_user(owner_id, traceback.format_exc())
    except Exception as e:
        logger.error(f"{traceback.format_exc()}")
        return await send_to_user(owner_id, traceback.format_exc())
    """
    for attempt in range(5):
        if not client.is_connected:
            try:
                await asyncio.sleep(5)
                await client.stop()
                print("Berhasil tersambung kembali.")
                await bot.send_message(
                    owner_id, f"Berhasil tersambung kembali {client.me.id}."
                )
                return
            except Exception as e:
                print(
                    f"Kesalahan saat menyambung kembali (Percobaan {attempt + 1}): {e}"
                )
                await bot.send_message(
                    owner_id,
                    f"Kesalahan saat menyambung kembali {client.me.id} (Percobaan {attempt + 1}): {str(e)}",
                )
        else:
            print("Klien sudah tersambung, tidak perlu reconnect.")
            await bot.send_message(
                owner_id,
                f"Klien {client.me.id} sudah tersambung, tidak perlu reconnect.",
            )
            return
    print("Gagal menyambung kembali setelah beberapa percobaan.")
    return await bot.send_message(
        owner_id,
        f"Gagal menyambung kembali {client.me.id}, setelah beberapa percobaan.",
    )
    """
