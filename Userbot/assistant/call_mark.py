from pyrogram.enums import ParseMode
from pyrogram.errors import MediaCaptionTooLong
from pyrogram.helpers import ikb

from Userbot.helper.database import dB
from Userbot.helper.tools import zb


def markdown_help():
    return ikb(
        [
            [("Markdown Format", "markd.butformat"), ("Fillings", "markd.filing")],
            [("Back Help", "help_back(0)")],
        ]
    )


mark_1 = """
**Markdown Formatting**
 Anda dapat memformat pesan Anda menggunakan **tebal**, _miring_, --garis bawah--, ~~coret~~, dan banyak lagi.

`<code>kata kode</code>`: Tanda kutip terbalik digunakan buat font monospace. Ditampilkan sebagai: `kata kode`.

 `<i>miring</i>`: Garis bawah digunakan buat font miring. Ditampilkan sebagai: __kata miring__.

 `<b>tebal</b>`: Asterisk digunakan buat font tebal. Ditampilkan sebagai: **kata tebal**.

 `<u>garis bawah</u>`: Buat membuat teks --garis bawah--.

 `<strike>coret</strike>`: Tilda digunakan buat strikethrough. Ditampilkan sebagai: ~~coret~~.

 `<spoiler>spoiler</spoiler>`: Garis vertikal ganda digunakan buat spoiler. Ditampilkan sebagai: ||spoiler||.

 `[hyperlink](contoh)`: Ini adalah pemformatan yang digunakan buat hyperlink.

 `<blockquote>teks quote</blockquote>`: Ini adalah pemformatan untuk > teks quote >

 `Hallo Disini [Tombol 1|https://link.com]` : Ini adalah pemformatan yang digunakan membuat tombol.
 `Halo Disini [Tombol 1|t.me/ZeebSupport][Tombol 2|t.me/ruangzeeb|same]` : Ini akan membuat tombol berdampingan.

 Anda juga bisa membuat tombol callback_data dengan diawal tanda `#`. Untuk lebih lanjut silahkan ke @ZeebSupport untuk meminta bantuan.
"""

mark_2 = "<blockquote><b>Fillings</b>\n\nAnda juga dapat menyesuaikan isi pesan Anda dengan data kontekstual. Misalnya, Anda bisa menyebut nama pengguna dalam pesan selamat datang, atau menyebutnya dalam filter!\n\n<b>Isian yang didukung:</b>\n\n<code>{first}</code>: Nama depan pengguna.\n<code>{last}</code>: Nama belakang pengguna.\n<code>{fullname}</code>: Nama lengkap pengguna.\n<code>{username}</code>: Nama pengguna pengguna. Jika mereka tidak memiliki satu, akan menyebutkan pengguna tersebut.\n<code>{mention}</code>: Menyebutkan pengguna dengan nama depan mereka.\n<code>{id}</code>: ID pengguna.\n<code>{chatname}</code>: Nama obrolan.</blockquote>"


@zb.callback("^markd.")
async def cb_markd(c, cq, _):
    cmd = cq.data.split(".")[1]
    cekpic = dB.get_var(cq.from_user.id, "HELP_PIC")
    costum_cq = cq.edit_message_caption if cekpic else cq.edit_message_text
    costum_text = "caption" if cekpic else "text"
    kb = ikb([[("⪻", "bace.markd")]])
    if cmd == "butformat":
        try:
            return await costum_cq(
                **{costum_text: mark_1}, reply_markup=kb, parse_mode=ParseMode.MARKDOWN
            )
        except MediaCaptionTooLong:
            return await c.send_message(
                cq.from_user.id, mark_1, parse_mode=ParseMode.MARKDOWN
            )
    elif cmd == "filing":
        return await costum_cq(
            **{costum_text: mark_2},
            reply_markup=kb,
            parse_mode=ParseMode.HTML,
        )


@zb.callback("^bace.")
async def cb_bace(c, cq, _):
    txt = _("mark_3")
    cekpic = dB.get_var(cq.from_user.id, "HELP_PIC")
    costum_cq = cq.edit_message_caption if cekpic else cq.edit_message_text
    costum_text = "caption" if cekpic else "text"
    return await costum_cq(**{costum_text: txt}, reply_markup=markdown_help())
