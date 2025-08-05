from gc import get_objects

from pyrogram.enums import ParseMode
from pyrogram.helpers import ikb

from config import nama_bot
from Userbot import nlx
from Userbot.helper.database import dB
from Userbot.helper.tools import zb

mmk = {
    "(",
    ")",
    "KLOS",
    "AC",
    "DEL",
    "%",
    "/",
    "*",
    "-",
    "+",
    "00",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ".",
    "=",
}

hitung = []


def calc_help():
    return ikb(
        [
            [
                ("(", "calc_("),
                (")", "calc_)"),
            ],
            [
                ("%", "calc_%"),
                ("AC", "calc_AC"),
                ("DEL", "calc_DEL"),
                ("÷", "calc_/"),
            ],
            [
                ("7", "calc_7"),
                ("8", "calc_8"),
                ("9", "calc_9"),
                ("x", "calc_*"),
            ],
            [
                ("4", "calc_4"),
                ("5", "calc_5"),
                ("6", "calc_6"),
                ("-", "calc_-"),
            ],
            [
                ("1", "calc_1"),
                ("2", "calc_2"),
                ("3", "calc_3"),
                ("+", "calc_+"),
            ],
            [
                ("00", "calc_00"),
                ("0", "calc_0"),
                ("=", "calc_="),
                (".", "calc_."),
            ],
            [
                ("Close", "calc_KLOS"),
            ],
        ]
    )


@zb.callback("calc_")
async def _(c, cq, _):
    global hitung
    kb = calc_help()
    data = cq.data.split("_")[1]
    teks = f"{nama_bot} Calculator"
    if data not in mmk:
        return
    user = cq.from_user
    kntl = dB.get_var(user.id, "KALKU")
    iid = dB.get_var(user.id, "CB_CALCU")
    if user.id != int(iid):
        return await cq.answer(
            f"BELI LAH {nama_bot} WAHAI {fullname}.\nHANYA 35k, ANDA SUDAH BISA MENIKMATI SEKIAN BANYAKNYA FITUR DI {nama_bot}!",
            show_alert=True,
        )
    fullname = user.first_name
    if user.last_name:
        fullname += f" {user.last_name}"

    if data == "DEL":
        if hitung:
            hitung = hitung[:-1]
        nan = f"{''.join(hitung)}\n\n{teks}"
        return await cq.edit_message_text(
            text=nan,
            reply_markup=kb,
            parse_mode=ParseMode.HTML,
        )
    elif data == "AC":
        hitung = []
        nan = f"{''.join(hitung)}\n\n{teks}"
        return await cq.edit_message_text(
            text=nan, reply_markup=kb, parse_mode=ParseMode.HTML
        )
    elif data == "=":
        try:
            expression = (
                "".join(hitung).replace("×", "*").replace("÷", "/").replace("^", "**")
            )
            hasil = str(eval(expression))
            await cq.answer(f"Hasil: {hasil}", show_alert=True)
            hitung = [hasil]
            return await cq.edit_message_text(
                text=f"{hasil}\n\n{teks}", reply_markup=kb
            )
        except Exception as e:
            return await cq.answer(f"Error: {str(e)}", show_alert=True)
            hitung = []
    elif data == "KLOS":
        _id = dB.get_var(user.id, "kalku_inline")
        m = next((obj for obj in get_objects() if id(obj) == int(_id)), None)
        client = m._client

        if user.id not in nlx._my_id:
            return await cq.answer(
                f"{fullname} KAYA KONTOL! SIRIK AJA LO!\nGAUSAH DIPENCET! ANJING! MEMEK! NGENTOT! BELI SENDIRI SANA!!",
                show_alert=True,
            )
        if cq.message:
            await cq.message.delete()
        else:
            try:
                chat_id = int(kntl["chat_id"])
                messsage_id = int(kntl["message_id"])
                return await client.delete_messages(chat_id, messsage_id)
            except Exception as er:
                return await cq.answer(f"{str(er)}", True)
            hitung = []
            return
    else:
        if user.id not in nlx._my_id:
            return await cq.answer(
                f"BELI LAH {nama_bot} WAHAI {fullname}.\nHANYA 35k, ANDA SUDAH BISA MENIKMATI SEKIAN BANYAKNYA FITUR DI Mix-Userbot!",
                show_alert=True,
            )
        hitung.append(data)
        nan = f"{''.join(hitung)}\n\n{teks}"
        return await cq.edit_message_text(
            text=nan, reply_markup=kb, parse_mode=ParseMode.HTML
        )
