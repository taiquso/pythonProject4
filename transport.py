import sys
import time
import math
import requests
import logging

token = sys.argv[1]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


def appeler_opendata(path):
    url = f"http://transport.opendata.ch/v1{path}"
    reponse = requests.get(url)
    return reponse.json()


def rechercher_arrets(parametres):
    data = appeler_opendata(parametres)
    arrets = data['stations']
    message_texte = "Voici les résultats:\n"

    for arret in arrets:
        if arret['id']:
            message_texte = f'{message_texte}\n /s{arret["id"]}'
            message_texte = f'{message_texte} {arret["name"]}'
            message_texte = f'{message_texte} ({arret["icon"]})'

    return message_texte


def rechercher_prochains_departs(id):
    data = appeler_opendata(f'/stationboard?id={id}')
    stationboard = data['stationboard']

    message_texte = "Here are the next departures ! 🙂:\n"
    maintenant = time.time()

    for depart in stationboard:
        message_texte += f"\n\n{depart['number']} → {depart['to']}\n"

        timestamp_depart = depart['stop']['departureTimestamp']
        diff = timestamp_depart - maintenant
        temps_en_minutes = math.floor(diff / 60)

        if temps_en_minutes < 0:
            message_texte += ' Already gone...'
        elif temps_en_minutes < 2:
            message_texte += ' RUN!'
        else:
            message_texte += f' in {temps_en_minutes} minutes'

    return message_texte


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}😀 write /stop with any city name to see all the buses and trains available in the city !😎 \n(Example : /stop Geneva)')


async def recherche_texte(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        texte_a_rechercher = ' '.join(context.args)
        arrets = rechercher_arrets(f'/locations?query={texte_a_rechercher}')
        await update.message.reply_text(arrets)
    else:
        await update.message.reply_text("Please provide a city name after the /stop command.")


async def recherche_gps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_location = update.message.location

    if user_location:
        arrets = rechercher_arrets(f'/locations?x={user_location.latitude}&y={user_location.longitude}')
        await update.message.reply_text(arrets)
    else:
        await update.message.reply_text("Please share your location for this command.")

async def afficher_arret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Extract the identifier from the command
    command_parts = update.message.text.split(" ")

    if len(command_parts) > 1:
        identifier = command_parts[1]
        prochains_departs = rechercher_prochains_departs(identifier)
        await update.message.reply_text(prochains_departs)
    else:
        await update.message.reply_text("Please provide a city name after the /departure command.")


def main() -> None:
    app = ApplicationBuilder().token(token).build()

    # app.add_handler(MessageHandler(filters.Regex("^bonjour$"), start))
    app.add_handler(MessageHandler(filters.COMMAND, afficher_arret))
    app.add_handler(MessageHandler(filters.LOCATION, recherche_gps))
    app.add_handler(MessageHandler(filters.TEXT, recherche_texte))
    app.add_handler(CommandHandler("transport", rechercher_prochains_departs))

    app.run_polling()
