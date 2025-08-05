import asyncio
import contextlib
import io
import os
import platform
import subprocess
import sys
from datetime import datetime, timedelta
from time import perf_counter

import psutil
import pyrogram
import pyrogram.enums
import pyrogram.raw
import pyrogram.types
from meval import meval
from psutil._common import bytes2human
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.errors import FloodWait, MessageNotModified

import config
from config import DEVS, bot_username, the_cegers
from Userbot import bot, nlx
from Userbot.helper.database import dB, state
from Userbot.helper.tools import Emojik, fetch, zb, paste


@zb.ubot("buttonch")
async def _(c: nlx, m, _):
    TM = await m.reply_text("Processing...")
    rep = m.reply_to_message
    if not rep and len(m.command) < 2:
        return await TM.edit("Reply to message!!")
    dB.set_var(c.me.id, "toprem", rep.text)
    link = m.text.split(None, 1)[1]
    await c.send_message(bot_username, f"/btch {link}")
    return await TM.edit("Done")


@zb.bots("trash")
@zb.thecegers
async def _(c: bot, m, _):
    return await cb_trash(c, m, _)


@zb.ubot("trash")
async def _(c: nlx, m, _):
    kon = m.from_user or m.sender_chat
    if kon.id not in the_cegers:
        return
    return await cb_trash(c, m, _)


async def cb_trash(c, m, _):
    if m.reply_to_message:
        try:
            if len(m.command) < 2:
                if len(str(m.reply_to_message)) > 4096:
                    with io.BytesIO(str.encode(str(m.reply_to_message))) as out_file:
                        out_file.name = "trash.txt"
                        return await m.reply_document(document=out_file)
                else:
                    return await m.reply(f"<pre>{m.reply_to_message}</pre>")
            else:
                value = eval(f"m.reply_to_message.{m.command[1]}")
                if len(str(value)) > 4096:
                    with io.BytesIO(str.encode(str(value))) as out_file:
                        out_file.name = "trash.txt"
                        return await m.reply_document(document=out_file)
                else:
                    return await m.reply(f"<pre>{value}</pre>")
        except Exception as error:
            return await m.reply(str(error))
    else:
        return await m.reply("noob")


@zb.bots("sh|shell")
@zb.thecegers
async def _(c: bot, m, _):
    return await cb_shell(c, m, _)


@zb.ubot("sh|shell")
@zb.thecegers
async def _(c: nlx, m, _):
    kon = m.from_user or m.sender_chat
    if kon.id not in the_cegers:
        return
    return await cb_shell(c, m, _)


async def cb_shell(c, m, _):
    if len(m.command) < 2:
        return await m.reply("Noob!!")
    cmd_text = m.text.split(maxsplit=1)[1]
    text = f"<code>{cmd_text}</code>\n\n"
    start_time = perf_counter()
    try:
        stdout, stderr = await c.bash(cmd_text)
    except asyncio.TimeoutError:
        text += "<b>Timeout expired!!</b>"
        return await m.reply(text)
    finally:
        duration = perf_counter() - start_time
    if len(stdout) > 4096:
        anuk = await m.reply("<b>Oversize, sending file...</b>")
        with open("output.txt", "w") as file:
            file.write(stdout)
        await c.send_document(
            m.chat.id,
            "output.txt",
            caption=f"<b>Command completed in `{duration:.2f}` seconds.</b>",
            reply_to_message_id=m.id,
        )
        os.remove("output.txt")
        return await anuk.delete()
    else:
        text += f"<pre><code>{stdout}</code></pre>"

    if stderr:
        text += f"<blockquote>{stderr}</blockquote>"
    text += f"\n<b>Completed in `{duration:.2f}` seconds.</b>"
    return await m.reply(text)


@zb.bots("eval")
@zb.thecegers
async def _(c: bot, message, _):
    return await cb_evalusi(c, message, _)


@zb.ubot("eval")
async def _(c: nlx, message, _):
    kon = message.from_user or message.sender_chat
    if kon.id not in the_cegers:
        return
    return await cb_evalusi(c, message, _)


@zb.cegers("ceval")
async def _(c: nlx, message, _):
    return await cb_evalusi(c, message, _)


