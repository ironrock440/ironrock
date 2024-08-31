import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
import os

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get Telegram token from environment variable
TELEGRAM_TOKEN = os.getenv('6926181754:AAFIbks3AYITaDXPgLgr4B9f7LqqTy3DDU4')

# Nobitex API endpoint for order book
NOBITEX_ORDERBOOK_URL = 'https://api.nobitex.ir/v2/orderbook/'

# Function to get the current price for a cryptocurrency
def get_price(crypto):
    url = f"{NOBITEX_ORDERBOOK_URL}{crypto}IRT"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'ok':
            bids = data['bids']
            asks = data['asks']
            best_bid = bids[0][0] if bids else None
            best_ask = asks[0][0] if asks else None
            return best_bid, best_ask
    return None, None

# Command handler to start the bot and show the main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create an inline keyboard with three buttons
    keyboard = [
        [
            InlineKeyboardButton("TON", callback_data='TON'),
            InlineKeyboardButton("TRON", callback_data='TRON'),
            InlineKeyboardButton("USDT", callback_data='USDT')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the initial message with the keyboard
    await update.message.reply_text('Select a cryptocurrency to check the price:', reply_markup=reply_markup)

# Callback handler to show price or go back to the main menu
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    # Check the callback data and respond accordingly
    if query.data in ['TON', 'TRON', 'USDT']:
        best_bid, best_ask = get_price(query.data)
        if best_bid and best_ask:
            text = f"Price for {query.data}:\nBest Bid: {best_bid} IRR\nBest Ask: {best_ask} IRR"
        else:
            text = "Failed to fetch price data."
        # Add a back button to return to the main menu
        keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=text, reply_markup=reply_markup)
    elif query.data == 'back':
        # Go back to the main menu
        keyboard = [
            [
                InlineKeyboardButton("TON", callback_data='TON'),
                InlineKeyboardButton("TRON", callback_data='TRON'),
                InlineKeyboardButton("USDT", callback_data='USDT')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Select a cryptocurrency to check the price:", reply_markup=reply_markup)

async def main():
    # Initialize the bot
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot and run polling in a non-blocking way
    await application.run_polling()

# Entry point for the script
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
