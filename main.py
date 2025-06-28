import os
import telebot
from keep_alive import keep_alive  # Optional, for hosting

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Make sure to set this in Render
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_previews(message):
    try:
        cmd_parts = message.text.strip().split()

        # If only "/start" is sent without any folder
        if len(cmd_parts) != 2:
            bot.reply_to(message, "📁 Please send like this:\n`/start movie1`", parse_mode="Markdown")
            return

        folder_name = cmd_parts[1]
        folder_path = os.path.join("previews", folder_name)

        if not os.path.exists(folder_path):
            bot.send_message(message.chat.id, f"❌ No folder named `{folder_name}` found.", parse_mode="Markdown")
            return

        sent_any = False

        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            if not os.path.exists(file_path) or os.path.getsize(file_path) < 1024:
                continue  # skip small/broken files

            try:
                with open(file_path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo)
                    sent_any = True
            except Exception as e:
                print(f"⚠️ Error sending {file_name}: {e}")
                bot.send_message(message.chat.id, f"❌ Error sending {file_name}")

        if not sent_any:
            bot.send_message(message.chat.id, f"⚠️ No valid images found in `{folder_name}`.", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Unexpected error: {e}")

# For hosting
keep_alive()

# Start bot
bot.infinity_polling()
