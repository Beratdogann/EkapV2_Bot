from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from scraper.ekap_scraper import EkapScraper
from utils.auth import kullanici_ekle, giris_dogrula
import traceback

app = Flask(__name__)
app.secret_key = 'gizli-key'

def log_error(message):
    with open("error.log", "a", encoding="utf-8") as f:
        f.write("==== Flask Hatası ====\n")
        f.write(message + "\n")
        traceback.print_exc(file=f)
        f.write("\n\n")

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    data = request.get_json()
    arama_terimi = data.get('arama_terimi')
    alici_email = data.get('alici_email')

    if not arama_terimi or not alici_email:
        return jsonify({'status': 'error', 'message': 'arama_terimi ve alici_email zorunludur.'}), 400

    try:
        scraper = EkapScraper(arama_terimi, alici_email)
        scraper.baslat(alici_email=alici_email)
        return jsonify({'status': 'success', 'message': 'Veriler alındı ve mail gönderildi.'})
    except Exception as e:
        log_error(str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email.endswith('@sinyalizasyon.com.tr'): # You can change this to any domain you want
            flash('Sadece @sinyalizasyon.com.tr uzantılı adres kabul edilir.')
            return redirect(url_for('register'))

        if kullanici_ekle(email, password):
            session['user'] = email
            return redirect(url_for('veri_al'))
        else:
            flash('Bu e-posta zaten kayıtlı.')
            return redirect(url_for('register'))

    try:
        return render_template('register.html')
    except Exception as e:
        log_error(f"register.html yüklenemedi: {str(e)}")
        return "register.html bulunamadı.", 500

@app.route('/veri', methods=['GET', 'POST'])
def veri_al():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        search_term = request.form['search_term']
        email = session['user']

        try:
            scraper = EkapScraper(search_term, email)
            scraper.baslat(alici_email=email)
            flash(f"{search_term} verileri {email} adresine gönderildi.")
        except Exception as e:
            flash(f"Hata oluştu: {e}")
            log_error(f"Veri alırken hata: {str(e)}")

        return redirect(url_for('veri_al'))

    try:
        return render_template('index.html')
    except Exception as e:
        log_error(f"index.html yüklenemedi: {str(e)}")
        return "index.html bulunamadı.", 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if giris_dogrula(email, password):
            session['user'] = email
            return redirect(url_for('veri_al'))
        else:
            flash('E-posta veya şifre hatalı.')
            return redirect(url_for('login'))

    try:
        return render_template('login.html')
    except Exception as e:
        log_error(f"login.html yüklenemedi: {str(e)}")
        return "login.html bulunamadı.", 500



if __name__ == '__main__':

    app.run(debug=True, port = 5000) 


