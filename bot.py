import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token bot - gunakan environment variable untuk keamanan
BOT_TOKEN = os.getenv('BOT_TOKEN', '7720259745:AAFdOZ5TefxR3hZXcFFCs0bZywa4_Jd_pGg')

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto forward messages from channel to channel"""
    try:
        # Channel sumber dan target
        source_channel = "@likalikushare"
        target_channel = "@LPMBTNIH"
        
        # Debug info
        logging.info(f"Received update: {update}")
        
        # Cek jika pesan berasal dari channel yang dituju
        if update.channel_post:
            message = update.channel_post
            chat = message.chat
            
            # Log informasi channel
            logging.info(f"Message from chat: {chat.title} (@{chat.username}) - ID: {chat.id}")
            
            # Forward pesan ke target channel
            if chat.username == "likalikushare" or str(chat.id) == "-1002122293090":  # ID channel sumber
                await context.bot.forward_message(
                    chat_id=target_channel,
                    from_chat_id=chat.id,
                    message_id=message.message_id
                )
                logging.info(f"✅ Message forwarded to {target_channel}")
            else:
                logging.info(f"❌ Message not from target source. From: @{chat.username}")
                
    except Exception as e:
        logging.error(f"❌ Error forwarding message: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start"""
    await update.message.reply_text("🤖 Bot Auto Forward is running!\n\n"
                                  "Bot akan otomatis forward pesan dari @likalikushare ke @LPMBTNIH")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /help"""
    await update.message.reply_text("ℹ️ Bot Auto Forward\n\n"
                                  "Fungsi: Auto forward pesan dari @likalikushare ke @LPMBTNIH\n\n"
                                  "Commands:\n"
                                  "/start - Mulai bot\n"
                                  "/help - Bantuan\n"
                                  "/status - Status bot")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /status"""
    await update.message.reply_text("🟢 Bot status: AKTIF\n"
                                  "📥 Source: @likalikushare\n"
                                  "📤 Target: @LPMBTNIH")

def main():
    """Main function"""
    # Validasi token
    if not BOT_TOKEN:
        logging.error("❌ BOT_TOKEN tidak ditemukan!")
        return
        
    # Buat application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambah handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    
    # Handler untuk forward message - PERBAIKAN FILTER
    application.add_handler(
        MessageHandler(
            filters.ALL,
            forward_message
        )
    )
    
    # Jalankan bot
    logging.info("🚀 Bot Auto Forward started...")
    logging.info("📥 Monitoring: @likalikushare")
    logging.info("📤 Forwarding to: @LPMBTNIH")
    
    application.run_polling()

if __name__ == "__main__":
    main()