import time
import subprocess
import re
import sys
import os

# Yapılandırma
MAX_FAILURES = 3  # Ban eşiği
CHECK_INTERVAL = 1  # Saniye cinsinden kontrol aralığı
LOG_FILE = "/var/log/auth.log"
WHITELISTED_IPS = {"127.0.0.1", "::1", "212.12.134.18"}  # Bu IP'ler asla banlanmayacak

# Hafıza
failed_attempts = {}
banned_ips = set()

def ban_ip(ip_address):
    """Belirtilen IP adresini iptables ile engeller."""
    if ip_address in banned_ips:
        return

    print(f"[!] {ip_address} için ban işlemi başlatılıyor (Eşik: {MAX_FAILURES} deneme)...")
    
    # iptables komutu: Gelen bağlantıları engelle
    command = f"iptables -A INPUT -s {ip_address} -j DROP"
    
    try:
        # Komutu çalıştır
        subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[+] {ip_address} başarıyla engellendi.")
        banned_ips.add(ip_address)
    except subprocess.CalledProcessError as e:
        print(f"[-] Hata: {ip_address} engellenemedi. Root yetkisi var mı?")

def monitor_events():
    print(f"[*] Örümcek Koruması Başlatıldı (Linux Modu).")
    print(f"[*] Hedef Log Dosyası: {LOG_FILE}")
    print(f"[*] Ban Eşiği: {MAX_FAILURES} deneme")
    
    if not os.path.exists(LOG_FILE):
        print(f"[-] Log dosyası bulunamadı: {LOG_FILE}")
        return

    if os.geteuid() != 0:
        print("[-] Lütfen programı ROOT olarak çalıştırın.")
        return

    # Dosyayı aç ve sonuna git
    try:
        f = open(LOG_FILE, 'r')
        f.seek(0, 2) # Dosyanın sonuna git
    except Exception as e:
        print(f"[-] Dosya açma hatası: {e}")
        return

    print("[*] İzleme modu aktif. Yeni olaylar bekleniyor...")

    while True:
        line = f.readline()
        if not line:
            time.sleep(CHECK_INTERVAL)
            continue
            
        # SSH başarısız giriş tespiti
        if "Failed password" in line:
            ip_match = re.search(r"from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
            if ip_match:
                ip_address = ip_match.group(1)
                
                if ip_address in WHITELISTED_IPS:
                    continue

                print(f"[*] Tespit: {ip_address} başarısız giriş yaptı.")
                failed_attempts[ip_address] = failed_attempts.get(ip_address, 0) + 1
                
                if failed_attempts[ip_address] >= MAX_FAILURES:
                    ban_ip(ip_address)
                    failed_attempts[ip_address] = 0

if __name__ == "__main__":
    try:
        monitor_events()
    except KeyboardInterrupt:
        print("\n[*] Korumadan çıkılıyor...")
