from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# Set up your API credentials from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user data
user_data = {}

# Handle /start command
@app.on_message(filters.command("start"))
def start(bot, update):
    chat_id = update.chat.id
    bot.send_message(chat_id, "Hi! I am your message forwarding bot. Send /cancel to stop.")

# Handle choosing source channel
@app.on_message(filters.text & ~filters.command)
def choose_source(bot, update):
    chat_id = update.chat.id
    user_data[chat_id] = {}  # Initialize user data dictionary
    user_data[chat_id]["source"] = update.text
    bot.send_message(chat_id, "Please enter the destination channel ID:")

# Handle confirming destination channel
@app.on_message(filters.text & ~filters.command)
def confirm_destination(bot, update):
    chat_id = update.chat.id
    user_data[chat_id]["destination"] = update.text
    
    # Create inline keyboard with "Yes" and "No" buttons
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data="yes"), InlineKeyboardButton("No", callback_data="no")]
    ])
    
    bot.send_message(chat_id, f"You want to forward messages from {user_data[chat_id]['source']} to {user_data[chat_id]['destination']}. Is that correct?", reply_markup=keyboard)

# Handle button responses
@app.on_callback_query()
def button_response(bot, update):
    query = update.data
    chat_id = update.message.chat.id
    
    if query == "yes":
        bot.edit_message_text(chat_id, update.message.message_id, "Great! Forwarding messages.")
        forward_messages(bot, chat_id)
    elif query == "no":
        bot.edit_message_text(chat_id, update.message.message_id, "Okay, let's start over.")
        # Implement handling for "No" response here

# Forward messages function (implement your logic here)
def forward_messages(bot, chat_id):
    # Implement your message forwarding logic here
    pass

if __name__ == "__main__":
    app.run()
    
