import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import Config
import pandas as pd

MAIL_AYARLARI = Config.MAIL_AYARLARI

def send_email(veri_df,alici_email):
    if pd.api.types.is_datetime64_any_dtype(veri_df['tarih']):
        veri_df['tarih'] = veri_df['tarih'].dt.strftime('%d.%m.%Y %H:%M')

    veri_df = veri_df.rename(columns={
        'type': 'Tür',
        'ikn': 'İKN',
        'tarih': 'Tarih',
        'yer': 'Yer',
        'baslik': 'Başlık',
        'alt_baslik': 'Alt Başlık'
    })

    tablo_df = veri_df[['Tür', 'İKN', 'Tarih', 'Yer', 'Başlık', 'Alt Başlık']].head(10)

    html_table = tablo_df.to_html(
        index=False,
        border=1,
        justify='left',
        escape=False
    )

    html_stil = """
    <style>
    table {
        font-family: Arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    th {
        background-color: #4CAF50;
        color: white;
        text-align: left;
        padding: 8px;
    }
    td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    </style>
    """

    html_body = f"""
    <html>
        <head>{html_stil}</head>
        <body>
            <p><b> Günlük EKAP İhale Verileri</b></p>
            {html_table}
        </body>
    </html>
    """

    message = MIMEMultipart("alternative")
    message["From"] = MAIL_AYARLARI["gonderen"]
    message["To"] = alici_email
    message["Subject"] = "Günlük EKAP İhale Verileri (HTML Tablo)"

    message.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(MAIL_AYARLARI["smtp_server"], MAIL_AYARLARI["smtp_port"]) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(MAIL_AYARLARI["gonderen"], MAIL_AYARLARI["uygulama_sifresi"])
            mail.sendmail(message["From"], message["To"], message.as_string())
        print("HTML tablo içeren mail başarıyla gönderildi.")
    except Exception as e:
        print(" HTML mail gönderim hatası:", e)


def send_email_text_only(message_text,alici_email):
    message = MIMEMultipart()
    message["From"] = MAIL_AYARLARI["gonderen"]
    message["To"] = alici_email
    message["Subject"] = "Günlük EKAP İhale Bilgisi"
    message.attach(MIMEText(message_text, "plain"))

    try:
        with smtplib.SMTP(MAIL_AYARLARI["smtp_server"], MAIL_AYARLARI["smtp_port"]) as mail:
            mail.ehlo()
            mail.starttls()
            mail.login(MAIL_AYARLARI["gonderen"], MAIL_AYARLARI["uygulama_sifresi"])
            mail.sendmail(message["From"], message["To"], message.as_string())
        print(" Bilgilendirme maili gönderildi.")
    except Exception as e:
        print(" Bilgilendirme maili gönderilemedi:", e)