async def cb_evalusi(client, message, _):
    if len(message.command) > 1:
        cmd = message.command[1]
    else:
        return await message.reply("<b>Noob</b>")
    try:
        cmd = message.text.split(maxsplit=1)[1]
    except IndexError:
        return await message.reply("<b>No code provided to evaluate!</b>")

    file = io.StringIO()
    eval_vars = {
        # PARAMETERS
        "c": client,
        "m": message,
        "u": (message.reply_to_message or message).from_user,
        "r": message.reply_to_message,
        "chat_id": message.chat.id,
        # PYROGRAM
        "asyncio": asyncio,
        "pyrogram": pyrogram,
        "raw": pyrogram.raw,
        "enums": pyrogram.enums,
        "types": pyrogram.types,
        # LOCAL
        "bot": bot,
        "config": config,
        "state": state,
        "nlx": nlx,
        "dB": dB,
        "fetch": fetch,
    }
    file = io.StringIO()
    with contextlib.redirect_stdout(file):
        try:
            meval_out = await meval(cmd, globals(), **eval_vars)
            print_out = file.getvalue().strip() or str(meval_out) or "None"
        except Exception as e:
            print_out = str(e)

    final_output = f"<pre language=Input>{cmd}</pre>"
    final_output += f"<pre language=Python>{print_out}</pre>"

    try:
        if len(final_output) > 4096:
            link = await paste(final_output)
        else:
            link = final_output
    except Exception as e:
        return await message.reply_text(f"<b>Error!\n <code>{str(e)}</code></b>")
    return await message.reply(link)


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@zb.ubot("host")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    xx = await m.reply(f"{em.proses}Processing...")
    uname = platform.uname()
    softw = "Informasi Sistem\n"
    softw += f"Sistem   : {uname.system}\n"
    softw += f"Rilis    : {uname.release}\n"
    softw += f"Versi    : {uname.version}\n"
    softw += f"Mesin    : {uname.machine}\n"

    boot_time_timestamp = psutil.boot_time()

    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"Waktu Hidup: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}\n"

    softw += "\nInformasi CPU\n"
    softw += "Physical cores   : " + str(psutil.cpu_count(logical=False)) + "\n"
    softw += "Total cores      : " + str(psutil.cpu_count(logical=True)) + "\n"
    cpufreq = psutil.cpu_freq()
    softw += f"Max Frequency    : {cpufreq.max:.2f}Mhz\n"
    softw += f"Min Frequency    : {cpufreq.min:.2f}Mhz\n"
    softw += f"Current Frequency: {cpufreq.current:.2f}Mhz\n\n"
    softw += "CPU Usage Per Core\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        softw += f"Core {i}  : {percentage}%\n"
    softw += "Total CPU Usage\n"
    softw += f"Semua Core: {psutil.cpu_percent()}%\n"

    softw += "\nBandwith Digunakan\n"
    softw += f"Unggah  : {get_size(psutil.net_io_counters().bytes_sent)}\n"
    softw += f"Download: {get_size(psutil.net_io_counters().bytes_recv)}\n"

    svmem = psutil.virtual_memory()
    softw += "\nMemori Digunakan\n"
    softw += f"Total     : {get_size(svmem.total)}\n"
    softw += f"Available : {get_size(svmem.available)}\n"
    softw += f"Used      : {get_size(svmem.used)}\n"
    softw += f"Percentage: {svmem.percent}%\n"

    return await xx.edit(f"{softw}")


