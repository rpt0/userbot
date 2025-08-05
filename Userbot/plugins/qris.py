#
#
# by @hiyaok ON TG
# UPDATE SOURCE CHAT @hiyaok TELEGRAM
import asyncio
import time
import os
import requests
import qrcode
import uuid
from datetime import datetime
from bs4 import BeautifulSoup

from Userbot.helper.tools import Emojik, h_s, initial_ctext, zb

__MODULES__ = "QrisPayment"

def help_string(org):
    return h_s(org, "help_qris")

# Data OrderKuota
MERCHANT_ID = "OK1174104"
API_KEY = "513021717379960191174104OKCT8B1C2E06B64BACA29A563DF92055DFB1"
CODE_QR = "00020101021126670016COM.NOBUBANK.WWW01189360050300000879140214615534398557520303UMI51440014ID.CO.QRIS.WWW0215ID20232690040570303UMI5204481253033605802ID5920BOYS STORE OK11741046007SUMENEP61056941262070703A016304FC48"

# URL API Mutasi
API_URL_MUTASI = f"https://gateway.okeconnect.com/api/mutasi/qris/{MERCHANT_ID}/{API_KEY}"

# Active transactions tracking
active_transactions = {}

# Generate unique reference ID
def generate_reference_id():
    return str(uuid.uuid4())[:12]

# CRC16 calculation function
def convert_crc16(string):
    """Implementasi Python dari fungsi ConvertCRC16 PHP"""
    crc = 0xFFFF
    for c in string:
        crc ^= ord(c) << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    
    hex_value = format(crc & 0xFFFF, 'X')
    if len(hex_value) == 3:
        hex_value = "0" + hex_value
    
    return hex_value

# Function untuk modifikasi kode QRIS menjadi dinamis
def modify_qris_code(qris_code, amount):
    """Mengubah QRIS statis menjadi dinamis dengan nominal"""
    # Hapus 4 karakter terakhir (CRC16 checksum)
    qris_without_crc = qris_code[:-4]
    
    # Ubah dari statis ke dinamis
    step1 = qris_without_crc.replace("010211", "010212")
    
    # Split pada 5802ID
    if "5802ID" not in step1:
        raise ValueError("Format QRIS tidak valid: Tidak ditemukan marker '5802ID'")
    
    parts = step1.split("5802ID")
    
    # Format tag nominal
    amount_str = str(int(amount))  # Pastikan tanpa desimal
    amount_tag = "54" + str(len(amount_str)).zfill(2) + amount_str
    
    # Tambahkan 5802ID kembali ke tag
    amount_tag_with_id = amount_tag + "5802ID"
    
    # Gabungkan bagian-bagian
    combined = parts[0] + amount_tag_with_id + parts[1]
    
    # Hitung dan tambahkan CRC16
    combined_with_crc = combined + convert_crc16(combined)
    
    return combined_with_crc

# Function untuk menghapus file QRIS
def cleanup_qris_file(filename):
    """Menghapus file QRIS yang tidak diperlukan lagi"""
    try:
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print(f"Error deleting file {filename}: {str(e)}")

