import os
import textwrap
from tinydb import TinyDB, Query
from PIL import Image, ImageDraw, ImageFont
from Userbot.helper.tools import zb
from pyrogram.types import Message

DB_PATH = os.path.join(os.getcwd(), "bratvid_settings.json")
db = TinyDB(DB_PATH)
UserQ = Query()
TEMP_DIR = os.path.join(os.getcwd(), "lib")
os.makedirs(TEMP_DIR, exist_ok=True)

COLOR_MAP = {
    "black": (0, 0, 0), "white": (255, 255, 255), "pink": (255, 192, 203),
    "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "gray": (128, 128, 128), "purple": (128, 0, 128),
    "orange": (255, 165, 0), "brown": (165, 42, 42), "cyan": (0, 255, 255),
    "lime": (50, 205, 50), "indigo": (75,0,130), "gold": (255, 215, 0),
    "navy": (0, 0, 128), "maroon": (128, 0, 0)
}

FONT_DIR = os.path.join(os.getcwd(), "Userbot", "font")

def generate_font_map():
    font_map = {}
    if not os.path.exists(FONT_DIR):
        raise Exception(f"Folder font '{FONT_DIR}' tidak ditemukan.")
    for fname in os.listdir(FONT_DIR):
        if fname.lower().endswith(".ttf"):
            basename = fname.rsplit('.', 1)[0]
            kode = ''.join([w[:2] for w in basename.replace("_", "-").split('-')])[:8].lower()
            original_kode = kode
            i = 2
            while kode in font_map:
                kode = f"{original_kode}{i}"
                i += 1
            display = basename.replace('-', ' ').replace('_', ' ').title()
            font_map[kode] = (display, fname)
    return font_map

FONT_MAP = generate_font_map()

ANIM_OPTIONS = [
    "none", "fade", "typewriter", "slide", "zoom", "bounce",
    "spin", "grow", "shake", "wave"
]
STYLE_OPTIONS = ["none", "bold", "italic", "underline", "shadow", "outline"]

DEFAULT_SETTINGS = {
    "anim": "none",
    "font": next(iter(FONT_MAP.keys()), ""),
    "warna": "black",
    "style": "none"
}

def get_user_settings(user_id):
    user = db.get(UserQ.user_id == user_id)
    if user:
        return user["settings"]
    db.upsert({"user_id": user_id, "settings": DEFAULT_SETTINGS.copy()}, UserQ.user_id == user_id)
    return DEFAULT_SETTINGS.copy()

def set_user_settings(user_id, key, value):
    settings = get_user_settings(user_id)
    settings[key] = value
    db.upsert({"user_id": user_id, "settings": settings}, UserQ.user_id == user_id)

def reset_user_settings(user_id):
    db.upsert({"user_id": user_id, "settings": DEFAULT_SETTINGS.copy()}, UserQ.user_id == user_id)

def show_user_settings(user_id):
    settings = get_user_settings(user_id)
    font_disp = FONT_MAP.get(settings['font'], ("?",))[0]
    text = (
        f"📺 <b>BratVid Setting Anda:</b>\n"
        f"- <b>Animasi:</b> {settings['anim']}\n"
        f"- <b>Font:</b> {font_disp} ({settings['font']})\n"
        f"- <b>Warna:</b> {settings['warna']}\n"
        f"- <b>Style:</b> {settings['style']}\n"
        f"\nGunakan <code>.bratvidset help</code> untuk bantuan."
    )
    return text

def get_font_help():
    return " | ".join([f"{k}={v[0]}" for k, v in sorted(FONT_MAP.items())])

HELP_TEXT = f"""
<b>BratVidSet Menu</b>
Command untuk mengatur preferensi .brattvid.

<b>Cara Pakai:</b>
<code>.bratvidset [opsi] [value]</code>

<b>Opsi:</b>
- <b>anim</b> [pilihan]   : Animasi teks
   Pilihan: {', '.join(ANIM_OPTIONS)}
- <b>font</b> [kode]      : Font teks, kode:
   {get_font_help()}
- <b>warna</b> [pilihan]  : Warna background
   Pilihan: {', '.join(COLOR_MAP.keys())}
- <b>style</b> [pilihan]  : Style teks
   Pilihan: {', '.join(STYLE_OPTIONS)}
- <b>reset</b>            : Reset semua setting
- <b>show</b>             : Tampilkan setting aktif
- <b>help</b>             : Menu bantuan ini

<b>Contoh:</b>
<code>.bratvidset anim fade</code>
<code>.bratvidset font anbo</code>
<code>.bratvidset warna gold</code>
<code>.bratvidset style outline</code>
<code>.bratvidset show</code>
<code>.bratvidset reset</code>

<b>Note:</b>
- Untuk background: reply ke gambar/sticker otomatis jadi background. Jika tidak, pakai warna setting.
- Setting tersimpan per user.
"""

