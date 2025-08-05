function log_info() {
  echo -e "\033[1;32m[INFO]: $1\033[0m"
}

function log_error() {
  echo -e "\033[1;31m[ERROR]: $1\033[0m"
}

log_info "Mulai proses pembersihan penggunaan CPU..."

top_processes=$(ps -eo pid,%cpu,cmd --sort=-%cpu | head -n 10)

log_info "Proses dengan penggunaan CPU tinggi:"
echo "$top_processes"

echo "$top_processes" | while read -r pid cpu cmd; do
if [[ "$pid" =~ ^[0-9]+$ ]]; then
log_info "Menghentikan proses PID: $pid ($cmd) dengan penggunaan CPU: $cpu%"
kill -9 "$pid" 2>/dev/null
if [[ $? -eq 0 ]]; then
log_info "Proses PID: $pid berhasil dihentikan."
else
log_error "Gagal menghentikan proses PID: $pid."
fi
fi
done

log_info "Pembersihan selesai. Penggunaan CPU telah dikurangi."