import os
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

async def giorno_fisso(update