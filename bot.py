from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")


SPREADSHEET_ID = "1JYZRB1ihWg0bT0IahJg8HKuN1XdSzyRUSUT161FoAAk"

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ ForensXBiotech Job Bot Active!\n\n"
        "Send job text or Instagram job post."
    )

def extract_field(text, key):
    for line in text.split("\n"):
        if line.lower().startswith(key.lower()):
            return line.split(":", 1)[1].strip()
    return ""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title = extract_field(text, "Title") or text.split("\n")[0][:80]
    location = extract_field(text, "Location")
    qualification = extract_field(text, "Qualification")
    last_date = extract_field(text, "Last Date")
    apply_link = extract_field(text, "Apply Link")

    sheet.append_row([
        timestamp,
        title,
        "General",
        location,
        qualification,
        last_date,
        apply_link,
        "Telegram / Instagram"
    ])

    await update.message.reply_text("✅ Job saved & published on website!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
