import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# PERBAIKAN: Token langsung atau dari environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN', '7720259745:AAFdOZ5TefxR3hZXcFFCs0bZywa4_Jd_pGg')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto forward messages from one channel to another"""
    try:
        source_channel = "@likalikushare"
        target_channel = "@LPMBTNIH"
        
        if update.channel_post and update.channel_post.chat.username == "likalikushare":
            await context.bot.forward_message(
                chat_id=target_channel,
                from_chat_id=update.channel_post.chat.id,
                message_id=update.channel_post.message_id
            )
            logging.info(f"✅ Pesan di-forward ke {target_channel}")
            
    except Exception as e:
        logging.error(f"❌ Error: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Auto Share is running on Railway!")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "7720259745:AAFdOZ5TefxR3hZXcFFCs0bZywa4_Jd_pGg":
        logging.error("❌ BOT_TOKEN not set properly!")
        return
        
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(
            filters.Chat(username="likalikushare") & filters.ALL,
            forward_message
        )
    )
    
    logging.info("🚀 Bot started on Railway...")
    application.run_polling()

if __name__ == "__main__":
    main()