# IoT Honeypot ve Botnet Analizi Projesi

Bu proje, Cowrie Honeypot kullanılarak toplanan 350.000+ saldırı logunu analiz eder ve görselleştirir.

## Proje Yapısı
- `index.py`: Logları analiz eden ve grafikler oluşturan ana yazılım.
- `test_analiz.py`: Kodun doğruluğunu kontrol eden birim testleri.
- `zararli_ip_raporu.csv`: Tespit edilen saldırganların IP ve ülke listesi (IOC).

##  Kurulum ve Çalıştırma
1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt