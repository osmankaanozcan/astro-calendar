import requests
from datetime import datetime, timedelta
import pytz
import sqlite3
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

dp_name = 'manyak.db'
auth = ['https://www.googleapis.com/auth/calendar']

print("--- GÜNCELLENİYOR ---")

def tablo():
    baglanti = sqlite3.connect(dp_name)
    imlec = baglanti.cursor()
    imlec.execute('''
        CREATE TABLE IF NOT EXISTS firlatmalar (
            id TEXT PRIMARY KEY,
            isim TEXT,
            tarih TEXT,
            ajans TEXT,
            konum TEXT,
            ozet TEXT,
            yayin_linki TEXT,
            iso_tarih TEXT,
            eklendi_mi INTEGER DEFAULT 0
        )
    ''')
    baglanti.commit()
    baglanti.close()

def zaman_ayari(utc_ayari):
    ayarlanmis_zaman = utc_ayari.replace("Z", "+00:00")
    zaman_obj = datetime.fromisoformat(ayarlanmis_zaman)
    ist_zaman = zaman_obj.astimezone(pytz.timezone("Europe/Istanbul"))
    ekran_t = ist_zaman.strftime("%H:%M | %d-%m-%Y UTC")
    iso_t = ist_zaman.isoformat()

    return ekran_t, iso_t

def google_baglan():
    creds = None
    if os.path.exists('tkn.json'):
        creds = Credentials.from_authorized_user_file('tkn.json', auth)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', auth)
            creds = flow.run_local_server(port=0)
        with open('tkn.json', 'w') as token:
            token.write(creds.to_json())
    return build('calendar', 'v3', credentials=creds)

def kota():
    tablo()
    url = "https://lldev.thespacedevs.com/2.2.0/launch/upcoming/?limit=100"
    try:
        r = requests.get(url)
        r.raise_for_status()
        veriler = r.json()["results"]

        baglanti = sqlite3.connect(dp_name)
        imlec = baglanti.cursor()

        güncel_sayi = 0
        for f in veriler:
            imlec.execute("SELECT id FROM firlatmalar WHERE id=?", (f["id"],))
            if not imlec.fetchone():
                ekran, iso = zaman_ayari(f["net"])
                konum = f["pad"]["location"]["name"] if f.get("pad") else "Bilinmiyor"
                ozet = f["mission"]["description"] if f.get("mission") else "Görev detayı yok."
                yayin = f["vidURLs"][0]["url"] if f.get("vidURLs") else "Yayın henüz yok."

                imlec.execute('''
                    INSERT INTO firlatmalar (id, isim, tarih, ajans, konum, ozet, yayin_linki, iso_tarih)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (f["id"], f["name"], ekran, f["launch_service_provider"]["name"], konum, ozet, yayin, iso))
                güncel_sayi += 1

        baglanti.commit()
        baglanti.close()
        print(f"✅ Liste güncellendi. {güncel_sayi} yeni görev bulundu.")
    except Exception as e:
        print(f"❌ Veri çekme hatası: {e}")

def takvim():
    service = google_baglan()
    baglanti = sqlite3.connect(dp_name)
    imlec = baglanti.cursor()

    imlec.execute('''
                  SELECT id, isim, konum, ozet, yayin_linki, iso_tarih, tarih
                   FROM firlatmalar WHERE eklendi_mi = 0
                 ''' )
    rows = imlec.fetchall()

    if not rows:
        print(" ☻ Sistem senkronize edildi ☻.")
        baglanti.close()
        return

    for r in rows:
        f_id = r[0]
        isim = r[1]
        konum = r[2]
        ozet = r[3]
        yayin = r[4]
        start_t = r[5]
        tarih_metin = r[6]

        end_t = (datetime.fromisoformat(start_t) + timedelta(hours=1)).isoformat()

        event = {
            'summary': isim,
            'location': konum,
            'description': f"Planlanan Zaman: {tarih_metin}\n\n{ozet}\n\nYayın: {yayin}",
            'start': {
                'dateTime': start_t,
            },
            'end': {
                'dateTime': end_t,
            },
        }

        try:
            service.events().insert(calendarId='primary', body=event).execute()
            imlec.execute("UPDATE firlatmalar SET eklendi_mi = 1 WHERE id = ?", (f_id,))
            print(f"📅 Takvime İşlendi: {isim}")
        except Exception as e:
            print(f"❌ {isim} eklenirken hata: {e}")

    baglanti.commit()
    baglanti.close()

kota()
takvim()