# ORUMCEK KORUMASI 🕷️🛡️

Linux Sunucular için SSH Brute-Force Koruma Botu.

Bu bot, Linux sistem günlüklerini (`/var/log/auth.log`) sürekli izler ve başarısız SSH giriş denemelerini takip eder. Aynı IP adresinden 3 kez başarısız giriş yapıldığında, o IP adresini `iptables` üzerinden otomatik olarak engeller.

## Özellikler
- **Gerçek Zamanlı İzleme**: Auth loglarını anlık takip eder.
- **Otomatik Ban**: 3 başarısız denemede IP'yi bloklar.
- **Güvenlik Duvarı**: `iptables` kullanarak IP'yi engeller.

## Gereksinimler
- Linux İşletim Sistemi (Debian/Ubuntu vb.)
- Python 3.x
- Root Yetkileri

## Kurulum

1. Python yüklü değilse kurun.
2. Gerekli kütüphaneler standart kütüphanelerdir, ekstra kurulum gerekmez.

## Kullanım

Bu script, Logları okumak ve iptables kuralı eklemek için **Root Olarak Çalıştırılmalıdır**.

1. Terminali açın.
2. Proje klasörüne gidin:
   ```bash
   cd /root/ORUMCEKKORUMASI
   ```
3. Botu başlatın:
   ```bash
   sudo python3 orumcek_korumasi.py
   ```

Bot başladığında mevcut logların sonuna gidecek ve yeni gelen başarısız giriş denemelerini beklemeye başlayacaktır.

## Test Etme
Botu test etmek için:
1. Botu çalıştırın.
2. Başka bir cihazdan sunucuya **yanlış şifre** ile SSH yapmayı deneyin.
3. Konsolda "Tespit: X.X.X.X başarısız giriş yaptı" mesajını görmelisiniz.
4. 3. denemeden sonra "X.X.X.X başarıyla engellendi" mesajı çıkacaktır.
