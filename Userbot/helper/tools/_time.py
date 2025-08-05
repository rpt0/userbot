# @TomiX

from time import time as waktunya

start_time = waktunya()

from config import bot_id

from ..database import dB


async def get_time(seconds):
    dia = dB.get_var(bot_id, "bahasa_dia")
    lng = dB.get_var(dia, "bahasa")
    count = 0
    up_time = ""
    time_list = []

    if lng == "en":
        time_suffix_list = [
            "s",
            "m",
            "h",
            "d",
            "w",
            "m",
            "y",
        ]
    elif lng == "id":
        time_suffix_list = ["d", "m", "j", "h", "m", "b", "t"]
    else:
        time_suffix_list = [
            "s",
            "m",
            "h",
            "d",
            "w",
            "m",
            "y",
        ]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        up_time += time_list.pop() + ":"

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time
