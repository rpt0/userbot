import asyncio
import os
import sys
from datetime import datetime

import croniter
from aiorun import run
from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered,
                             SessionRevoked, UserAlreadyParticipant,
                             UserDeactivated, UserDeactivatedBan)
from pytz import timezone


from Userbot import Userbot, bot, dB, list_error, logger, owner_id, nlx
from Userbot.helper.task import (ExpiredBot, ReadUser, TaskPending,
                                 installPeer, sending_user)


def handle_remove_err(_ubot, message):
    dB.remove_ubot(int(_ubot["name"]))
    dB.rm_all(int(_ubot["name"]))
    dB.rem_expired_date(int(_ubot["name"]))
    dB.rem_pref(int(_ubot["name"]))
    logger.error(f"✅ {int(_ubot['name'])} {message}")
    data = {"user": int(_ubot["name"]), "error_msg": message}
    list_error.append(data)


async def start_ubot(_ubot):
    ubot_ = Userbot(**_ubot)
    try:
        await ubot_.start()
        for chat in ["transaksikingzbotz", "KingzUserbotSupport"]:
            try:
                await ubot_.join_chat(chat)
            except UserAlreadyParticipant:
                pass
            except Exception as join_error:
                logger.warning(f"Failed to join {chat}: {join_error}")
    except asyncio.TimeoutError:
        data = {"user": int(_ubot["name"]), "error_msg": "TimeoutError"}
        logger.error(f"❌ Si {int(_ubot['name'])} ga ada respon")
        list_error.append(data)
    except KeyError as e:
        tol = e.args[0]
        logger.error(f"❌ Si {int(_ubot['name'])} kena banned di: {tol}")
        data = {
            "user": int(_ubot["name"]),
            "error_msg": f"Kena banned ({e.args[0]})",
        }
        list_error.append(data)
    except AuthKeyUnregistered:
        handle_remove_err(_ubot, "Telah dihapus karna  hentikan sesi.")
        logger.error(f"✅ {int(_ubot['name'])} Telah dihapus karna  hentikan sesi")
    except AuthKeyDuplicated:
        handle_remove_err(_ubot, "Telah dihapus karna  double sesi")
        logger.error(f"✅ {int(_ubot['name'])} Telah dihapus karna  double sesi")
    except SessionRevoked:
        handle_remove_err(_ubot, "Telah dihapus karna session revoked")
        logger.error(f"✅ {int(_ubot['name'])} Telah dihapus karna session revoked")
    except (UserDeactivatedBan, UserDeactivated):
        handle_remove_err(_ubot, "Telah dihapus karna deak")
        logger.error(f"✅ {int(_ubot['name'])} Telah dihapus karna deak")


async def start_userbots():
    """Start all userbots first."""
    logger.info("🔄 Starting userbots...")
    userbots = dB.get_userbots()
    tasks = [asyncio.create_task(start_ubot(ubot)) for ubot in userbots]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for idx, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"❌ Error starting userbot {userbots[idx]['name']}: {result}")
            raise Exception(f"Userbot {userbots[idx]['name']} failed to start.")

    logger.info("✅ All userbots started successfully.")


async def send_error_msg():
    if list_error != []:
        for x in list_error:
            await sending_user(x["user"], x["error_msg"])


async def auto_restart():
    tz = timezone("Asia/Jakarta")
    cron = croniter.croniter("00 00 * * *", datetime.now(tz))
    while True:
        now = datetime.now(tz)
        next_run = cron.get_next(datetime)

        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        try:
            await bot.send_message(
                owner_id,
                "<blockquote><b>Restart Daily..\n\nTunggu beberapa menit bot sedang di Restart!!</b></blockquote>",
            )
        except:
            pass
        os.execl(sys.executable, sys.executable, "-m", "Userbot")


async def start_main_bot():
    """Start the main bot after userbots."""
    logger.info("🤖 Starting main bot...")
    await bot.start()
    await bot.load_seles()

    logger.info("✅ Main bot started successfully.")


async def run_background_tasks():
    """Run background tasks like expiredUserbots, installPeer, and loadReminders."""
    background_tasks = [
        asyncio.create_task(ReadUser()),
        asyncio.create_task(TaskPending()),
        asyncio.create_task(ExpiredBot()),
        asyncio.create_task(installPeer()),
        asyncio.create_task(nlx.loop_restart()),
        asyncio.create_task(auto_restart()),
    ]
    await asyncio.gather(*background_tasks)
    await send_error_msg()


async def stop_main():
    logger.info("Stopping task and bot")
    await bot.stop()
    dB.close()


async def main():
    await start_userbots()
    await start_main_bot()
    
    # Start augcsast cleanup task after event loop is running
    try:
        from Userbot.plugins.augcsast import cleanup_old_locks
        asyncio.create_task(cleanup_old_locks())
        logger.info("Started autogcast cleanup task")
    except ImportError:
        pass
    
    # Restore autogcast states if any were active before restart
    try:
        from Userbot.plugins.augcsast import restore_autogcast_states
        await restore_autogcast_states(nlx._ubot)
        logger.info("Checked for autogcast states to restore")
    except ImportError:
        pass
    
    await run_background_tasks()
    # await idle()


if __name__ == "__main__":
    run(main(), loop=bot.loop, shutdown_callback=stop_main())
    """
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    loop.run_until_complete(main())
    """
