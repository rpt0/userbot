from pyrogram import Client, filters
import random
from Userbot.helper.tools import Emojik, h_s, zb
from Userbot import nlx

__MODULES__ = "CekCantik"

def help_string(org):
    return h_s(org, "help_cekcantik")


def emoji(alias):
    emojis = {
        "DETEK": "<emoji id=6026321200597176575>🃏</emoji>",    
        "SUBJEK": "<emoji id=5251365214699408742>🧜‍♀️</emoji>",
        "ANALISIS": "<emoji id=4956680567853679460>💋</emoji>",
        "ANALISISA": "<emoji id=5251634899990897163>💎</emoji>",        
        "KODAM": "<emoji id=5461151522177965764>🎁</emoji>", 
        "ENERGY": "<emoji id=5296645049151417006>🎁</emoji>",                   
    }
    return emojis.get(alias, "⎆.")


dtk = emoji("DETEK")
subj = emoji("SUBJEK")
anal = emoji("ANALISIS")
anala = emoji("ANALISISA")
kdm = emoji("KODAM")
engy = emoji("ENERGY")


KHODAM_LIST = [
    "kreativitas, kemampuan beradaptasi, dan antusiasme tinggi.",
    "mudah bergaul, menyukai hal-hal baru, dan memiliki jiwa yang bebas.",
    "memiliki jiwa yang ceria, pandai berkomunikasi, dan sangat tertarik untuk belajar hal-hal baru.",
    "karakter yang positif dan energik, membuat mereka sering dianggap inspiratif bagi orang lain.",
    "keseimbangan, kedamaian, dan kasih sayang",
    "kedamaian batin, kejujuran, dan kebijaksanaan.",
    "spiritualitas yang tinggi dan kemampuan untuk merasakan ikatan mendalam dengan alam sekitar.",
    "intuisi tinggi, kreativitas, dan kesadaran spiritual yang mendalam.",
    "jiwa seni yang kuat, bijaksana, dan memiliki ikatan yang kuat dengan alam dan hal-hal spiritual.",
    "lambang kemurnian, kedamaian batin, dan perlindungan spiritual yang tinggi.",
    "karakter yang tenang, damai, dan terbebas dari konflik.",
    "ketidakseimbangan atau perasaan berat yang membebani pikiran dan emosi seseorang.",
    "orang yang menghargai proses pengasahan pengetahuan faktual yang empiris dan disiplin.",
    "emosional dan psikis lebih membumi atau seimbang.",
    "kreativitas dan energi seksual.",
    "pikiran yang sangat cepat dan cenderung perfeksionis serta mudah cemas.",
    "seseorang yang bahagia dan harmonis dengan orang-orang di sekitarnya.",
    "emosi yang kuat seperti kemarahan, cinta, dan kesombongan.",
    "sangat intuitif, dan condong ke disiplin yang melibatkan interaksi manusia.",
    "brilian dan bisa membuat seseorang menjadi eksentrik.",
    "orang yang kompetitif secara atletik dan sukses di bidang kinerja pribadi.",
    "kepribadian untuk berjuang dengan aspek kehidupan logis dan metodis.",
]

ENERGY_STATUS_LIST = [
    "Merah 🟥", 
    "Jingga 🟧", 
    "Kuning 🟨", 
    "Hijau 🟩", 
    "Biru 🟦", 
    "Ungu 🟪", 
    "Putih ⬜",
    "Hitam ⬛",
    "Coklat 🟫",              
]

@zb.ubot("ccantik")
async def _(client, message, *args):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user = await client.get_users(message.command[1])
    else:
        user = message.from_user
    
    if user:
        username = f"@{user.username}" if user.username else user.first_name
        energy_percent = random.randint(10, 100)
        aura_percent = random.randint(10, 100)
        khodam = random.choice(KHODAM_LIST)
        energy_status = random.choice(ENERGY_STATUS_LIST)

        response = f"""
<blockquote>**__{dtk} **Deteksi Kecantikan Aktif** {dtk}

{subj} **Subjek**: {username}
{anal} **Analisis Kecantikan**: [{energy_percent}%] {"█" * (energy_percent // 10)}
{anala} **Analisis Aura**: [{aura_percent}%] {"█" * (aura_percent // 10)}
{kdm} **Energy Aura**: {khodam}

{engy} **Warna Aura**: {energy_status}__**</blockquote>
"""
        await message.reply_text(response)
    else:
        await message.reply_text("⛔ **Gagal mendeteksi pengguna...**")
