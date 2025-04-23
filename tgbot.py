from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from getWeather import *
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackQueryHandler
API_TOKEN = "7927164642:AAEgkY9zsddPrusHPgaQUgN9e804HNZ5GAQ"


#represents state or keep track of where we are in a conversation
CHOOSE_LOCATION, CHOOSE_TIME, CHOOSE_CITY = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays which location wether they want to see"""
    reply_keyboard = [["Other cities"]]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard)
    await update.message.reply_text(
        'Welcome to wether bot!\n'
        'Choose the location you want.',
        parse_mode="HTML",
        reply_markup=reply_markup
    )
    return CHOOSE_LOCATION


async def choose_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choosen_location = update.message.text
    await update.message.reply_text("welcome", reply_markup=ReplyKeyboardRemove())
    if choosen_location == "Other cities":
        cities = ["Jimma", "Addis Abeba", "Hawassa", "Bahirdar", "Dire Dawa"]
        keyboard = [
            [InlineKeyboardButton(i, callback_data=i)] for i in cities
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "\t Choose city \t\n",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    else:
        await update.message.reply_text("Unkown choice please try agin.")

async def choose_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choosen_location = query.data
    weather = get_weather(f"{choosen_location}")
    await query.edit_message_text(
       text=f"\t\t <b>City choosen</b>: {weather['name']} \t\t\n"
        f"\t\t Weather Today: {weather['weather']} \t\t\n"
        f"\t\t Tempreture: {weather['temp_info']['temp']}ºC \t\t\n"
        f"\t\t Feels like: {weather['temp_info']['feels_like']}ºC \t\t\n"
        f"\t\t Humidity: {weather['temp_info']['humidity']}% \t\t\n"
        f"\t\t Wind speed: {weather['wind']['speed']}km/hr \t\t\n"
        f"\t\t Sunrise: {weather['sys']['sunrise']} \t\t\n"
        f"\t\t Sunset: {weather['sys']['sunset']} \t\t\n",
        parse_mode = 'HTML'
    )

async def dislay_weather(update, context, weather):
    pass

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is a bot where you get current weather condition.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bye bye!")
    return ConversationHandler.END

if __name__ == "__main__":
    application = ApplicationBuilder().token(API_TOKEN).build()
    
    start_handler = CommandHandler("start", start)
    location_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, choose_location)
    cancel_handler = CommandHandler("cancel", cancel)
    handle_choose_city = CallbackQueryHandler(choose_city)
    
    
    application.add_handler(start_handler)
    application.add_handler(cancel_handler)
    application.add_handler(location_handler)
    application.add_handler(handle_choose_city)
    
    application.add_handler(CommandHandler("help", help))
    
    application.run_polling()
    