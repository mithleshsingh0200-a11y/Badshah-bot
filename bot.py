import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- FINAL UPDATED TOKEN ---
TOKEN = '8044105919:AAFLYGZhW1ItYqXkEHHAnFPpMta4cOgPZZM'

class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    HTTPServer(('0.0.0.0', port), HealthCheck).serve_forever()

class BadshahEngine:
    def __init__(self):
        self.last_period = None
        self.mode = "WinGo_30S"

    async def fetch_now(self, context, chat_id):
        try:
            g_id = '1' if '30S' in self.mode else '2'
            # Sahi URL aur logic yahan set hai
            url = f"https://api.9987up.com/api/web/game/v1/wingo/last-results?gameId={g_id}"
            response = requests.get(url, timeout=15)
            data = response.json()['data'][0]
            
            curr_p = data['issueNumber']
            
            if curr_p != self.last_period:
                self.last_period = curr_p
                res = "BIG" if int(data['number']) >= 5 else "SMALL"
                color = "RED 🔴" if int(data['number']) % 2 == 0 else "GREEN 🟢"
                
                msg = f"🎯 *ROUND:* `{curr_p}`\n🎰 *RESULT:* `{res}`\n🎨 *COLOR:* `{color}`"
                await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
        except Exception as e:
            print(f"Error: {e}")

engine = BadshahEngine()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("WinGo 30S", callback_data='WinGo_30S')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('🎮 *Select Game Mode:*', reply_markup=reply_markup, parse_mode='Markdown')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    engine.mode = query.data
    await query.edit_message_text(f"✅ *{query.data} SELECTED*\n🚀 Agle round se prediction shuru hogi...")
    
    # Purane jobs hatane ke liye
    for job in context.job_queue.get_jobs_by_name(str(query.message.chat_id)):
        job.schedule_removal()
    
    # Naya prediction cycle shuru (Har 15 second)
    context.job_queue.run_repeating(engine.fetch_now, interval=15, first=1, chat_id=query.message.chat_id, name=str(query.message.chat_id))

if __name__ == '__main__':
    Thread(target=run_server, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("🚀 BOT POLLING STARTING...")
    app.run_polling(drop_pending_updates=True)
