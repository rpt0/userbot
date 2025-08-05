import asyncio
import os
import zipfile
from datetime import datetime

import aiocron
from pytz import timezone

from config import bot_id, bot_username, dump, nama_bot
from Userbot import bot, logger, nlx

from ..database import dB, db_path
from ..tools._button import MSG, Button

waktu_jkt = timezone("Asia/Jakarta")


async def sending_user(user_id, msg):
    return await bot.send_message(dump, f"⛔ Laporan {user_id} {msg}")


@aiocron.crontab("00 00 * * *", tz=waktu_jkt)
async def _():
    flooding = dB.get_list_from_var(bot_id, "flood_bokep", "user")
    for x in flooding:
        dB.remove_from_var(bot_id, "flood_bokep", int(x), "user")
        return await bot.send_message(dump, f"Reset user bokep {int(x)}")


async def CheckUsers():
    while True:
        await asyncio.sleep(15)
        total = dB.get_var(bot_id, "total_users")
        try:
            if len(nlx._ubot) != total:
                now = datetime.now(timezone("Asia/Jakarta"))
                timestamp = now.strftime("%Y-%m-%d_%H:%M")
                zip_filename = f"{nama_bot}_{timestamp}.zip"
                with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                    if os.path.exists(".env"):
                        env_path = os.path.abspath("./.env")
                        zipf.write(env_path, os.path.basename(env_path))
                        zipf.write(db_path, os.path.basename(db_path))
                    else:
                        zipf.write(db_path, os.path.basename(db_path))
                caption = now.strftime("%d %B %Y %H:%M")
                await bot.send_document(dump, zip_filename, caption=caption)
                os.remove(zip_filename)
                return
        except Exception as e:
            return await bot.send_message(dump, f"CheckUsers error: {str(e)}")


async def ExpiredBot():
    while True:
        await asyncio.sleep(1)
        for X in nlx._ubot:
            try:
                wkt = datetime.now(timezone("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M")
                exp = dB.get_expired_date(X.me.id)
                expir = exp.astimezone(timezone("Asia/Jakarta")).strftime(
                    "%Y-%m-%d %H:%M"
                )
                if expir == wkt:
                    msg = MSG.EXPIRED_MSG_BOT(X)
                    keyb = Button.expired()
                    await bot.send_message(dump, msg, reply_markup=keyb)
                    await X.unblock_user(bot_username)
                    await bot.send_message(X.me.id, msg, reply_markup=keyb)
                    dB.remove_ubot(X.me.id)
                    dB.rem_expired_date(X.me.id)
                    nlx._my_id.remove(X.me.id)
                    nlx._ubot.remove(X)
                    return
            except Exception as e:
                dB.remove_ubot(X.me.id)
                return await bot.send_message(dump, f"ExpiredBot error: {str(e)}")


async def Clean_Accses():
    while True:
        await asyncio.sleep(60)
        prem = dB.get_list_from_var(bot_id, "PREM", "USERS")
        for org in prem:
            try:
                seles = dB.get_list_from_var(bot_id, "seller", "user")
                if org not in seles:
                    return dB.remove_from_var(bot_id, "PREM", org, "USERS")
            except Exception as e:
                return await bot.send_message(dump, f"Clean_Accses error: {str(e)}")


async def TaskPending():
    try:
        CA = asyncio.create_task(Clean_Accses())
        CU = asyncio.create_task(CheckUsers())
        await asyncio.gather(CA, CU)
    except Exception as e:
        return await bot.send_message(dump, f"TaskPending error: {str(e)}")


async def move_expired(mongo_db, sqlite_db, user_id):
    expired_date = mongo_db.get_expired_date(user_id)

    if expired_date:
        formatted_date = expired_date.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        sqlite_db.set_expired_date(user_id, formatted_date)
        logger.info(f"Expired date untuk user {user_id} dipindahkan: {formatted_date}")
    else:
        logger.error(f"Tidak ada expired date untuk user {user_id}")
