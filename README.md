# 🤖 EKAP V2 Automation Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Selenium](https://img.shields.io/badge/Library-Selenium%20%7C%20SMTP-green)
![Status](https://img.shields.io/badge/Status-Active-success)

Bu proje, **EKAP (Elektronik Kamu Alımları Platformu)** üzerindeki ihaleleri otomatik olarak takip etmek, belirli kriterlere uyan ilanları yakalamak ve kullanıcıyı **e-posta yoluyla anında bilgilendirmek** amacıyla geliştirilmiştir.

## 🚀 Özellikler

* **Otomatik Giriş:** EKAP sistemine güvenli ve hızlı oturum açma.
* **Akıllı Filtreleme:** Anahtar kelime, sektör veya konuma göre ihale taraması.
* **📩 E-Posta Bildirimi:** Kriterlere uyan yeni bir ihale bulunduğunda otomatik mail atar.
* **Arka Plan Çalışması:** Belirlenen aralıklarla siteyi periyodik olarak kontrol eder.
* **Uygulama Desteği:** Kullanıcı dostu arayüz veya `exe` dosyası ile kolay kullanım.

## 🛠️ Kurulum

Projeyi çalıştırmak için aşağıdaki adımları izleyin:

1.  **Repoyu Klonlayın:**
    ```bash
    git clone [https://github.com/Beratdogann/EkapV2_Bot.git](https://github.com/Beratdogann/EkapV2_Bot.git)
    cd EkapV2_Bot
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **WebDriver:** Chrome sürümünüze uygun ChromeDriver'ın proje klasöründe olduğundan emin olun.

## ⚙️ Yapılandırma (Mail Ayarları)

Botun mail atabilmesi için gerekli ayarları yapmanız gerekmektedir. Proje içerisindeki ayar dosyasını (örneğin `config.json` veya `settings.py`) açarak kendi bilgilerinizi giriniz:

* **Gönderici Mail:** Bildirimleri gönderecek e-posta adresi (Örn: Gmail kullanıyorsanız "Uygulama Şifresi" almanız gerekebilir).
* **Alıcı Mail:** Bildirimlerin geleceği adres.
* **Mail Sunucusu:** (Örn: `smtp.gmail.com` port `587`)

## 💻 Kullanım

Uygulamayı başlatmak için:

```bash
python main.py
(Bot çalışmaya başladığında periyodik olarak siteyi tarar ve yeni bir sonuç bulduğunda mail kutunuza düşer.)

⚠️ Yasal Uyarı
Bu yazılım eğitim ve kişisel takip amaçlı geliştirilmiştir. EKAP platformunun kullanım koşullarına uygun hareket etmek kullanıcının sorumluluğundadır.

👤 İletişim
Geliştirici: Berat Doğan

GitHub: Beratdogann
