import logging
import sys
import telegram

from transport import afficher_arret, rechercher_arrets, recherche_texte, rechercher_prochains_departs, \
    start as start_transport
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

token = sys.argv[1]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOICE, RESTAURANT, HANGOUT, RESTAU_RESULT, LOCATION, MUSEES, BARS, CLUBS, END, TRANSPORT = range(10)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Restaurant", "Hangout"]]

    await update.message.reply_text(
        "Hi! My name is Geneva Bot😁. \nI am here to help you chose for a restaurant or somewhere fun for you to go like bars, clubs or museums 😆!"
        "\nAre you looking for Restaurants or Hangout 🤔? \nClick with your mouse on whichever option suits you the most 😉!\n\nYou can also use the /transport command to see the available stops of buses and trains in a particular city and /departure following with a city name to see the next departures !😎",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Restaurants or Hangout?"
        ),
    )

    return CHOICE


async def start_transport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}😀 write /stop with any city name to see all the buses and trains available in the city !😎 \n(Example : /stop Geneva)')

    return TRANSPORT


async def choice_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["French", "Swiss"],
                      ["Japanese", "Lebanese", "Italian"],
                      ["Return"]]

    await update.message.reply_text(
        "You chose Restaurant 😃!"
        "\nWhat type of cuisine are you looking for 🤔? \n Click on that type of cuisine that you would like to eat tonight😊.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="What cuisine?"
        ),
    )

    return RESTAURANT


async def choice_hangout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["Musées", "Bars", "Clubs"],
                      ["Return"]]
    await update.message.reply_text(
        "You chose Hangout 😄!"
        "\nGood choice ! \nWhat are you looking for tonight 🤔?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Which hangout ?"
        ),
    )

    return HANGOUT


async def restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["Braceria Gerardo", "La Tranche Gerardo"],
                      ["Intenso", "Costa Smeralda", "Le Shogun"],
                      ["Return"]]

    await update.message.reply_text(
        "Here is a list of restaurants in Geneva I recommend you😎:"
        "\n\nBarceria Gerardo Scalea \nLa Tranche Gerardo Scalea\nRestaurant Intenso\nCosta Smeralda\nle Shogun"
        "\n\n\nWhich one are you interested in 🤔?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Which Restaurant ?"
        ),
    )

    return RESTAU_RESULT


async def restau_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["Display Location"],
                      ["Return"]]

    await update.message.reply_text(
        "Adress : \nRue du 31-Décembre 16, 1207 Geneva"
        "\n\nTelephone : \n022 736 93 06*"
        "\n\nE-Mail : \nrestaurant.shogun@live.fr"
        "\n\nWebsite : \nwww.leshogun.ch"
        "\n\nReview : \n4.6 / 5",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Display location"
        ),
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["Return to Restaurants"]]
    location_restaurant = telegram.Location(latitude=46.204130, longitude=6.158910)
    await update.message.reply_location(
        location=location_restaurant,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Back to start"
        ),
    )

    return END


async def hangout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "You chose museums😄"
        "\nGood choice 🧐!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return HANGOUT


async def musees(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["Return"]]
    await update.message.reply_text(
        "Here are the best museums in Geneva we can recommend you 😇: "
        "\n\n\nMusée d'Art et d'Histoire (MAH) de Genève : \nAdress:  Rue Charles-Galland 2, 1206 Genève, Suisse"
        "\n\nDescription : The MAH houses an extensive collection of artworks, archaeological artifacts, sculptures, natural history specimens, and more. It also features temporary exhibitions."
        "\n\n\nFondation Baur, Musée des Arts d'Extrême-Orient : \nAdress:  Rue Munier-Romilly 8, 1206 Genève, Suisse"
        "\n\nDescription : This museum specializes in Asian arts, showcasing an impressive collection of objects from East Asia, including porcelain, sculptures, paintings, and art from China, Japan, and Korea."
        "\n\n\nMusée international de la Croix-Rouge et du Croissant-Rouge \nAdress:   Avenue de la Paix 17, 1202 Genève, Suisse"
        "\n\nDescription : This museum highlights the history and humanitarian work of the Red Cross and Red Crescent through interactive exhibits, historical artifacts, documents, and testimonials.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Back to start"
        ),
    )

    return END


