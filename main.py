import os
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler

# Set up environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Conversation states
CHOOSING, CONFIRM = range(2)

# Dictionary to store user data
user_data = {}

# Start command handler
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Hi! I am your message forwarding bot. Send /cancel to stop.")

    return CHOOSING

# Function to get source channel ID
def choose_source(update: Update, context: CallbackContext) -> int:
    user_data['source'] = update.message.text
    update.message.reply_text("Please enter the destination channel ID:")
    
    return CONFIRM

# Function to get destination channel ID and confirm forwarding
def confirm_destination(update: Update, context: CallbackContext) -> int:
    user_data['destination'] = update.message.text
    source = user_data['source']
    destination = user_data['destination']
    
    # Create an InlineKeyboardMarkup with "Yes" and "No" buttons
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="yes"),
         InlineKeyboardButton("No", callback_data="no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(f"You want to forward messages from {source} to {destination}. Is that correct?", reply_markup=reply_markup)
    
    return CONFIRM

# Forward messages function (implement your logic here)
def forward_message(update: Update, context: CallbackContext) -> None:
    # Implement your message forwarding logic here

# Callback function for handling button responses
def button_response(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == "yes":
        query.edit_message_text("Great! Forwarding messages.")
        forward_message(update, context)
    elif query.data == "no":
        query.edit_message_text("Okay, let's start over.")
        # Implement handling for "No" response here
    
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(Filters.text & ~Filters.command, choose_source)],
            CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm_destination)]
        },
        fallbacks=[],
    )
    
    # Message handler
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, forward_message))
    dispatcher.add_handler(CallbackQueryHandler(button_response))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
