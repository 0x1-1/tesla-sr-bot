"""
Tesla Bot Web Arayüzü
Streamlit tabanlı kullanıcı arayüzü
"""

import streamlit as st
import threading
import time
import json
from datetime import datetime
from typing import Optional
import queue
import os

# Import our modules
from core.config import (
    TeslaConfig, KullaniciHesabi, KartBilgisi, 
    AracTercihi, BotAyarlari, RenkTercihi, AracTipi
)
from features.inventory import TeslaEnvanter, EnvanterArac
from features.order_bot import TeslaSiparisBot

# Sayfa yapılandırması
st.set_page_config(
    page_title="Tesla SR Bot",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global değişkenler
if 'bot_thread' not in st.session_state:
    st.session_state.bot_thread = None
if 'bot_running' not in st.session_state:
    st.session_state.bot_running = False
if 'log_queue' not in st.session_state:
    st.session_state.log_queue = queue.Queue()
if 'config' not in st.session_state:
    st.session_state.config = None


def log_mesaj(mesaj: str, seviye: str = "INFO"):
    """Log mesajı ekle"""
    zaman = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{zaman}] [{seviye}] {mesaj}"
    st.session_state.log_queue.put(log_entry)


def bot_calistir(config: TeslaConfig):
    """Bot'u arka planda çalıştır"""
    try:
        log_mesaj("Bot başlatılıyor...", "INFO")
        
        # Envanter nesnesini oluştur
        envanter = TeslaEnvanter(config)
        
        # Sipariş bot nesnesini oluştur
        siparis_bot = TeslaSiparisBot(config)
        
        def siparis_callback(arac: EnvanterArac):
            """Araç bulunduğunda çağrılacak fonksiyon"""
            log_mesaj(f"Uygun araç bulundu: {arac.vin}", "SUCCESS")
            log_mesaj(f"Model: {arac.trim}, Renk: {arac.renk}, Fiyat: {arac.fiyat:,.0f} TL", "INFO")
            
            # Sipariş işlemini başlat
            if siparis_bot.siparis_ver(arac):
                log_mesaj("Sipariş başarıyla verildi!", "SUCCESS")
                st.session_state.bot_running = False
            else:
                log_mesaj("Sipariş işlemi başarısız!", "ERROR")
        
        # Sürekli kontrol başlat
        envanter.surekli_kontrol(callback=siparis_callback)
        
    except Exception as e:
        log_mesaj(f"Bot hatası: {str(e)}", "ERROR")
    finally:
        st.session_state.bot_running = False
        log_mesaj("Bot durduruldu", "INFO")


