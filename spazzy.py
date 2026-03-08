import requests
import schedule
import time
from datetime import datetime

TOKEN = "8657843146:AAE9qNCRc4KE4d4e4fZVbnKfXNaSFlnq-0o"
CHAT_IDS = ["694270267", "8786350932", "344763043"]

calendario = {
    6: "🟤 Stasera: UMIDO + PLASTICA",
    0: "⚫ Stasera: INDIFFERENZIATA",
    1: "🟢 Stasera: VETRO + CARTA",
    2: "🟤 Stasera: UMIDO",
    3: "🟡 Stasera: PLASTICA",
    4: "🟤 Stasera: UMIDO + CARTA",
}

def manda_messaggio():
    giorno = datetime.now().weekday()
    if giorno in calendario:
        testo = calendario[giorno]
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        for chat_id in CHAT_IDS:
            requests.post(url, data={"chat_id": chat_id, "text": testo})
        print(f"Messaggio inviato: {testo}")
    else:
        print("Sabato — nessuna spazzatura.")

schedule.every().day.at("20:00").do(manda_messaggio)     
#manda_messaggio()

print("Bot avviato. Aspetto le 20:00...")

while True:
    schedule.run_pending()
    time.sleep(60)
