import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Get token from environment variable (HEROKU)
BOT_TOKEN = os.getenv('BOT_TOKEN', '7720259745:AAFdOZ5TefxR3hZXcFFCs0bZywa4_Jd_pGg')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto forward messages from one channel to another"""
    try:
        # ID channel sumber dan tujuan
        source_channel = "@likalikushare"
        target_channel = "@LPMBTNIH"
        
        # Cek jika pesan berasal dari channel sumber
        if update.channel_post and update.channel_post.chat.username == "likalikushare":
            # Forward message
            await context.bot.forward_message(
                chat_id=target_channel,
                from_chat_id=update.channel_post.chat.id,
                message_id=update.channel_post.message_id
            )
            logging.info(f"✅ Pesan berhasil di-forward ke {target_channel}")
            
    except Exception as e:
        logging.error(f"❌ Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Auto Share is running on Heroku!")

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    
    # Handler untuk message dari channel sumber
    application.add_handler(
        MessageHandler(
            filters.Chat(username="likalikushare") & filters.ALL,
            forward_message
        )
    )
    
    # Start bot dengan error handling
    port = int(os.environ.get('PORT', 8443))
    logging.info("Bot started on Heroku...")
    application.run_polling()

if __name__ == "__main__":
    main()