@zb.ubot("bratvidset")
async def bratvidset_handler(client, message: Message, *args):
    user_id = message.from_user.id
    params = message.text.split(maxsplit=2)
    if len(params) < 2 or params[1] == "help":
        await message.reply_text(HELP_TEXT)
        return
    #@moire_mor
    opsi = params[1].lower()
    value = params[2].strip().lower() if len(params) > 2 else ""

    if opsi == "anim":
        if value not in ANIM_OPTIONS:
            await message.reply_text(f"Animasi tidak valid!\nPilihan: {', '.join(ANIM_OPTIONS)}")
            return
        set_user_settings(user_id, "anim", value)
        await message.reply_text(f"Animasi di-set ke <b>{value}</b>!")

    elif opsi == "font":
        if value not in FONT_MAP:
            await message.reply_text("Font tidak valid!\nGunakan salah satu kode: " + ", ".join(FONT_MAP.keys()))
            return
        set_user_settings(user_id, "font", value)
        await message.reply_text(f"Font di-set ke <b>{FONT_MAP[value][0]}</b> ({value})!")

    elif opsi == "warna":
        if value not in COLOR_MAP:
            await message.reply_text(f"Warna tidak valid!\nPilihan: {', '.join(COLOR_MAP.keys())}")
            return
        set_user_settings(user_id, "warna", value)
        await message.reply_text(f"Warna di-set ke <b>{value}</b>!")

    elif opsi == "style":
        if value not in STYLE_OPTIONS:
            await message.reply_text(f"Style tidak valid!\nPilihan: {', '.join(STYLE_OPTIONS)}")
            return
        set_user_settings(user_id, "style", value)
        await message.reply_text(f"Style di-set ke <b>{value}</b>!")

    elif opsi == "reset":
        reset_user_settings(user_id)
        await message.reply_text("Semua setting berhasil di-reset ke default.")

    elif opsi == "show":
        await message.reply_text(show_user_settings(user_id))

    else:
        await message.reply_text("Opsi tidak dikenali! Gunakan <code>.bratvidset help</code>.")

def get_color(keyword):
    return COLOR_MAP.get(keyword.lower(), (30, 30, 30))

def get_font(fontkey):
    """
    Mengembalikan path font .ttf lokal yang valid, sesuai dengan yang dipilih user.
    Bila gagal, raise Exception.
    """
    fontinfo = FONT_MAP.get(fontkey)
    if not fontinfo:
        raise Exception(f"Font '{fontkey}' tidak ditemukan di daftar FONT_MAP. Cek kode font di .bratvidset help")
    fname, ffile = fontinfo
    font_path = os.path.join(FONT_DIR, ffile)
    if not os.path.exists(font_path):
        raise Exception(f"File font '{ffile}' tidak ditemukan di folder Userbot/font.")
    try:
        ImageFont.truetype(font_path, 12)
        return font_path
    except Exception as e:
        raise Exception(f"Font '{fname}' gagal dipakai: {e}")

