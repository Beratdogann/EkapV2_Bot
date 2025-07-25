import threading
import webview
from web import app
import sys
import traceback

# Hataları log dosyasına kaydet
def log_exception(exc_type, exc_value, exc_traceback):
    with open("error.log", "a", encoding="utf-8") as f:
        f.write("==== Uygulama Hatası ====\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        f.write("\n\n")

sys.excepthook = log_exception

def run_flask():
    try:
        app.run(debug=False, port=5000, use_reloader=False)
    except Exception:
        log_exception(*sys.exc_info())

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    webview.create_window("EKAP V2 Otomasyon", "http://127.0.0.1:5000", width=1024, height=768)
    webview.start()



# import threading
# import webview 
# from web import app


# def run_flask():
#     app.run(debug=False, port=5000, use_reloader=False)

# if __name__ == '__main__':
#     flask_thread = threading.Thread(target=run_flask)
#     flask_thread.daemon = True
#     flask_thread.start()

#     # Webview penceresini oluştur
#     webview.create_window("EKAP V2 Otomasyon", "http://127.0.0.1:5000", width=1024, height=768)
#     webview.start()
