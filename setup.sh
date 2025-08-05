sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y --no-install-recommends \
    ffmpeg git neofetch apt-utils libmediainfo0v5 \
    libgl1-mesa-glx libglib2.0-0 fonts-noto-color-emoji python3-venv python3-pip sqlite3 net-tools lsof
    
sudo apt-get clean
sudo rm -rf /var/lib/apt/lists/*

ulimit -n 100000

echo "Menetapkan ulimit -n menjadi 100000"

LIMITS_CONF="/etc/security/limits.conf"
echo "root soft nofile 100000" | sudo tee -a $LIMITS_CONF
echo "root hard nofile 100000" | sudo tee -a $LIMITS_CONF
echo "Batasan telah ditambahkan ke $LIMITS_CONF"

SYSTEMD_CONF="/etc/systemd/system.conf"
USER_CONF="/etc/systemd/user.conf"

echo "DefaultLimitNOFILE=100000" | sudo tee -a $SYSTEMD_CONF
echo "DefaultLimitNPROC=100000" | sudo tee -a $SYSTEMD_CONF

echo "DefaultLimitNOFILE=100000" | sudo tee -a $USER_CONF
echo "DefaultLimitNPROC=100000" | sudo tee -a $USER_CONF

echo "Batasan telah ditambahkan ke konfigurasi systemd."

echo "Restarting systemd to apply changes..."
sudo systemctl daemon-reexec

echo "Konfigurasi selesai. Silakan reboot agar perubahan diterapkan sepenuhnya."