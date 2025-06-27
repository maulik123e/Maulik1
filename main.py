import os
import telebot
from keep_alive import keep_alive  # Optional, for hosting

# Get your bot token from environment variable or paste directly here
BOT_TOKEN = os.getenv("BOT_TOKEN")  # or replace with your actual token

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Welcome! Send /preview to get image previews.")

@bot.message_handler(commands=['preview'])
def send_previews(message):
    folder_path = "screenshots"  # Make sure this folder exists in your project

    if not os.path.exists(folder_path):
        bot.send_message(message.chat.id, "❌ No preview folder found.")
        return

    sent_any = False

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Skip if file doesn't exist or is too small (possibly broken)
        if not os.path.exists(file_path) or os.path.getsize(file_path) < 1024:
            continue

        try:
            with open(file_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
                sent_any = True
        except Exception as e:
            print(f"⚠️ Error sending {file_name}: {e}")
            bot.send_message(message.chat.id, f"❌ Error sending {file_name}")

    if not sent_any:
        bot.send_message(message.chat.id, "⚠️ No valid images found to preview.")

# Keep-alive for Replit or Render
keep_alive()

# Start the bot
bot.infinity_polling()
