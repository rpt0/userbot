import asyncio

from pyrogram import enums
from pyrogram.errors import (ChannelPrivate, FloodWait, PeerIdInvalid,
                             UserBannedInChannel)
from pyrogram.raw.functions.messages import ReadMentions

from Userbot import bot, nlx, owner_id

from ..database import dB


async def autor_gc(c):
    if not dB.get_var(c.me.id, "read_gc"):
        return
    wkt = dB.get_var(c.me.id, "time_read") or 7200
    while True:
        await asyncio.sleep(wkt)
        try:
            async for bb in c.get_dialogs():
                try:
                    if bb.chat.type in [
                        enums.ChatType.GROUP,
                        enums.ChatType.SUPERGROUP,
                    ]:
                        try:
                            await c.read_chat_history(bb.chat.id, max_id=0)
                        except (ChannelPrivate, PeerIdInvalid, UserBannedInChannel):
                            continue
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            try:
                                await c.read_chat_history(bb.chat.id, max_id=0)
                            except:
                                pass
                except Exception as e:
                    return f"An error occurred while processing dialog: {str(e)}"
        except Exception as e:
            return f"An error occurred while fetching dialogs: {str(e)}"


async def autor_mention(c):
    if not dB.get_var(c.me.id, "read_mention"):
        return
    wkt = dB.get_var(c.me.id, "time_read") or 7200
    while True:
        await asyncio.sleep(wkt)
        try:
            async for bb in c.get_dialogs():
                try:
                    if bb.chat.type in [
                        enums.ChatType.GROUP,
                        enums.ChatType.SUPERGROUP,
                    ]:
                        try:
                            await c.invoke(
                                ReadMentions(peer=await c.resolve_peer(bb.chat.id))
                            )
                        except (ChannelPrivate, PeerIdInvalid, UserBannedInChannel):
                            continue
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            try:
                                await c.invoke(
                                    ReadMentions(peer=await c.resolve_peer(bb.chat.id))
                                )
                            except:
                                pass
                except Exception as e:
                    return f"An error occurred while processing dialog: {str(e)}"
        except Exception as e:
            return f"An error occurred while fetching dialogs: {str(e)}"


async def autor_ch(c):
    if not dB.get_var(c.me.id, "read_ch"):
        return
    wkt = dB.get_var(c.me.id, "time_read") or 7200
    while True:
        await asyncio.sleep(wkt)

        try:
            async for bb in c.get_dialogs():
                try:
                    if bb.chat.type == enums.ChatType.CHANNEL:
                        try:
                            await c.read_chat_history(bb.chat.id, max_id=0)
                        except (ChannelPrivate, PeerIdInvalid, UserBannedInChannel):
                            continue
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            try:
                                await c.read_chat_history(bb.chat.id, max_id=0)
                            except:
                                pass
                except Exception as e:
                    return f"An error occurred while processing dialog: {str(e)}"
        except Exception as e:
            return f"An error occurred while fetching dialogs: {str(e)}"


async def autor_us(c):
    if not dB.get_var(c.me.id, "read_us"):
        return
    wkt = dB.get_var(c.me.id, "time_read") or 7200
    while True:
        await asyncio.sleep(wkt)

        try:
            async for bb in c.get_dialogs():
                try:
                    if bb.chat.type == enums.ChatType.PRIVATE:
                        try:
                            await c.read_chat_history(bb.chat.id, max_id=0)
                        except (ChannelPrivate, PeerIdInvalid, UserBannedInChannel):
                            continue
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            try:
                                await c.read_chat_history(bb.chat.id, max_id=0)
                            except:
                                pass
                except Exception as e:
                    return f"An error occurred while processing dialog: {str(e)}"
        except Exception as e:
            return f"An error occurred while fetching dialogs: {str(e)}"


async def autor_bot(c):
    if not dB.get_var(c.me.id, "read_bot"):
        return
    wkt = dB.get_var(c.me.id, "time_read") or 7200
    while True:
        await asyncio.sleep(wkt)

        try:
            async for bb in c.get_dialogs():
                try:
                    if bb.chat.type == enums.ChatType.BOT:
                        try:
                            await c.read_chat_history(bb.chat.id, max_id=0)
                        except (ChannelPrivate, PeerIdInvalid, UserBannedInChannel):
                            continue
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            try:
                                await c.read_chat_history(bb.chat.id, max_id=0)
                            except:
                                pass
                except Exception as e:
                    return f"An error occurred while processing dialog: {str(e)}"
        except Exception as e:
            return f"An error occurred while fetching dialogs: {str(e)}"


async def autor_all(c):
    if not dB.get_var(c.me.id, "read_all"):
        return
    wkt = dB.get_var(c.me.id, "time_read") or 7200
    while True:
        await asyncio.sleep(wkt)
        try:
            async for bb in c.get_dialogs():
                try:
                    if bb.chat.type in [
                        enums.ChatType.GROUP,
                        enums.ChatType.SUPERGROUP,
                        enums.ChatType.CHANNEL,
                        enums.ChatType.PRIVATE,
                        enums.ChatType.BOT,
                    ]:
                        try:
                            await c.read_chat_history(bb.chat.id, max_id=0)
                        except (ChannelPrivate, PeerIdInvalid, UserBannedInChannel):
                            continue
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            try:
                                await c.read_chat_history(bb.chat.id, max_id=0)
                            except:
                                pass
                except Exception as e:
                    return f"An error occurred while processing dialog: {str(e)}"
        except Exception as e:
            return f"An error occurred while getting dialogs: {str(e)}"


async def ReadUser():
    for X in nlx._ubot:
        try:
            asyncio.create_task(autor_all(X))
            asyncio.create_task(autor_bot(X))
            asyncio.create_task(autor_gc(X))
            asyncio.create_task(autor_mention(X))
            asyncio.create_task(autor_ch(X))
            asyncio.create_task(autor_us(X))
            asyncio.create_task(autor_bot(X))
        except Exception as e:
            return await bot.send_message(owner_id, f"Error Auto Read {str(e)}")