async def generate_sysinfo(workdir):
    info = {
        "BOOT": (
            datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        )
    }
    cpu_freq = psutil.cpu_freq().current
    if cpu_freq >= 1000:
        cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
    else:
        cpu_freq = f"{round(cpu_freq, 2)}MHz"
    info["CPU"] = (
        f"{psutil.cpu_percent(interval=1)}% " f"({psutil.cpu_count()}) " f"{cpu_freq}"
    )
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    info["RAM"] = f"{bytes2human(vm.used)}, " f"/ {bytes2human(vm.total)}"
    info["SWAP"] = f"{bytes2human(sm.total)}, {sm.percent}%"
    du = psutil.disk_usage(workdir)
    dio = psutil.disk_io_counters()
    info["DISK"] = (
        f"{bytes2human(du.used)} / {bytes2human(du.total)} " f"({du.percent}%)"
    )
    if dio:
        info["DISK I/O"] = (
            f"R {bytes2human(dio.read_bytes)} | W {bytes2human(dio.write_bytes)}"
        )
    nio = psutil.net_io_counters()
    info["NET I/O"] = (
        f"TX {bytes2human(nio.bytes_sent)} | RX {bytes2human(nio.bytes_recv)}"
    )
    sensors_temperatures = psutil.sensors_temperatures()
    if sensors_temperatures:
        temperatures_list = [x.current for x in sensors_temperatures["coretemp"]]
        temperatures = sum(temperatures_list) / len(temperatures_list)
        info["TEMP"] = f"{temperatures}\u00b0C"
    info = {f"{key}:": value for (key, value) in info.items()}
    max_len = max(len(x) for x in info)
    return "\n" + "\n".join([f"{x:<{max_len}} {y}" for x, y in info.items()]) + ""


@zb.ubot("stats")
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    response = await generate_sysinfo(c.workdir)
    return await m.reply(
        f"<b><blockquote>{em.proses}#Stats : Total Usage\n{response}</blockquote></b>"
    )


@zb.ubot("benal")
@zb.thecegers
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    chat = await c.get_chat(m.chat.id)
    tunggu = None
    member = await c.get_chat_member(m.chat.id, m.from_user.id)
    if member.privileges:
        if member.privileges.can_manage_chat and member.privileges.can_restrict_members:
            is_channel = True if m.chat.type == ChatType.CHANNEL else False
            if m.from_user.id not in DEVS:
                await m.reply(f"{em.gagal}Maaf, Anda bukan seorang DEVELOPER!")
                return
            kick_count = 0
            fail_count = 0
            members_count = chat.members_count
            if members_count <= 200:
                async for member in chat.get_members():
                    if member.user.id == c.me.id:
                        continue
                    elif (
                        member.status == ChatMemberStatus.ADMINISTRATOR
                        or member.status == ChatMemberStatus.OWNER
                    ):
                        continue
                    try:
                        await chat.ban_member(
                            member.user.id, datetime.now() + timedelta(seconds=30)
                        )
                        kick_count += 1
                        try:
                            await m.edit(
                                f"{em.sukses}Berhasil ban : <code>{kick_count}</code> member. Gagal: <code>{fail_count}</code>"
                            )
                        except MessageNotModified:
                            pass
                    except FloodWait as e:
                        fail_count += 1
                        tunggu = e.value
                        await asyncio.sleep(e.value)
                        try:
                            await m.edit(f"{em.gagal}Harap tunggu {tunggu} detik lagi")
                        except MessageNotModified:
                            pass
                try:
                    await m.edit(
                        f"{em.sukses}Berhasil ban : <code>{kick_count}</code> member. Gagal: <code>{fail_count}</code>"
                    )
                except MessageNotModified:
                    pass
            else:
                loops_count = members_count / 200
                loops_count = round(loops_count)
                for loop_num in range(loops_count):
                    async for member in chat.get_members():
                        if member.user.id == c.me.id:
                            continue
                        elif (
                            member.status == ChatMemberStatus.ADMINISTRATOR
                            or member.status == ChatMemberStatus.OWNER
                        ):
                            continue
                        try:
                            await chat.ban_member(
                                member.user.id, datetime.now() + timedelta(seconds=30)
                            )
                            kick_count += 1
                            try:
                                await m.edit(
                                    f"{em.sukses}Berhasil ban : <code>{kick_count}</code> member. Gagal: <code>{fail_count}</code>"
                                )
                            except (
                                pyrogram.errors.exceptions.bad_request_400.MessageNotModified
                            ):
                                pass
                        except FloodWait as e:
                            fail_count += 1
                            tunggu = e.value
                            await asyncio.sleep(e.value)
                            try:
                                await m.edit(
                                    f"{em.gagal}Silahkan tunggu selama {tunggu} detik!"
                                )
                            except MessageNotModified:
                                pass
                    await asyncio.sleep(tunggu)
                try:
                    await m.edit(
                        f"{em.sukses}Berhasil kick : <code>{kick_count}</code> member! Gagal: <code>{fail_count}</code>"
                    )
                except MessageNotModified:
                    pass
        else:
            return await m.reply(
                f"{em.gagal}Izin admin Anda tidak cukup untuk menggunakan perintah ini!"
            )
    else:
        return await m.reply(
            f"{em.gagal}Anda harus menjadi admin dan memiliki izin yang cukup!"
        )


