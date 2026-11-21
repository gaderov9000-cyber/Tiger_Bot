import os, json, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "9051644157:AAGx24lRzyIyO6mjFxIeYqBexybOm-JgrKM"
ADMIN_ID = 8090000000
DATA_FILE = "users.json"
logging.basicConfig(level=logging.INFO)

def load_users():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🆕 انشاء حساب", callback_data="create")],
        [InlineKeyboardButton("🔑 تسجيل دخول", callback_data="login")],
        [InlineKeyboardButton("👤 حسابي", callback_data="my")],
        [InlineKeyboardButton("🆘 دعم", callback_data="support")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا فيك بـ Tiger Bot 🐯\nاختار من القائمة:", reply_markup=main_menu())

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "create":
        context.user_data["step"] = "create_user"
        await q.message.reply_text("ابعت اسم المستخدم:")
    elif q.data == "login":
        context.user_data["step"] = "login_user"
        await q.message.reply_text("ابعت اسم المستخدم:")
    elif q.data == "my":
        users = load_users()
        u = users.get(str(q.from_user.id))
        await q.message.reply_text("الايدي: " + str(u.get('username')) + " حسابك: " + str(q.from_user.id))
        await q.message.reply_text("الايدي: " + str(u.get('username')) + " حسابك: " + str(q.from_user.id))
        await q.message.reply_text("ما عندك حساب بعد، اكبس انشاء حساب", reply_markup=main_menu())
    elif q.data == "support":
        context.user_data["step"] = "support"
      
await q.message.reply_text("الباسورد: " + str(u.get('username')) + " الايدي: " + str(u.get('password')))
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("step")
    text = update.message.text.strip()
    uid = str(update.effective_user.id)
    users = load_users()

    if step == "create_user":
        context.user_data["tmp_user"] = text
        context.user_data["step"] = "create_pass"
        await update.message.reply_text("ابعت كلمة السر:")
        return
    if step == "create_pass":
        users[uid] = {"username": context.user_data.get("tmp_user"), "password": text}
        save_users(users)
        context.user_data["step"] = None
        await update.message.reply_text("تم انشاء حسابك بنجاح ✅", reply_markup=main_menu())
        return
    if step == "login_user":
        for k, v in users.items():
            if v.get("username") == text:
                context.user_data["tmp_login"] = k
                context.user_data["step"] = "login_pass"
                await update.message.reply_text("ابعت كلمة السر:")
                return
        await update.message.reply_text("الاسم مو موجود")
        return
    if step == "login_pass":
        k = context.user_data.get("tmp_login")
        if k and users.get(k, {}).get("password") == text:
            await update.message.reply_text("تم تسجيل الدخول ✅", reply_markup=main_menu())
        else:
            await update.message.reply_text("كلمة السر غلط")
        context.user_data["step"] = None
        return
    if step == "support":
        context.user_data["step"] = None
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"رسالة دعم جديدة من @{update.effective_user.username} ({uid}):\n\n{text}")
        await update.message.reply_text("وصلت رسالتك للادمن، رح يرد عليك قريبا ✅", reply_markup=main_menu())
        return
    await update.message.reply_text("اختار من القائمة:", reply_markup=main_menu())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling()

if __name__ == "__main__":
    main()
