# 🌌 Astro-Calendar 

Astro-Calendar, dünya genelindeki aktif uzay ajanslarının (NASA, SpaceX, ESA, Roscosmos vb.) yaklaşan roket fırlatma takvimlerini otomatik olarak toplayan, işleyen ve tek tıkla **Google Takvim**'e entegre etmeyi amaçlayan bir projedir.

---

## 🛠️ Mimari ve Teknolojiler


* **Veri Katmanı (`veriler.py`):** The Space Devs API'sinden fırlatma verilerini çeker,  zaman dilimlerini (İstanbul/Europe) ve eksik verileri temizler , yerel bir SQLite veritabanına yazar.
* **Arayüz Katmanı (`visual.py`):** Kullanıcıların Google hesaplarıyla güvenli bir şekilde OAuth 2.0 protokolü üzerinden bağlanmasını ve verileri kendi takvimlerine tek tıkla senkronize etmesini sağlayan **Streamlit** arayüzü.

---

## 🚀 Özellikler

* **100+ Güncel Fırlatma:** Küresel ölçekteki tüm yaklaşan uzay görevlerinin takibi.
* **Otomatik Güncelleme:** Günlük olarak arka planda çalışan ve veritabanını güncel tutan GitHub Actions botu.

---

## 📦 Kurulum ve Lokal Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için:

1. Bu repoyu klonlayın:
   ```bash
   
   Bu repoyu klonlayın ---> git clone https://github.com/osmankaanozcan/astro-calendar.git
   
   proje klasörüne girin ---> cd astro-calendar

   Gerekli paketleri/bağımlılıkları yükleyin ---> pip install -r req.txt