async def mak_mek(c, chat_id, message):
    em = Emojik(c)
    em.initialize()
    unban_count = 0
    async for meki in c.get_chat_members(chat_id, filter=ChatMembersFilter.BANNED):
        if meki.user is not None:
            try:
                user_id = meki.user.id
                await c.unban_chat_member(chat_id, user_id)
                unban_count += 1
                await message.edit(
                    f"{em.proses}Memproses unban... Berhasil unban: {unban_count}"
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await c.send_message(
                    chat_id, f"{em.gagal}Harap tunggu {e.value} detik lagi"
                )
    return await message.edit(
        f"{em.sukses}Berhasil unban : <code>{unban_count}</code> member."
    )


@zb.ubot("anben")
@zb.thecegers
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    dia = await c.get_chat_member(chat_id=m.chat.id, user_id=m.from_user.id)
    pros = await m.reply(f"{em.proses}Sabar ya..")
    if dia.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        if m.from_user.id not in DEVS:
            await m.reply(f"{em.gagal}Maaf, Anda bukan seorang DEVELOPER!")
            await pros.delete()
            return

        return await mak_mek(c, m.chat.id, pros)
    else:
        await m.reply(
            f"{em.gagal}Anda harus menjadi admin atau memiliki izin yang cukup untuk menggunakan perintah ini!"
        )
        await pros.delete()
        return


async def send_large_output(message, output):
    with io.BytesIO(str.encode(str(output))) as out_file:
        out_file.name = "update.txt"
        await message.reply_document(document=out_file)


@zb.ubot("reboot|update")
async def _(c: nlx, m, _):
    kon = m.from_user or m.sender_chat
    if kon.id not in the_cegers:
        return
    return await cb_gitpull2(c, m, _)


@zb.bots("update")
@zb.bots("reboot")
@zb.thecegers
async def _(c: bot, m, _):
    return await cb_gitpull2(c, m, _)


async def cb_gitpull(c, m, _):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if "Already up to date." in str(out):
        return await m.reply(f"<pre>{out}</pre>")
    elif int(len(str(out))) > 4096:
        await send_large_output(m, out)
    else:
        await m.reply(f"<pre>{out}</pre>")
    await c.shell_exec("pkill -f gunicorn")
    os.execl(sys.executable, sys.executable, "-m", "Userbot")


async def cb_gitpull2(c, m, _):
    if m.command[0] == "update":
        out, err = await c.shell_exec("git pull")
        if "Already up to date." in str(out):
            return await m.reply(f"<pre>{out}</pre>")
        elif len(str(out)) > 4096:
            await send_large_output(m, out)
        else:
            msg = f"<pre>{out}</pre>"
        try:
            oot, arr = await c.shell_exec("pkill -f gunicorn")
            msg += "\n".join(oot)
        except Exception as e:
            return await m.reply(f"Failed to stop Gunicorn: {str(e)}")
        await m.reply(
            msg
            + "\n<b>✅ Gunicorn stopped successfully. Trying to Update Userbot!!</b>"
        )
        os.execl(sys.executable, sys.executable, "-m", "Userbot")
    elif m.command[0] == "reboot":
        oot, arr = await c.shell_exec("pkill -f gunicorn")
        await m.reply(
            "<b>✅ Gunicorn stopped successfully. Trying to restart Userbot!!</b>"
        )
        os.execl(sys.executable, sys.executable, "-m", "Userbot")


@zb.cegers("logut")
@zb.thecegers
async def _(c: nlx, m, _):
    em = Emojik(c)
    em.initialize()
    if not m.reply_to_message:
        return
    pros = await m.reply(_("proses").format(em.proses))
    await pros.edit(f"{em.sukses}Done!! You Logout!!")
    return await c.log_out()
