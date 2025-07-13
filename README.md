# 🚗 Tesla SR Otomatik Sipariş Botu

Tesla Model Y Standard Range araçları için otomatik sipariş sistemi. Bu bot, Tesla'nın resmi web sitesinden envanter kontrolü yapar ve kriterlere uygun araç bulduğunda otomatik sipariş vermeye çalışır.

## 🎯 Özellikler

- ✅ Tesla envanter API'sini sürekli kontrol
- ✅ SR (Standard Range) model filtreleme
- ✅ Renk tercihi ve fiyat limiti kontrolü
- ✅ Otomatik form doldurma (Selenium)
- ✅ Bot tespit korumaları
- ✅ Streamlit tabanlı kullanıcı arayüzü
- ✅ Satış saati kontrolü (17:59)
- ✅ Detaylı log sistemi

## 📋 Gereksinimler

- Python 3.8+
- Google Chrome tarayıcı
- ChromeDriver (otomatik indirilir)

## 🛠️ Kurulum

1. Projeyi klonlayın:
```bash
cd tesla_bot
```

2. Sanal ortam oluşturun:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

## 🚀 Kullanım

1. Uygulamayı başlatın:
```bash
streamlit run app.py
```

2. Tarayıcınızda açılan arayüzde:
   - Sol taraftan kullanıcı bilgilerinizi girin
   - Kart bilgilerinizi ekleyin
   - Araç tercihlerinizi belirleyin
   - Bot ayarlarını yapılandırın
   - "Ayarları Kaydet" butonuna tıklayın

3. "Başlat" butonuna tıklayarak botu çalıştırın

## ⚙️ Konfigürasyon

### Kullanıcı Bilgileri
- Ad, soyad
- E-posta adresi
- Telefon numarası

### Kart Bilgileri
- Kart sahibi adı
- Kart numarası (16 hane)
- Son kullanma tarihi
- CVV kodu
- Fatura posta kodu

### Araç Tercihleri
- Maksimum fiyat limiti
- Renk tercihleri (öncelik sırasına göre)
- Otomatik koltuk rengi kuralı
- Teslimat posta kodu

### Bot Ayarları
- Kontrol aralığı (saniye)
- Maksimum deneme sayısı
- Bot korumaları (aktif/pasif)
- Headless mod
- Debug modu
- Satış başlangıç saati

## 🏗️ Proje Yapısı

```
tesla_bot/
├── core/
│   ├── __init__.py
│   └── config.py          # Konfigürasyon modelleri
├── features/
│   ├── __init__.py
│   ├── inventory.py       # Envanter kontrolü
│   └── order_bot.py       # Sipariş botu
├── utils/
│   └── __init__.py
├── app.py                 # Streamlit arayüzü
├── requirements.txt       # Bağımlılıklar
└── README.md             # Bu dosya
```

## 🔒 Güvenlik Uyarıları

⚠️ **ÖNEMLİ**: Bu bot yalnızca eğitim ve test amaçlıdır!

- Kart bilgileriniz şifrelenmemiş olarak saklanır
- Gerçek sipariş vermeden önce tüm bilgileri kontrol edin
- Kişisel bilgilerinizin güvenliğinden siz sorumlusunuz
- Production ortamında kullanmayın

## 🤖 Bot Korumaları

Bot, Tesla'nın bot tespit sistemlerini aşmak için:
- Rastgele User-Agent kullanır
- İnsan benzeri yazma hızı simüle eder
- Rastgele bekleme süreleri ekler
- Undetected ChromeDriver kullanır

## 📊 API Detayları

Bot, Tesla'nın resmi envanter API'sini kullanır:
- Endpoint: `https://www.tesla.com/api/tesla/inventory/tesla`
- Market: TR (Türkiye)
- Model: Model Y
- Condition: New (Yeni)

## 🐛 Sorun Giderme

### ChromeDriver Hatası
```bash
# Manuel olarak ChromeDriver indirin
# https://chromedriver.chromium.org/
```

### SSL Hatası
```bash
pip install --upgrade certifi
```

### Selenium Hatası
Debug modunu açarak detaylı hata mesajlarını görebilirsiniz.

## 📝 Lisans

Bu proje eğitim amaçlıdır. Ticari kullanım için uygun değildir.

## ⚖️ Sorumluluk Reddi

Bu bot kullanılarak yapılan işlemlerden doğacak her türlü sorumluluk kullanıcıya aittir. Geliştiriciler hiçbir sorumluluk kabul etmez. 