async def qris_cmd(client, message, _, em):
    # Ambil nominal dan timeout dari pesan
    args = message.text.split()
    
    # Validasi format perintah
    if len(args) < 2 or not args[1].isdigit():
        return await message.reply(f"{em.gagal}<b>Format salah! Gunakan: <code>.qris [nominal] [timeout_menit?]</code></b>")
    
    # Ambil nominal
    nominal = int(args[1])
    
    # Ambil timeout jika ada, default 5 menit
    timeout_minutes = 5
    if len(args) >= 3 and args[2].isdigit():
        timeout_minutes = int(args[2])
        # Batasi timeout antara 1-60 menit
        timeout_minutes = max(1, min(60, timeout_minutes))
    
    # Catat waktu mulai untuk perhitungan waktu
    start_time = time.time()
    start_datetime = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
    reference_id = generate_reference_id()
    
    # Pesan awal untuk proses
    pong_, uptime_, owner_, ubot_, proses_, sukses_ = initial_ctext(client)
    process_msg = await message.reply(f"{em.proses}<b>Membuat QRIS...</b>")
    
    try:
        # Modifikasi kode QRIS statis untuk menambahkan amount
        dynamic_qris_code = modify_qris_code(CODE_QR, nominal)
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(dynamic_qris_code)
        qr.make(fit=True)
        
        # Simpan QR ke file dengan nama unik berdasarkan waktu dan nominal
        qr_filename = f"qris_{nominal}_{reference_id}.png"
        img = qr.make_image(fill="black", back_color="white")
        img.save(qr_filename)
        
        # Update pesan dengan QR code dan informasi
        await process_msg.delete()
        qr_msg = await client.send_photo(
            message.chat.id,
            qr_filename,
            caption=f"{em.sukses}<b>QRIS BERHASIL DIBUAT</b>\n\n"
                    f"<b> {em.smile}Nominal:</b> Rp{nominal:,}\n"
                    f"<b>{em.clock} Waktu Pembuatan:</b> {start_datetime}\n"
                    f"<b>{em.timer} Timeout:</b> {timeout_minutes} menit\n\n"
                    f"<b>{em.hourglass} Menunggu pembayaran...</b>"
        )
        
        # Kirim pesan status pembayaran dengan emoji premium
        status_msg = await client.send_message(
            message.chat.id,
            f"{em.chat} Menunggu pembayaran...\n"
            f"{em.clock} Sisa waktu: {timeout_minutes} menit\n"
            f"{em.smile} Total Bayar: Rp{nominal}"
        )
        
        # Tambahkan ke daftar transaksi aktif
        transaction_id = f"{nominal}_{reference_id}"
        active_transactions[transaction_id] = {
            "qr_msg_id": qr_msg.id,
            "status_msg_id": status_msg.id,
            "chat_id": message.chat.id,
            "start_time": start_time,
            "nominal": nominal,
            "reference_id": reference_id
        }
        
        # Mulai cek pembayaran
        max_attempts = int(timeout_minutes * 60 / 10)  # 10 detik per percobaan
        attempt = 0
        payment_success = False
        
        while attempt < max_attempts and transaction_id in active_transactions and not payment_success:
            try:
                response = requests.get(API_URL_MUTASI)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Cari transaksi dengan tipe CR dan jumlah yang sesuai
                    if "data" in data and data["status"] == "success":
                        for transaction in data["data"]:
                            # Cek jika nominal sama, tipe CR, dan transaksi terjadi setelah pembuatan QRIS
                            if (transaction["type"] == "CR" and 
                                int(transaction["amount"]) == nominal and
                                transaction["date"] >= start_datetime and
                                transaction["qris"] in ["static", "dynamic"]):
                                
                                payment_success = True
                                
                                # Format waktu
                                payment_time = transaction["date"]
                                elapsed_time = int(time.time() - start_time)
                                
                                # Tangani penghapusan dan update pesan dalam blok try-except terpisah
                                try:
                                    # Hapus pesan QR
                                    await client.delete_messages(message.chat.id, qr_msg.id)
                                except Exception as e:
                                    print(f"Error deleting QR message: {str(e)}")
                                
                                try:
                                    # Update pesan status dengan info sukses dan emoji premium
                                    success_text = (
                                        f"{em.sukses} PEMBAYARAN BERHASIL\n\n"
                                        f"{em.smile} Nominal: Rp{nominal}\n"
                                        f"{em.coin} Metode Pembayaran: {transaction['brand_name']}\n"
                                        f"{em.receipt} Referensi: {reference_id}\n"
                                        f"{em.timer} Waktu Pembayaran: {payment_time}\n"
                                        f"{em.hourglass} Waktu Tunggu: {elapsed_time} detik"
                                    )
                                    
                                    # Coba edit pesan
                                    await client.edit_message_text(
                                        chat_id=message.chat.id,
                                        message_id=status_msg.id,
                                        text=success_text
                                    )
                                except Exception as e:
                                    print(f"Error updating status message: {str(e)}")
                                    # Jika gagal mengedit, coba kirim pesan baru
                                    try:
                                        await client.send_message(
                                            message.chat.id,
                                            f"{em.sukses} PEMBAYARAN BERHASIL\n\n"
                                            f"{em.smile} Nominal: Rp{nominal}\n"
                                            f"{em.coin} Metode Pembayaran: {transaction['brand_name']}\n"
                                            f"{em.receipt} Referensi: {reference_id}\n"
                                            f"{em.timer} Waktu Pembayaran: {payment_time}\n"
                                            f"{em.hourglass} Waktu Tunggu: {elapsed_time} detik"
                                        )
                                    except Exception as e2:
                                        print(f"Error sending new success message: {str(e2)}")
                                
                                # Hapus dari daftar transaksi aktif
                                if transaction_id in active_transactions:
                                    del active_transactions[transaction_id]
                                    
                                # Bersihkan file QR
                                cleanup_qris_file(qr_filename)
                                return
                
                # Tunggu 10 detik sebelum cek lagi
                await asyncio.sleep(10)
                attempt += 1
                
                # Sisa waktu dalam menit dan detik
                remaining_seconds = (max_attempts - attempt) * 10
                remaining_minutes = remaining_seconds // 60
                remaining_secs = remaining_seconds % 60
                
                # Update pesan status dengan jumlah percobaan dan sisa waktu menggunakan emoji premium
                try:
                    await client.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=status_msg.id,
                        text=f"{em.chat} Menunggu pembayaran...\n"
                            f"{em.clock} Sisa waktu: {remaining_minutes} menit {remaining_secs} detik\n"
                            f"{em.smile} Total Bayar: Rp{nominal}"
                    )
                except Exception as e:
                    print(f"Error updating countdown message: {str(e)}")
                
            except Exception as e:
                print(f"Error checking payment: {str(e)}")
                await asyncio.sleep(10)
                attempt += 1
        
        # Jika tidak ada pembayaran setelah batas maksimal
        if transaction_id in active_transactions and not payment_success:
            try:
                # Hapus pesan QR
                await client.delete_messages(message.chat.id, qr_msg.id)
            except Exception as e:
                print(f"Error deleting QR on timeout: {str(e)}")
            
            try:
                # Update pesan status dengan info gagal
                await client.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=status_msg.id,
                    text=f"{em.gagal} PEMBAYARAN GAGAL\n\n"
                        f"{em.smile} Nominal: Rp{nominal}\n"
                        f"{em.receipt} Referensi: {reference_id}"
                )
            except Exception as e:
                print(f"Error updating failed status message: {str(e)}")
                # Jika gagal edit, coba kirim pesan baru
                try:
                    await client.send_message(
                        message.chat.id,
                        f"{em.gagal} PEMBAYARAN GAGAL\n\n"
                        f"{em.smile} Nominal: Rp{nominal}\n"
                        f"{em.receipt} Referensi: {reference_id}"
                    )
                except Exception as e2:
                    print(f"Error sending new failure message: {str(e2)}")
            
            # Hapus dari daftar transaksi aktif
            if transaction_id in active_transactions:
                del active_transactions[transaction_id]
        
        # Bersihkan file QR
        cleanup_qris_file(qr_filename)
        
    except Exception as e:
        await process_msg.edit_text(f"{em.gagal}<b>Error: {str(e)}</b>")
        if 'transaction_id' in locals() and transaction_id in active_transactions:
            del active_transactions[transaction_id]
        if 'qr_filename' in locals():
            cleanup_qris_file(qr_filename)

