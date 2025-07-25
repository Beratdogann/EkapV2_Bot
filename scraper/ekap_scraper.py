import undetected_chromedriver as uc # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from time import sleep
from mail.send_mail import send_email, send_email_text_only
import os
import pandas as pd # type: ignore
import sqlite3
from config import Config
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



class EkapScraper:
    def __init__(self, arama_terimi,email):
        self.config = Config()
        self.arama_terimi = arama_terimi
        self.email = email
        self.driver = None
        self.veri_df = None
        self.type_list = []
        self.id_type_date_location = []
        self.title_subtitle = []
        self.status_list = []
        self.db_adi = self.config.GENEL_AYARLAR["veritabani_adi"]
        self.tablo  = self.config.GENEL_AYARLAR["tablo_adi"]

    def baslat(self , alici_email=None):
        self._tarayici_ayarla()
        self._google_arama_yap()
        self._ekap_sitesine_git()
        self._filtreleme_ayarlari_yap()
        self._verileri_topla()
        self._verileri_isle()

        if self.veritabaninda_yeni_veri_var_mi():
            self._veritabanina_kaydet()
            self._mail_gonder(yeni_var=True, alici_email=alici_email)
        else:
            self._mail_gonder(yeni_var=False, alici_email=alici_email)

        self._tarayici_kapat()



    def _tarayici_ayarla(self):
        print("Tarayıcı ayarlanıyor...")
        
        self.driver = uc.Chrome()
        self.driver.get("https://www.google.com/?hl=tr")
        self.driver.maximize_window()

        # options = uc.ChromeOptions()
        # options.add_argument("--headless=new")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--disable-background-networking")
        # options.add_argument("--disable-background-timer-throttling")
        # options.add_argument("--disable-renderer-backgrounding")

        # try:
        #     self.driver = uc.Chrome(options=options, headless=True, use_subprocess=True)
        #     self.driver.get("https://www.google.com/?hl=tr")
        #     # self.driver.maximize_window()
        #     print("Tarayıcı başarıyla başlatıldı.")
        # except Exception as e:
        #     print("Tarayıcı başlatma hatası:", e)
        #     raise
        

    def _google_arama_yap(self):
        search_box = WebDriverWait(self.driver, self.config.GENEL_AYARLAR["max_bekleme_suresi"]).until(
            EC.presence_of_element_located(self.config.LOCATORS["google_arama_kutusu"])
        )
        search_box.send_keys(self.config.GENEL_AYARLAR["google_arama_terimi"])
        sleep(self.config.GENEL_AYARLAR["bekleme_suresi"])
        search_box.send_keys(Keys.ENTER)

    def _ekap_sitesine_git(self):
        link = WebDriverWait(self.driver, self.config.GENEL_AYARLAR["bekleme_suresi"]).until(
            EC.presence_of_element_located(self.config.LOCATORS["ekap_linki"])
        )
        link.click()
        sleep(self.config.GENEL_AYARLAR["bekleme_suresi"])

    def _filtreleme_ayarlari_yap(self):
        self._arama_terimi_gir()
        self._filtre_kutusunu_ac()
        self._ihale_ilaninda_ayari_yap()
        self._teknik_sartname_kontrol_yap()
        self._filtreleme_butonuna_tikla()
        self._yil_secimi_yap()

    def _arama_terimi_gir(self):
        placeholder = self.config.ARAMA_TERIMLERI[self.arama_terimi]["placeholder"]
        self.driver.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]').send_keys(self.arama_terimi)

    def _filtre_kutusunu_ac(self):
        filtre_kutusu = self.config.ARAMA_TERIMLERI[self.arama_terimi]["filtre_kutusu"]
        self.driver.find_element(By.XPATH, f'//input[@placeholder="{filtre_kutusu}"]').click()
        sleep(self.config.GENEL_AYARLAR["bekleme_suresi"])

        choose_all = self.driver.find_element(*self.config.LOCATORS["checkbox"])
        choose_all.click()
        choose_all.click()

    def _ihale_ilaninda_ayari_yap(self):
        if self.config.ARAMA_TERIMLERI[self.arama_terimi].get("ihale_ilaninda_kontrol"):
            detail_box = self.driver.find_element(*self.config.LOCATORS["ihale_ilaninda_checkbox"])
            if detail_box.get_attribute("aria-checked") != "true":
                detail_box.click()
            sleep(self.config.GENEL_AYARLAR["bekleme_suresi"])

    def _teknik_sartname_kontrol_yap(self):
        if self.config.ARAMA_TERIMLERI[self.arama_terimi].get("teknik_sartname_kontrol"):
            checkbox = self.driver.find_element(*self.config.LOCATORS["teknik_sartname_checkbox"])
            if checkbox.get_attribute("aria-checked") != "true":
                checkbox.click()
            sleep(self.config.GENEL_AYARLAR["bekleme_suresi"])

    def _filtreleme_butonuna_tikla(self):
        self.driver.find_element(*self.config.LOCATORS["filtreleme_butonu"]).click()
        sleep(self.config.GENEL_AYARLAR["bekleme_suresi"])

    def _yil_secimi_yap(self):
        self.driver.find_element(*self.config.LOCATORS["yil_secim_kutusu"]).click()
        sleep(self.config.GENEL_AYARLAR["bekleme_suresi"])

        year_element = self.driver.find_element(
            By.XPATH, f'//div[contains(@class, "dx-item") and contains(text(), "{self.config.GENEL_AYARLAR["yil"]}")]')
        self.driver.execute_script("arguments[0].click();", year_element)
        sleep(1)
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, self.config.GENEL_AYARLAR["bekleme_suresi"]).until(
            EC.element_to_be_clickable(self.config.LOCATORS["kapat_butonu"])
        ).click()
        sleep(5)

    def _verileri_topla(self):
        matches = self.driver.find_elements(*self.config.LOCATORS["ihale_kartlari"])

        self.type_list = []
        self.id_type_date_location = []
        self.title_subtitle = []
        self.status_list = []

        for match in matches:
            try:
                self.type_list.append(match.find_element(By.XPATH, './/div[contains(@class, "type-icon")]').text)
                self.id_type_date_location.append(match.find_element(By.XPATH, './/div[contains(@class, "id-type-date-location")]').text)
                self.title_subtitle.append(match.find_element(By.XPATH, './/div[contains(@class, "content")]').text)
                self.status_list.append(match.find_element(By.XPATH, './/div[contains(@class, "status")]').text)
            except Exception as e:
                print("Hata:", e)

    def _verileri_isle(self):
        try:
            self.veri_df = pd.DataFrame({
                'type': self.type_list,
                'id_type_date_location': self.id_type_date_location,
                'title_subtitle': self.title_subtitle,
                'status': self.status_list
            })

            def safe_split(text):
                text = str(text).replace("\n", " ").strip()
                parts = [p.strip() for p in text.split(" - ")]
                
                if len(parts) == 3:
                    ikn, tarih, yer = parts
                
                elif len(parts) == 2:
                    ikn = ""
                    tarih, yer = parts
                
                else:
                    ikn = ""
                    tarih = ""
                    yer = parts[0] if parts else ""
                
                return ikn, tarih, yer

                    
            
            split_data = self.veri_df['id_type_date_location'].apply(safe_split).apply(pd.Series)

            self.veri_df['ikn'] = split_data[0]
            self.veri_df['tarih'] = split_data[1]
            self.veri_df['yer'] = split_data[2]

            


            title_split = self.veri_df['title_subtitle'].str.split('\n', n=1, expand=True)
            self.veri_df['baslik'] = title_split[0]
            self.veri_df['alt_baslik'] = title_split[1].fillna('')


        except Exception as e:
            print(f"Veri işleme hatası: {str(e)}")
            if not hasattr(self, 'veri_df'):
                self.veri_df = pd.DataFrame()
            raise

        print(self.veri_df[['tarih', 'yer']])

   
    def _veritabanina_kaydet(self):
            if self.veri_df is None or self.veri_df.empty:
                print("Veri yok, veritabanına kaydedilmeyecek.")
                return

            with sqlite3.connect(self.db_adi) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.tablo} (
                        type        TEXT,
                        ikn         TEXT PRIMARY KEY,
                        tarih       TEXT,
                        yer         TEXT,
                        baslik      TEXT,
                        alt_baslik  TEXT,
                        status      TEXT
                    );
                """)
                for satir in self.veri_df.to_dict(orient="records"):
                    try:
                        cursor.execute(f"""
                            INSERT OR REPLACE INTO {self.tablo}
                            (type, ikn, tarih, yer, baslik, alt_baslik, status)
                            VALUES
                            (:type, :ikn, :tarih, :yer, :baslik, :alt_baslik, :status);
                        """, satir)
                    except Exception as e:
                        print(f"Satır eklenemedi: {satir}\nHata: {e}")
                conn.commit()


    def _tarayici_kapat(self):
        sleep(3)
        self.driver.quit()

    def verileri_goster(self):
        return self.veri_df

    def veritabaninda_yeni_veri_var_mi(self):
        try:
            if not os.path.exists(self.config.GENEL_AYARLAR["veritabani_adi"]):
                print("Veritabanı dosyası yok, yeni veri kabul edilecek.")
                return True

            with sqlite3.connect(self.config.GENEL_AYARLAR["veritabani_adi"]) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.config.GENEL_AYARLAR['tablo_adi']}';")
                if cursor.fetchone() is None:
                    print("Tablo yok, yeni veri kabul edilecek.")
                    return True

                mevcut_df = pd.read_sql_query(f"SELECT * FROM {self.config.GENEL_AYARLAR['tablo_adi']}", conn)

                if mevcut_df.empty or self.veri_df.empty:
                    return not self.veri_df.empty

                en_son_tarih = pd.to_datetime(mevcut_df["tarih"], errors="coerce").max()
                yeni_max_tarih = pd.to_datetime(self.veri_df["tarih"], errors="coerce").max()

                
                if pd.isna(yeni_max_tarih) or pd.isna(en_son_tarih):
                    return False

                return yeni_max_tarih > en_son_tarih

        except Exception as e:
            print(f" Karşılaştırma hatası: {e}")
            return True
    
    def _mail_gonder(self, yeni_var , alici_email):
        # if yeni_var and not self.veri_df.empty:
        #     send_email(self.veri_df)
        # else:
        #     send_email_text_only("Bugün yeni ihale verisi bulunmamaktadır.")
            if yeni_var and not self.veri_df.empty:
                send_email(self.veri_df, alici_email)
            else:
                send_email_text_only("Bugün yeni ihale verisi bulunmamaktadır.", alici_email)



# if __name__ == "__main__":
    
#     # def main():
#     #     for terim in ["Sinyalizasyon", "Trafik"]:
#     #         scraper = EkapScraper(terim)
#     #         scraper.baslat()
#     #         df = scraper.verileri_goster()
#     #         send_email(df)

