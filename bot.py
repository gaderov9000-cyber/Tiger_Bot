import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN") or "8000000000:AAH-TOKEN-HERE"
ADMIN_ID = 8090000000
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user(data, user_id):
    uid = str(user_id)
    if uid not in data["users"]:
        data["users"][uid] = {"balance": 0, "invited": 0, "referrer": None}
    return data["users"][uid]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    user = update.effective_user
    me = get_user(data, user.id)

    if context.args:
        try:
            ref_id = int(context.args[0])
            if ref_id != user.id and me["referrer"] is None:
                me["referrer"] = ref_id
                ref = get_user(data, ref_id)
                ref["invited"] += 1
                ref["balance"] += 10
        except:
            pass

    save_data(data)

    keyboard = [
        [InlineKeyboardButton("💰 رصيدي", callback_data="balance")],
        [InlineKeyboardButton("👥 دعوة أصدقاء", callback_data="invite")],
        [InlineKeyboardButton("🎁 هدية يومية", callback_data="daily")]
    ]
    text = f"أهلاً {user.first_name} 👋\n\nمرحباً بك في بوت النمر