# Command untuk membatalkan pembayaran yang sedang berlangsung
async def cancel_qris_cmd(client, message, _, em):
    """Batalkan pembayaran QRIS yang sedang aktif"""
    # Periksa apakah ada transaksi aktif
    user_transactions = []
    for transaction_id, transaction_data in active_transactions.items():
        if transaction_data["chat_id"] == message.chat.id:
            user_transactions.append((transaction_id, transaction_data))
    
    if not user_transactions:
        return await message.reply(f"{em.gagal}<b>Tidak ada pembayaran QRIS aktif.</b>")
    
    # Jika hanya ada satu transaksi, batalkan langsung
    if len(user_transactions) == 1:
        transaction_id, transaction_data = user_transactions[0]
        
        try:
            # Hapus pesan QR
            await client.delete_messages(
                message.chat.id, 
                transaction_data["qr_msg_id"]
            )
        except Exception as e:
            print(f"Error deleting QR on cancel: {str(e)}")
        
        try:
            # Update pesan status
            await client.edit_message_text(
                chat_id=message.chat.id,
                message_id=transaction_data["status_msg_id"],
                text=f"{em.gagal} PEMBAYARAN DIBATALKAN\n\n"
                    f"{em.smile} Nominal: Rp{transaction_data['nominal']}\n"
                    f"{em.receipt} Referensi: {transaction_data['reference_id']}"
            )
        except Exception as e:
            print(f"Error updating cancel message: {str(e)}")
            # Jika gagal edit, coba kirim pesan baru
            try:
                await client.send_message(
                    message.chat.id,
                    f"{em.gagal} PEMBAYARAN DIBATALKAN\n\n"
                    f"{em.smile} Nominal: Rp{transaction_data['nominal']}\n"
                    f"{em.receipt} Referensi: {transaction_data['reference_id']}"
                )
            except Exception as e2:
                print(f"Error sending new cancel message: {str(e2)}")
        
        # Hapus dari daftar transaksi aktif
        del active_transactions[transaction_id]
        
        # Hapus file QR jika masih ada
        qr_filename = f"qris_{transaction_data['nominal']}_{transaction_data['reference_id']}.png"
        cleanup_qris_file(qr_filename)
        
        return await message.reply(f"{em.sukses}<b>Pembayaran QRIS berhasil dibatalkan.</b>")
    
    # Jika ada lebih dari satu, beri pilihan
    text = f"{em.warn}<b>Ditemukan {len(user_transactions)} pembayaran aktif. Silakan batalkan dengan:</b>\n\n"
    for i, (transaction_id, transaction_data) in enumerate(user_transactions, 1):
        elapsed_time = int(time.time() - transaction_data["start_time"])
        text += f"<b>{i}. Rp{transaction_data['nominal']} - {elapsed_time} detik lalu</b>\n"
        text += f"   <code>.qriscancel {transaction_id}</code>\n\n"
    
    await message.reply(text)

