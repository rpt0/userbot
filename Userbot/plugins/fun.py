import random

from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "Fake"


def help_string(org):
    return h_s(org, "help_func")


@zb.ubot("gben")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        if len(m.command) > 1:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(80, 800)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn}<b>Laporan Global Banned :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal}<b>Gagal : `{gagal}` grup.</b>"
            )
            if alasan:
                report_message += f"\n\n<b>{em.block}Alasan : `{alasan}`</b>"
            return await pros.edit(report_message)
        else:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(80, 800)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn}<b>Laporan Global Banned :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal}<b>Gagal : `{gagal}` grup.</b>"
            )
            return await pros.edit(report_message)
    except Exception as e:
        return await pros.edit(
            f"{em.gagal}Gagal membuat laporan Global Banned: {str(e)}"
        )


@zb.ubot("gmut")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        if len(m.command) > 1:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(80, 800)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn}<b>Laporan Global Mute :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal}<b>Gagal : `{gagal}` grup.</b>"
            )
            if alasan:
                report_message += f"\n\n<b>{em.block}Alasan : `{alasan}`</b>"
            return await pros.edit(report_message)
        else:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(80, 800)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn}<b>Laporan Global Mute :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal}<b>Gagal : `{gagal}` grup.</b>"
            )
            return await pros.edit(report_message)
    except Exception as e:
        return await pros.edit(f"{em.gagal}Gagal membuat laporan Global Mute: {str(e)}")


@zb.ubot("gkik")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        if len(m.command) > 1:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(80, 800)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn}<b>Laporan Global Kick :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal}<b>Gagal : `{gagal}` grup.</b>"
            )
            if alasan:
                report_message += f"\n<b>{em.block}Alasan : `{alasan}`</b>"
            return await pros.edit(report_message)
        else:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(80, 800)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn}<b>Laporan Global Kick :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal}<b>Gagal : `{gagal}` grup.</b>"
            )
            if alasan:
                report_message += f"\n<b>{em.block}Alasan : `{alasan}`</b>"
            return await pros.edit(report_message)
    except Exception as e:
        return await pros.edit(f"{em.gagal}Gagal membuat laporan Global Kick: {str(e)}")


@zb.ubot("ftf")
async def _(c, m, _):
    em = Emojik(c)
    em.initialize()
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(c)
    pros = await m.reply(_("proses").format(em.proses, proses_))
    try:
        rep = m.reply_to_message
        if not rep and len(m.command) < 2:
            await pros.edit(
                f"{em.gagal}Mohon balas pesan pengguna atau berikan username dan nominal sebagai argumen."
            )
            return

        if rep:
            nominal = (
                m.command[1].replace(".", "")
                if len(m.command) > 1
                else str(random.randint(100000, 50000000))
            )
            pengguna, _ = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            formatted_nominal = "{:,.0f}".format(int(nominal)).replace(",", ".")
            report_message = (
                f"{em.warn}<b>Laporan Transfer :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Nominal : Rp {formatted_nominal},-</b>\n"
            )
            return await pros.edit(report_message)
        else:
            nominal = m.command[1].replace(".", "")
            pengguna, _ = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            formatted_nominal = "{:,.0f}".format(int(nominal)).replace(",", ".")
            report_message = (
                f"{em.warn}<b>Laporan Transfer :</b>\n\n"
                f"{em.profil}<b>Pengguna : {mention}</b>\n"
                f"{em.sukses}<b>Nominal : Rp {formatted_nominal},-</b>\n"
            )
            return await pros.edit(report_message)
    except Exception as e:
        return await pros.edit(f"{em.gagal}Gagal membuat laporan Transfer: {str(e)}")
