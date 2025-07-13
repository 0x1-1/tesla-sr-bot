# Tesla Bot - Teknik Dokümantasyon

## 📦 Bağımlılıklar

### Ana Kütüphaneler

| Kütüphane | Versiyon | Açıklama |
|-----------|----------|----------|
| `pydantic` | 2.5.3 | Veri doğrulama ve model yönetimi |
| `requests` | 2.31.0 | HTTP istekleri için |
| `selenium` | 4.16.0 | Web otomasyon |
| `streamlit` | 1.29.0 | Web arayüzü |
| `apscheduler` | 3.10.4 | Görev zamanlama |
| `fake-useragent` | 1.4.0 | Rastgele User-Agent |
| `undetected-chromedriver` | 3.5.4 | Bot tespit koruması |
| `python-dotenv` | 1.0.0 | Çevre değişkenleri |
| `beautifulsoup4` | 4.12.2 | HTML parsing |
| `lxml` | 5.0.0 | XML/HTML işleme |

### Kurulum

```bash
pip install -r requirements.txt
```

## 🏗️ Mimari

### MVVM Pattern

Proje MVVM (Model-View-ViewModel) mimarisini takip eder:

- **Model**: `core/config.py` - Veri modelleri
- **View**: `app.py` - Streamlit UI
- **ViewModel**: `features/` - İş mantığı

### Core ve Features Yapısı

```
tesla_bot/
├── core/              # Temel yapılar
│   └── config.py      # Konfigürasyon modelleri
├── features/          # Özellikler
│   ├── inventory.py   # Envanter yönetimi
│   └── order_bot.py   # Sipariş otomasyonu
└── utils/            # Yardımcı fonksiyonlar
```

## 🔧 Teknik Detaylar

### Envanter API

Tesla'nın resmi envanter API'si kullanılır:

```python
INVENTORY_API = "https://www.tesla.com/api/tesla/inventory/tesla"

# API Parametreleri
{
    'model': 'my',           # Model Y
    'condition': 'new',      # Yeni araç
    'market': 'TR',         # Türkiye
    'language': 'tr',       # Türkçe
    'super_region': 'europe'
}
```

#### Türkiye İçin Özel Notlar

Tesla'nın API'si global olarak aynı endpoint'i kullanır, bölgesel farklılıklar query parametrelerinde belirtilir. Bot, otomatik olarak:

1. Ana API endpoint'ini dener: `https://www.tesla.com/api/tesla/inventory/tesla`
2. Eğer 404 hatası alırsa, alternatif URL'leri dener:
   - `https://www.tesla.com/tr_TR/inventory/api/v1/inventory-results`
   - `https://www.tesla.com/tr_TR/api/tesla/inventory`
   - `https://www.tesla.com/inventory/api/v1/inventory-results`

3. Türkiye'ye özel veri yapılarını kontrol eder

### Bot Korumaları

1. **Undetected ChromeDriver**: Selenium'un tespit edilmesini engeller
2. **Rastgele User-Agent**: Her oturumda farklı tarayıcı kimliği
3. **İnsan Davranışı Simülasyonu**:
   - Rastgele yazma hızı (0.05-0.15 sn/karakter)
   - Rastgele bekleme süreleri
   - Mouse offset ile tıklama

### Selenium Selektörler

Form elemanları için çoklu selektör stratejisi:

```python
selectors = [
    (By.NAME, field_name),
    (By.ID, field_name),
    (By.CSS_SELECTOR, f"input[name='{field_name}']"),
    (By.XPATH, f"//input[@name='{field_name}']")
]
```

## 🔐 Güvenlik

### Veri Güvenliği

- Kart bilgileri sadece runtime'da saklanır
- Session state kullanılır (disk'e yazılmaz)
- SSL/TLS üzerinden iletişim

### Bot Tespit Önlemleri

```python
# JavaScript özelliklerini maskele
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
```

## 📊 Performans

### Optimizasyonlar

1. **Session Pooling**: `requests.Session()` kullanımı
2. **Lazy Loading**: Selenium elementi sadece gerektiğinde yükle
3. **Async İşlemler**: Thread kullanımı ile UI bloklanmaz

### Rate Limiting

- API çağrıları arasında min 5 sn bekle
- Rastgele varyasyon ekle (±1 sn)

## 🐛 Debug

### Debug Modu

`debug_mod = True` ayarlandığında:

- Detaylı log mesajları
- Hata stack trace'leri
- Manuel onay istemi (sipariş öncesi)

### Log Seviyeleri

- `INFO`: Genel bilgi
- `SUCCESS`: Başarılı işlemler
- `WARNING`: Uyarılar
- `ERROR`: Hatalar

## 🔄 State Yönetimi

Streamlit session state kullanılır:

```python
st.session_state.bot_running  # Bot durumu
st.session_state.config       # Konfigürasyon
st.session_state.log_queue    # Log mesajları
```

## 📱 API Response Örneği

```json
{
  "results": [
    {
      "VIN": "7SAYGDEE1PF123456",
      "Model": "MY",
      "TrimName": "Model Y Standard Range",
      "Price": 1990000,
      "PAINT": {"Code": "red"},
      "INTERIOR": {"Code": "black"},
      "InventoryStatus": "Available"
    }
  ]
}
```

## 🚀 Deployment

### Lokal Çalıştırma

```bash
streamlit run app.py --server.port 8501
```

### Docker (Opsiyonel)

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

## 📈 Gelecek Geliştirmeler

1. **Veritabanı Entegrasyonu**: Sipariş geçmişi
2. **Bildirim Sistemi**: Email/SMS entegrasyonu
3. **Multi-Threading**: Paralel envanter kontrolü
4. **Proxy Desteği**: IP rotasyonu
5. **Captcha Çözümü**: 2Captcha entegrasyonu

## 🔗 Faydalı Linkler

- [Tesla API (Unofficial)](https://tesla-api.timdorr.com/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/) 