async def clubs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["Return"]]
    await update.message.reply_text(
        "Here are the best clubs in Geneva we can recommend you 😇: "
        "\n\n\nMoulin Rouge Club: \nAddress: Rue de la Rôtisserie 3, 1204 Geneva, Switzerland"
        "\n\nDescription: Moulin Rouge Club is a well-known nightclub in Geneva, offering a lively atmosphere with DJs playing a mix of electronic dance music (EDM) and other genres. It's particularly popular for its vibrant nightlife scene."
        "\n\n\nJava Club: \nAddress: Quai du Seujet 18, 1201 Geneva, Switzerland"
        "\n\nDescription: Java Club is a trendy nightclub located along the Rhône River. It features a stylish interior, hosts various events, and offers a diverse range of music, including electronic and house music."
        "\n\n\nSilencio Club: \nAddress: Rue de Lausanne 2, 1201 Geneva, Switzerland"
        "\n\nDescription: Silencio Club is known for its sophisticated and elegant ambiance. It hosts live music events, DJ nights, and offers a chic setting for those looking to enjoy a night out in Geneva.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Back to start"
        ),
    )

    return END


async def bars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [["Return"]]
    await update.message.reply_text(
        "Here are the best bars in Geneva we can recommend you 😇:"
        "\n\n\nLe Verre à Monique: \nAddress: Rue des Bains 25, 1205 Geneva, Switzerland"
        "\n\nDescription: Le Verre à Monique is known for its cozy and intimate atmosphere. It offers a wide selection of wines and cocktails, and the knowledgeable staff can help you choose the perfect drink."
        "\n\n\nL'Atelier Cocktail Club: \nAddress: Rue de la Coulouvrenière 19, 1204 Geneva, Switzerland"
        "\n\nDescription: L'Atelier Cocktail Club is a stylish cocktail bar with a creative menu. The skilled bartenders craft unique and delicious cocktails in a chic setting."
        "\n\n\nBrasserie des Halles de l'Île: \nAddress: Place de l'Île 1, 1204 Geneva, Switzerland"
        "\n\nDescription: While technically a brasserie, Brasserie des Halles de l'Île also has a vibrant bar scene. It's situated in a historical building and offers a selection of drinks in a lively atmosphere.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Back to start"
        ),
    )

    return END


async def rechercher_prochains_departs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    identifiant = update.message.text[2:]
    prochains_departs = rechercher_prochains_departs(identifiant)
    await update.message.reply_text(prochains_departs)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("transport", start_transport),
        ],
        states={
            CHOICE: [
                MessageHandler(filters.Regex("^(Restaurant)$"), choice_restaurant),
                MessageHandler(filters.Regex("^(Hangout)$"), choice_hangout)
            ],
            RESTAURANT: [
                MessageHandler(filters.Regex("^(French|Swiss|Japanese|Lebanese|Italian)$"), restaurant),
                MessageHandler(filters.Regex("^(Return)$"), start)
            ],
            RESTAU_RESULT: [
                MessageHandler(
                    filters.Regex("^(Braceria Gerardo|La Tranche Gerardo|Intenso|Costa Smeralda|Le Shogun)$"),
                    restau_result),
                MessageHandler(filters.Regex("^(Return)$"), choice_restaurant)
            ],
            LOCATION: [MessageHandler(filters.Regex("^(Display Location)$"), location),
                       MessageHandler(filters.Regex("^(Return)$"), restaurant)
                       ],
            HANGOUT: [MessageHandler(filters.Regex("^(Musées)$"), musees),
                      MessageHandler(filters.Regex("^(Bars)$"), bars),
                      MessageHandler(filters.Regex("^(Clubs)$"), clubs),
                      MessageHandler(filters.Regex("^(Return)$"), start)
                      ],
            END: [MessageHandler(filters.Regex("^(Return)$"), choice_hangout),
                  MessageHandler(filters.Regex("^(Return to Restaurants)$"), restaurant)
                  ],
            TRANSPORT: [
                CommandHandler("stop", recherche_texte),
                CommandHandler("departure", afficher_arret),
            ]

        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start),
            CommandHandler("transport", start_transport),
        ],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