# Command untuk cek status transaksi
async def check_qris_status_cmd(client, message, _, em):
    """Cek status pembayaran QRIS yang aktif"""
    # Periksa apakah ada transaksi aktif
    user_transactions = []
    for transaction_id, transaction_data in active_transactions.items():
        if transaction_data["chat_id"] == message.chat.id:
            user_transactions.append((transaction_id, transaction_data))
    
    if not user_transactions:
        return await message.reply(f"{em.sukses}<b>Tidak ada pembayaran QRIS aktif.</b>")
    
    # Tampilkan semua transaksi aktif
    text = f"{em.sukses}<b>Status Pembayaran QRIS Aktif:</b>\n\n"
    for i, (transaction_id, transaction_data) in enumerate(user_transactions, 1):
        elapsed_time = int(time.time() - transaction_data["start_time"])
        elapsed_minutes = elapsed_time // 60
        elapsed_seconds = elapsed_time % 60
        
        text += f"<b>{i}. Nominal:</b> Rp{transaction_data['nominal']}\n"
        text += f"<b>   Referensi:</b> {transaction_data['reference_id']}\n"
        text += f"<b>   Waktu Berlalu:</b> {elapsed_minutes} menit {elapsed_seconds} detik\n\n"
    
    await message.reply(text)

# Command implementasi utama
@zb.ubot("qris|qriscancel|qrisstatus")
@zb.thecegers
async def _(client, message, _):
    em = Emojik(client)
    em.initialize()
    
    cmd = message.command[0].lower()
    
    if cmd == "qris":
        return await qris_cmd(client, message, _, em)
    elif cmd == "qriscancel":
        return await cancel_qris_cmd(client, message, _, em)
    elif cmd == "qrisstatus":
        return await check_qris_status_cmd(client, message, _, em)
