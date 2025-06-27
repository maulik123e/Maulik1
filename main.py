import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from keep_alive import keep_alive

# Load bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Folder containing preview subfolders
PREVIEW_FOLDER = "previews"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if not args:
        await update.message.reply_text("👋 Welcome! Please send a folder code.\nExample: `/start V1`", parse_mode="Markdown")
        return

    folder = args[0]
    folder_path = os.path.join(PREVIEW_FOLDER, folder)

    if not