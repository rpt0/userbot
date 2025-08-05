import platform
import sys
from datetime import datetime
import psutil
from asyncio import create_subprocess_exec as asyncrunapp
from pyrogram import filters, Client
from pyrogram import __version__
from pyrogram.types import Message
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "SystemStat"

def help_string(org):
    return h_s(org, "help_systemstat")

async def get_readable_time(seconds: int) -> str: 
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["Dtk", "Mnt", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

@zb.ubot("spc")
async def psu(client: Client, message: Message, *args):
    uname = platform.uname()
    softw = f"""<blockquote><b>Informasi Sistem</b></blockquote>\n"""
    softw += f"ᚗ Sistem   : {uname.system}\n"
    softw += f"ᚗ Rilis    : {uname.release}\n"
    softw += f"ᚗ Versi    : {uname.version}\n"
    softw += f"ᚗ Mesin    : {uname.machine}\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"ᚗ Waktu Hidup: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}\n"
    # CPU Cores
    cpuu = f"""<blockquote><b>Informasi CPU</b></blockquote>\n"""
    cpuu += "ᚗ Physical cores   : " + \
        str(psutil.cpu_count(logical=False)) + "\n"
    cpuu += "ᚗ Total cores      : " + \
        str(psutil.cpu_count(logical=True)) + "\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"ᚗ Max Frequency    : {cpufreq.max:.2f}Mhz\n"
    cpuu += f"ᚗ Min Frequency    : {cpufreq.min:.2f}Mhz\n"
    cpuu += f"ᚗ Current Frequency: {cpufreq.current:.2f}Mhz\n\n"
    # CPU usage
    cpuu += f"""<blockquote><b>CPU Usage Per Core</b></blockquote>\n"""
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"ᚗ Core {i}  : {percentage}%\n"
    cpuu += f"ᚗ Semua Core: {psutil.cpu_percent()}%\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = f"""<blockquote><b>Memori Digunakan</b></blockquote>\n"""
    memm += f"ᚗ Total     : {get_size(svmem.total)}\n"
    memm += f"ᚗ Available : {get_size(svmem.available)}\n"
    memm += f"ᚗ Used      : {get_size(svmem.used)}\n"
    memm += f"ᚗ Percentage: {svmem.percent}%\n"
    # Bandwidth Usage
    bw = f"""<blockquote><b>Bandwith Digunakan**</b></blockquote>\n"""
    bw += f"ᚗ Unggah  : {get_size(psutil.net_io_counters().bytes_sent)}\n"
    bw += f"ᚗ Download: {get_size(psutil.net_io_counters().bytes_recv)}\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(bw)}\n"
    help_string += f"""<blockquote><b>Informasi Mesin</b></blockquote>\n"""
    help_string += f"ᚗ Python {sys.version}\n"
    help_string += f"ᚗ Pyrogram {__version__}\n\n"
    help_string += f"**Powered by {client.me.mention}**\n"
    await message.reply(help_string)