async def BratVideo(
    text, bg_color="black",
    anim="none",
    font_key=None,
    style="none",
    bg_img_path=None
):
    if not text:
        return "textnya mana?"
    if len(text) > 350:
        return "teks terlalu panjang!"

    temp_dir = TEMP_DIR
    frame_paths = []

    try:
        font_path = get_font(font_key)
    except Exception as e:
        return f"Terjadi kesalahan: {e}"

    font_size = 48
    frame_width, frame_height = 720, 480
    color = get_color(bg_color)

    try:
        words = text.split()
        anim = anim.lower()
        style = style.lower()
        if anim == "typewriter":
            frames_range = range(len(text))
        else:
            frames_range = range(len(words))

        for i in frames_range:
            if anim == "typewriter":
                current_text = text[:i+1]
            else:
                current_text = " ".join(words[:i+1])

            font = ImageFont.truetype(font_path, font_size)
            if bg_img_path and os.path.exists(bg_img_path):
                bg_img = Image.open(bg_img_path).convert("RGB").resize((frame_width, frame_height))
                draw_img = bg_img.copy()
            else:
                draw_img = Image.new("RGB", (frame_width, frame_height), color=color)

            draw = ImageDraw.Draw(draw_img)

            max_chars_per_line = 22
            wrapped_text = textwrap.fill(current_text, width=max_chars_per_line)
            w, h = draw.multiline_textsize(wrapped_text, font=font)
            fs = font_size
            while h > frame_height - 40 and fs > 10:
                fs -= 2
                font = ImageFont.truetype(font_path, fs)
                w, h = draw.multiline_textsize(wrapped_text, font=font)

            x = (frame_width - w) / 2
            y = (frame_height - h) / 2

            main_color = (255, 255, 255) if color != (255,255,255) else (0,0,0)
            if style in ["shadow", "outline"]:
                draw.multiline_text((x+2, y+2), wrapped_text, font=font, fill=(0,0,0), align="center")
            if style == "outline":
                for dx in [-2,2]: draw.multiline_text((x+dx, y), wrapped_text, font=font, fill=(0,0,0), align="center")
                for dy in [-2,2]: draw.multiline_text((x, y+dy), wrapped_text, font=font, fill=(0,0,0), align="center")
            if style == "bold":
                draw.multiline_text((x+1, y), wrapped_text, font=font, fill=main_color, align="center")
            if style == "underline":
                draw.line((x, y+h+3, x+w, y+h+3), fill=main_color, width=3)

            img = draw_img
            if anim == "fade":
                alpha = int(255 * (i+1) / len(frames_range))
                overlay = Image.new("RGBA", (frame_width, frame_height), (0,0,0,0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.multiline_text((x, y), wrapped_text, font=font, fill=main_color+(alpha,), align="center")
                img = Image.alpha_composite(draw_img.convert("RGBA"), overlay).convert("RGB")
            elif anim == "slide":
                slide_x = int((frame_width - w) * (1 - (i+1)/len(frames_range)))
                img = draw_img.copy()
                slide_draw = ImageDraw.Draw(img)
                slide_draw.multiline_text((slide_x, y), wrapped_text, font=font, fill=main_color, align="center")
            elif anim == "zoom":
                scale = 0.5 + 0.5*(i+1)/len(frames_range)
                zoom_fs = int(fs * scale)
                zoom_font = ImageFont.truetype(font_path, zoom_fs)
                zw, zh = draw.multiline_textsize(wrapped_text, font=zoom_font)
                zx = (frame_width-zw)/2
                zy = (frame_height-zh)/2
                img = draw_img.copy()
                zoom_draw = ImageDraw.Draw(img)
                zoom_draw.multiline_text((zx, zy), wrapped_text, font=zoom_font, fill=main_color, align="center")
            elif anim == "bounce":
                import math
                bounce_y = y + 30 * abs(math.sin(3.14*(i+1)/len(frames_range)))
                img = draw_img.copy()
                bounce_draw = ImageDraw.Draw(img)
                bounce_draw.multiline_text((x, bounce_y), wrapped_text, font=font, fill=main_color, align="center")
            elif anim == "spin":
                angle = 360 * (i+1) / len(frames_range)
                img = draw_img.copy()
                text_img = Image.new("RGBA", (frame_width, frame_height), (0,0,0,0))
                text_draw = ImageDraw.Draw(text_img)
                text_draw.multiline_text((x, y), wrapped_text, font=font, fill=main_color+(255,), align="center")
                img = Image.alpha_composite(img.convert("RGBA"), text_img.rotate(angle, resample=Image.BICUBIC)).convert("RGB")
            elif anim == "grow":
                scale = (i+1)/len(frames_range)
                grow_fs = int(10 + fs * scale)
                grow_font = ImageFont.truetype(font_path, grow_fs)
                gw, gh = draw.multiline_textsize(wrapped_text, font=grow_font)
                gx = (frame_width-gw)/2
                gy = (frame_height-gh)/2
                img = draw_img.copy()
                grow_draw = ImageDraw.Draw(img)
                grow_draw.multiline_text((gx, gy), wrapped_text, font=grow_font, fill=main_color, align="center")
            elif anim == "shake":
                import random
                shake_x = x + random.randint(-5,5)
                shake_y = y + random.randint(-5,5)
                img = draw_img.copy()
                shake_draw = ImageDraw.Draw(img)
                shake_draw.multiline_text((shake_x, shake_y), wrapped_text, font=font, fill=main_color, align="center")
            elif anim == "wave":
                img = draw_img.copy()
                wave_draw = ImageDraw.Draw(img)
                base_y = y
                for idx, ch in enumerate(wrapped_text):
                    ch_font = font
                    ch_x = x + draw.textsize(wrapped_text[:idx], font=font)[0]
                    ch_y = base_y + 10 * math.sin((i+1)/len(frames_range)*3.14*2 + idx)
                    wave_draw.text((ch_x, ch_y), ch, font=ch_font, fill=main_color)
            else:
                draw.multiline_text((x, y), wrapped_text, font=font, fill=main_color, align="center")

            frame_path = os.path.join(temp_dir, f"frame{i}.png")
            img.save(frame_path)
            frame_paths.append(frame_path)

        file_list_path = os.path.join(temp_dir, "filelist.txt")
        with open(file_list_path, "w") as f:
            for frame in frame_paths:
                f.write(f"file '{frame}'\n")
                f.write("duration 0.7\n")
            f.write(f"file '{frame_paths[-1]}'\n")
            f.write("duration 2\n")

        output_video_path = os.path.join(temp_dir, "output.mp4")
        os.system(
            f"ffmpeg -y -f concat -safe 0 -i {file_list_path} -vf 'fps=30,format=yuv420p' -c:v libx264 -preset ultrafast {output_video_path}"
        )

        for frame in frame_paths:
            if os.path.exists(frame):
                os.remove(frame)
        if os.path.exists(file_list_path):
            os.remove(file_list_path)
        if bg_img_path and os.path.exists(bg_img_path) and "bratvid_bg" in bg_img_path:
            os.remove(bg_img_path)
        return output_video_path

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Terjadi kesalahan: {e}"

@zb.ubot("bratvid")
async def brat_handler(client, message: Message, *args):
    user_id = message.from_user.id
    settings = get_user_settings(user_id)
    anim = settings.get("anim", "none")
    font_key = settings.get("font", next(iter(FONT_MAP.keys()), ""))
    warna = settings.get("warna", "black")
    style = settings.get("style", "none")

    params = message.text.split(maxsplit=1)
    text = None
    bg_img_path = None
    bg_color = warna

    if message.reply_to_message:
        if message.reply_to_message.photo:
            bg_img = await message.reply_to_message.download()
            bg_img_path = bg_img
        elif message.reply_to_message.sticker:
            bg_img = await message.reply_to_message.download()
            if bg_img.endswith(".webp"):
                from PIL import Image as PILImage
                im = PILImage.open(bg_img).convert("RGB")
                temp_bg = os.path.join(TEMP_DIR, "bratvid_bg.png")
                im.save(temp_bg)
                os.remove(bg_img)
                bg_img_path = temp_bg
            else:
                bg_img_path = bg_img

    if len(params) > 1:
        text = params[1]
    else:
        if message.reply_to_message and message.reply_to_message.text:
            text = message.reply_to_message.text
    if not text:
        await message.reply_text("Format: <code>.bratvid &lt;text&gt;</code> atau reply ke gambar+teks.")
        return

    processing_msg = await message.reply_text("proses...")
    video_path = await BratVideo(
        text,
        bg_color=bg_color,
        anim=anim,
        font_key=font_key,
        style=style,
        bg_img_path=bg_img_path
    )

    if isinstance(video_path, str) and video_path.startswith("Terjadi kesalahan"):
        await processing_msg.delete()
        await message.reply_text(video_path)
    else:
        await processing_msg.delete()
        await message.reply_video(video=video_path, caption="```\ndone```")
        if os.path.exists(video_path):
            os.remove(video_path)
