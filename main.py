import os
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

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
    
    update.message.reply_text(f"You want to forward messages from {source} to {destination}. Is that correct? (yes/no)")
    
    return CONFIRM

# Forward messages function
def forward_message(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == ADMIN_ID:
        message = update.message.reply_to_message
        if message:
            source = user_data['source']
            destination = user_data['destination']
            
            if message.text:
                context.bot.send_message(destination, message.text)
            elif message.document:
                context.bot.send_document(destination, document=InputFile(message.document.get_file().download()))
            elif message.video:
                context.bot.send_video(destination, video=InputFile(message.video.get_file().download()))
            elif message.photo:
                context.bot.send_photo(destination, photo=InputFile(message.photo[-1].get_file().download()))
                
# Broadcast message function
def broadcast(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.id == ADMIN_ID:
        users = context.bot.get_chat_members_count(update.message.chat.id)
        broadcast_message = update.message.text
        context.bot.send_message(update.message.chat.id, f"Broadcasting to {users} users...")
        context.bot.send_message(update.message.chat.id, broadcast_message)
    
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
    dispatcher.add_handler(MessageHandler(Filters.command(['broadcast']), broadcast))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
