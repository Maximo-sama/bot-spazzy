from dotenv import load_dotenv
load_dotenv()

import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
print("TOKEN LETTO:", TOKEN)
import asyncio
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import schedule
import time
import threading

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = ["694270267", "8786350932", "344763043"]

calendario = {
    0: "⚫ INDIFFERENZIATA",
    1: "🟢 VETRO + CARTA",
    2: "🟤 UMIDO",
    3: "🟡 PLASTICA",
    4: "🟤 UMIDO + CARTA",
    5: None,
    6: "🟤 UMIDO + PLASTICA",
}

nomi_giorni = {
    0: "Lunedì",
    1: "Martedì",
    2: "Mercoledì",
    3: "Giovedì",
    4: "Venerdì",
    5: "Sabato",
    6: "Domenica",
}

def cosa_si_butta(giorno_num):
    raccolta = calendario.get(giorno_num)
    nome = nomi_giorni[giorno_num]
    if raccolta:
        return f"🗓 {nome}: {raccolta}"
    else:
        return f"🗓 {nome}: nessuna raccolta"

async def stasera(update: Update, context: ContextTypes.DEFAULT_TYPE):
    giorno = datetime.now().weekday()
    await update.message.reply_text(cosa_si_butta(giorno))

async def domani(update: Update, context: ContextTypes.DEFAULT_TYPE):
    giorno = (datetime.now() + timedelta(days=1)).weekday()
    await update.message.reply_text(cosa_si_butta(giorno))

async def tutto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = "📅 Raccolta settimanale:\n\n"
    for num, nome in nomi_giorni.items():
        raccolta = calendario.get(num)
        if raccolta:
            testo += f"• {nome}: {raccolta}\n"
        else:
            testo += f"• {nome}: nessuna raccolta\n"
    await update.message.reply_text(testo)

async def giorno_fisso(update: Update, context: ContextTypes.DEFAULT_TYPE, giorno_num: int):
    await update.message.reply_text(cosa_si_butta(giorno_num))

async def manda_reminder(app):
    giorno = datetime.now().weekday()
    raccolta = calendario.get(giorno)
    if raccolta:
        testo = f"🔔 Reminder serale!\n{cosa_si_butta(giorno)}"
        for chat_id in CHAT_IDS:
            await app.bot.send_message(chat_id=chat_id, text=testo)
        print(f"Reminder inviato: {testo}")
    else:
        print("Sabato — nessun reminder.")

def avvia_scheduler(app):
    def job():
        asyncio.run(manda_reminder(app))
    schedule.every().day.at("20:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(30)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("stasera", stasera))
app.add_handler(CommandHandler("domani", domani))
app.add_handler(CommandHandler("tutto", tutto))
app.add_handler(CommandHandler("lunedi", lambda u, c: giorno_fisso(u, c, 0)))
app.add_handler(CommandHandler("martedi", lambda u, c: giorno_fisso(u, c, 1)))
app.add_handler(CommandHandler("mercoledi", lambda u, c: giorno_fisso(u, c, 2)))
app.add_handler(CommandHandler("giovedi", lambda u, c: giorno_fisso(u, c, 3)))
app.add_handler(CommandHandler("venerdi", lambda u, c: giorno_fisso(u, c, 4)))
app.add_handler(CommandHandler("sabato", lambda u, c: giorno_fisso(u, c, 5)))
app.add_handler(CommandHandler("domenica", lambda u, c: giorno_fisso(u, c, 6)))

threading.Thread(target=avvia_scheduler, args=(app,), daemon=True).start()

print("Bot avviato.")
app.run_polling()