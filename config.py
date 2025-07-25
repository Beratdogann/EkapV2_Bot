from selenium.webdriver.common.by import By # type: ignore
import os
class Config:
    ARAMA_TERIMLERI = {
        "Sinyalizasyon": {
            "placeholder": "İKN'de ve İhale Adında Ara",
            "filtre_kutusu": "Seçiniz",
            "ihale_ilaninda_kontrol": True,
            "teknik_sartname_kontrol": False
        },
        "Trafik": {
            "placeholder": "İKN'de ve İhale Adında Ara",  
            "filtre_kutusu": "Seçiniz",
            "ihale_ilaninda_kontrol": False,
            "teknik_sartname_kontrol": True
        }
    }

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    GENEL_AYARLAR = {
        "yil": "2025",
        "veritabani_adi": "ekapV2.db",
        "tablo_adi": "ilanlar",
        "bekleme_suresi": 4,
        "max_bekleme_suresi": 14,
        "google_arama_terimi": "ekap v2"
    }

    LOCATORS = {
        "google_arama_kutusu": (By.CLASS_NAME, "gLFyf"),
        "ekap_linki": (By.PARTIAL_LINK_TEXT, "EKAP (Elektronik Kamu Alımları Platformu)"),
        "filtreleme_butonu": (By.CLASS_NAME, "dx-button-text"),
        "yil_secim_kutusu": (By.XPATH, '//input[@placeholder="Seç"]'),
        "kapat_butonu": (By.XPATH, '//div[@role="button" and @aria-label="Kapat"]'),
        "ihale_kartlari": (By.CLASS_NAME, "tender-list-item-wrapper"),
        "checkbox": (By.CLASS_NAME, "dx-checkbox-text"),
        "ihale_ilaninda_checkbox": (By.XPATH, '//span[text()="İhale İlanında"]/ancestor::li//div[@role="checkbox"]'),
        "teknik_sartname_checkbox": (By.XPATH, '//span[text()="Teknik Şartnamede"]/ancestor::li//div[@role="checkbox"]'),

    }


    MAIL_AYARLARI = {
        "gonderen": "#field your sender email address#",
        "uygulama_sifresi": "#field your aplication password#",
        "smtp_server": "smtp.yandex.com", #if you want use gmail, change it to "smtp.gmail.com"
        "smtp_port": 587
    }
