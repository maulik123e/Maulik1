import os
import re
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive

BOT_TOKEN = "7312814639:AAHsVOkNCHnej6sfvujEHwlviP0Ox1dnKVU"  # 🔁 Replace with your real bot token
BASE_DIR = "previews"  # Folder where screenshots are stored
DELETE_DELAY = 120  # Delay (in seconds) to delete screenshots

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me a link or keyword to get video preview screenshots.")

# Extract folder name from a link
def extract_folder_name(text: str):
    match = re.search(r'/([^/\s]+)/?$', text.strip())
    return match.group(1) if match else text.strip()

# Main handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    folder_name = extract_folder_name(user_input)
    folder_path = os.path.join(BASE_DIR, folder_name)

    if not os.path.isdir(folder_path):
        await update.message.reply_text("❌ No previews found for this request.")
        return

    files = os.listdir(folder_path)
    sent_messages = []

    for file in files:
        file_path = os.path.join(folder_path, file)

        # Skip small or empty files
        if os.path.getsize(file_path) < 1024:
            await update.message.reply_text(f"⚠️ Skipped small file (may be broken): {file}")
            continue

        try:
            msg = await update.message.reply_photo(photo=open(file_path, "rb"))
            sent_messages.append(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Error sending {file}\nReason: {str(e)}")

    # Auto-delete after delay
    await asyncio.sleep(DELETE_DELAY)
    for msg in sent_messages:
        try:
            await context.bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        except:
            pass  # Ignore if already deleted

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    keep_alive()
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())