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


## Veri Seti Hakkında 

GitHub dosya boyutu sınırları nedeniyle, bu depoda projenin test edilmesi amacıyla **5.000 satırlık örnek veri seti (Sample Data)** bulunmaktadır. 

Kodları çalıştırdığınızda grafikler bu örnek veri üzerinden oluşacaktır.

**Tam Veri Seti (350.000+ Log - 190 MB):**
Analizlerin yapıldığı tam veri setini incelemek isterseniz aşağıdaki bağlantıdan indirebilirsiniz:
[Tam Veri Setini İndir (Google Drive Linki)](https://drive.google.com/file/d/1o513wkte2GqVHyfs43RsBhbueyw7-BCt/view?usp=sharing)

Not: İndirdiğiniz tam dosyayı proje klasörüne atıp kodun içindeki dosya adını güncelleyerek tam analizi görebilirsiniz.