def main():
    """Ana uygulama"""
    
    # Başlık
    st.title("🚗 Tesla SR Otomatik Sipariş Botu")
    st.markdown("Model Y Standard Range araçları için otomatik sipariş sistemi")
    
    # Sidebar - Konfigürasyon
    with st.sidebar:
        st.header("⚙️ Konfigürasyon")
        
        # Kullanıcı Bilgileri
        with st.expander("👤 Kullanıcı Bilgileri", expanded=True):
            ad = st.text_input("Ad", placeholder="Ahmet")
            soyad = st.text_input("Soyad", placeholder="Yılmaz")
            email = st.text_input("E-posta", placeholder="ahmet.yilmaz@example.com")
            telefon = st.text_input("Telefon", placeholder="5551234567")
        
        # Kart Bilgileri
        with st.expander("💳 Kart Bilgileri"):
            kart_sahibi = st.text_input("Kart Sahibi", placeholder="AHMET YILMAZ")
            kart_no = st.text_input("Kart Numarası", placeholder="4532123456789012", type="password")
            col1, col2 = st.columns(2)
            with col1:
                son_kullanma_ay = st.number_input("Ay", min_value=1, max_value=12, value=12)
            with col2:
                son_kullanma_yil = st.number_input("Yıl", min_value=2024, max_value=2030, value=2025)
            cvv = st.text_input("CVV", placeholder="123", type="password", max_chars=3)
            fatura_posta_kodu = st.text_input("Fatura Posta Kodu", placeholder="34000")
        
        # Araç Tercihleri
        with st.expander("🚙 Araç Tercihleri"):
            maksimum_fiyat = st.number_input(
                "Maksimum Fiyat (TL)", 
                min_value=1000000.0, 
                max_value=5000000.0, 
                value=2000000.0,
                step=100000.0,
                format="%.0f"
            )
            
            renk_tercih_sirasi = st.multiselect(
                "Renk Tercihleri (Öncelik Sırasına Göre)",
                options=[
                    ("red", "🔴 Kırmızı"),
                    ("white", "⚪ Beyaz"),
                    ("black", "⚫ Siyah"),
                    ("blue", "🔵 Mavi"),
                    ("grey", "⚫ Gri"),
                    ("standard", "🎨 Standart")
                ],
                default=[("red", "🔴 Kırmızı"), ("standard", "🎨 Standart")],
                format_func=lambda x: x[1]
            )
            
            koltuk_rengi_kurali = st.checkbox(
                "Otomatik koltuk rengi (Kırmızı=Standart, Diğer=Beyaz)",
                value=True
            )
            
            teslimat_posta_kodu = st.text_input("Teslimat Posta Kodu", placeholder="34000")
        
        # Bot Ayarları
        with st.expander("🤖 Bot Ayarları"):
            kontrol_araligi = st.slider(
                "Kontrol Aralığı (saniye)",
                min_value=1,
                max_value=60,
                value=5
            )
            
            maksimum_deneme = st.number_input(
                "Maksimum Deneme",
                min_value=1,
                max_value=1000,
                value=100
            )
            
            bot_korumalari = st.checkbox("Bot Korumaları Aktif", value=True)
            headless_mod = st.checkbox("Headless Mod", value=False)
            debug_mod = st.checkbox("Debug Modu", value=False)
            
            satis_baslangic_saati = st.time_input(
                "Satış Başlangıç Saati",
                value=datetime.strptime("17:59", "%H:%M").time()
            )
        
        # Kaydet butonu
        if st.button("💾 Ayarları Kaydet", use_container_width=True):
            try:
                # Konfigürasyon oluştur
                config = TeslaConfig(
                    kullanici=KullaniciHesabi(
                        ad=ad,
                        soyad=soyad,
                        email=email,
                        telefon=telefon
                    ),
                    kart=KartBilgisi(
                        kart_sahibi=kart_sahibi,
                        kart_no=kart_no,
                        son_kullanma_ay=son_kullanma_ay,
                        son_kullanma_yil=son_kullanma_yil,
                        cvv=cvv,
                        fatura_posta_kodu=fatura_posta_kodu
                    ),
                    tercih=AracTercihi(
                        arac_tipi=AracTipi.SR,
                        maksimum_fiyat=maksimum_fiyat,
                        renk_tercihi=[RenkTercihi(r[0]) for r in renk_tercih_sirasi],
                        koltuk_rengi_kurali=koltuk_rengi_kurali,
                        teslimat_posta_kodu=teslimat_posta_kodu
                    ),
                    bot=BotAyarlari(
                        kontrol_araligi=kontrol_araligi,
                        maksimum_deneme=maksimum_deneme,
                        bot_korumalari=bot_korumalari,
                        headless_mod=headless_mod,
                        debug_mod=debug_mod,
                        satis_baslangic_saati=satis_baslangic_saati.strftime("%H:%M")
                    )
                )
                
                st.session_state.config = config
                st.success("✅ Ayarlar başarıyla kaydedildi!")
                
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")
    
    # Ana içerik
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("📊 Durum")
        
        # Durum göstergesi
        if st.session_state.bot_running:
            st.success("🟢 Bot Çalışıyor")
        else:
            st.info("🔴 Bot Durduruldu")
        
        # Kontrol butonları
        col_start, col_stop = st.columns(2)
        
        with col_start:
            if st.button("▶️ Başlat", use_container_width=True, disabled=st.session_state.bot_running):
                if st.session_state.config:
                    st.session_state.bot_running = True
                    st.session_state.bot_thread = threading.Thread(
                        target=bot_calistir,
                        args=(st.session_state.config,),
                        daemon=True
                    )
                    st.session_state.bot_thread.start()
                    st.rerun()
                else:
                    st.error("❌ Önce ayarları kaydedin!")
        
        with col_stop:
            if st.button("⏹️ Durdur", use_container_width=True, disabled=not st.session_state.bot_running):
                st.session_state.bot_running = False
                log_mesaj("Bot durdurma isteği alındı", "WARNING")
                st.rerun()
    
    with col2:
        st.header("ℹ️ Bilgi")
        st.metric("Kontrol Aralığı", f"{st.session_state.config.bot.kontrol_araligi if st.session_state.config else 0} sn")
        st.metric("Max Deneme", st.session_state.config.bot.maksimum_deneme if st.session_state.config else 0)
    
    # Log Alanı
    st.header("📜 İşlem Kayıtları")
    
    log_container = st.container()
    
    # Auto-refresh için placeholder
    log_placeholder = st.empty()
    
    # Log mesajlarını göster
    if not st.session_state.log_queue.empty():
        logs = []
        while not st.session_state.log_queue.empty():
            logs.append(st.session_state.log_queue.get())
        
        with log_placeholder.container():
            for log in logs:
                if "[SUCCESS]" in log:
                    st.success(log)
                elif "[ERROR]" in log:
                    st.error(log)
                elif "[WARNING]" in log:
                    st.warning(log)
                else:
                    st.info(log)
    
    # Auto-refresh
    if st.session_state.bot_running:
        time.sleep(1)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>⚠️ <strong>Uyarı:</strong> Bu bot yalnızca eğitim ve test amaçlıdır.</p>
            <p>Gerçek sipariş vermeden önce tüm bilgileri kontrol edin.</p>
            <p>Kart ve kişisel bilgilerinizin güvenliğinden siz sorumlusunuz.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main() 