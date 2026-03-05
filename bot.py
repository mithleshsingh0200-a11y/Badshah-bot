import random, asyncio, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = '8044105919:AAE_lP2bsbcekqmTX2Y3e6lRkKX7EBbY6Pg'

class BadshahEngine:
    def get_pred(self):
        pats = ["DRAGON 🐉", "ZIG-ZAG 📈", "MIRROR 🪞", "CHIP MARKET 🤖"]
        sz, cl = random.choice(["BIG", "SMALL"]), random.choice(["RED", "GREEN"])
        if random.random() < 0.15: cl = random.choice(["🔴+🟣 Jackpot", "🟢+🟣 Jackpot"])
        return {"s": sz, "c": cl, "p": random.choice(pats)}

engine = BadshahEngine()

async def start(u, c):
    kb = [[InlineKeyboardButton("⏱️ 30S MODE", callback_data='30')], [InlineKeyboardButton("⏱️ 60S MODE", callback_data='60')]]
    await u.message.reply_text("👑 *BADSHAH AI V240*\nChoose Mode:", reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def auto_loop(c: ContextTypes.DEFAULT_TYPE):
    res = engine.get_pred()
    msg = f"👑 *BADSHAH AI*\n━━━━━━━━\n🆔 PERIOD: `{time.strftime('%M%S')}`\n📊 PATTERN: {res['p']}\n📏 SIZE: *{res['s']}*\n🎨 COLOUR: *{res['c']}*\n━━━━━━━━\n✅ WINNING!!"
    await c.bot.send_message(chat_id=c.job.chat_id, text=msg, parse_mode='Markdown')

async def button(u, c):
    q = u.callback_query
    await q.answer()
    sec = int(q.data)
    for j in c.job_queue.get_jobs_by_name(str(q.message.chat_id)): j.schedule_removal()
    c.job_queue.run_repeating(auto_loop, interval=sec, first=1, chat_id=q.message.chat_id, name=str(q.message.chat_id))
    await q.edit_message_text(f"✅ {sec}s Mode Active 24/7!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
