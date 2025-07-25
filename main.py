from scraper.ekap_scraper import EkapScraper
from mail.send_mail import send_email, send_email_text_only
from config import Config
from database.db_utils import oku

def main():
    alici_email = "#Receiver email address#"

    scraper = EkapScraper("Keyword from config file" , alici_email) 
    scraper.baslat()  

    
    if hasattr(scraper, "veritabaninda_yeni_veri_var_mi"):
        yeni_var = scraper.veritabaninda_yeni_veri_var_mi()
    else:
        yeni_var = not scraper.veri_df.empty

    if yeni_var and not scraper.veri_df.empty:
        send_email(scraper.veri_df, alici_email)
        scraper._veritabanina_kaydet()
    else:
        send_email_text_only("Bugün yeni ihale verisi bulunmamaktadır.", alici_email)

    print(oku(Config.GENEL_AYARLAR["veritabani_adi"], Config.GENEL_AYARLAR["tablo_adi"]))


if __name__ == "__main__":
    main()