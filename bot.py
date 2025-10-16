import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token bot
BOT_TOKEN = '7720259745:AAFdOZ5TefxR3hZXcFFCs0bZywa4_Jd_pGg'

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto forward messages from channel to channel"""
    try:
        # Channel target
        target_channel = "@LPMBTNIH"
        
        # Cek jika pesan berasal dari channel @likalikushare
        if update.channel_post:
            message = update.channel_post
            chat = message.chat
            
            logging.info(f"Message from: {chat.title} (@{chat.username})")
            
            # Forward ke target channel
            await message.forward(chat_id=target_channel)
            logging.info(f"✅ Message forwarded to {target_channel}")
                
    except Exception as e:
        logging.error(f"❌ Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start"""
    await update.message.reply_text("🤖 Bot Auto Forward is running!")

def main():
    """Main function"""
    if not BOT_TOKEN:
        logging.error("❌ BOT_TOKEN tidak ditemukan!")
        return
        
    # Buat application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambah handlers
    application.add_handler(CommandHandler("start", start))
    
    # Handler untuk semua pesan di channel
    application.add_handler(MessageHandler(filters.ALL, forward_message))
    
    # Jalankan bot
    logging.info("🚀 Bot Auto Forward started...")
    logging.info("📥 Monitoring channels...")
    logging.info("📤 Forwarding to: @LPMBTNIH")
    
    application.run_polling()

if __name__ == "__main__":
    main()