import openai
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# 🔐 Завантажуємо змінні середовища
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# 💬 Генерація відповіді від ChatGPT
def generate_openai_response(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # або gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Ти — доброзичливий Telegram-бот на базі ChatGPT."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            request_timeout=10  # ⏱️ таймаут OpenAI-запиту
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ OpenAI error:", e)
        return f"❌ Помилка при зверненні до OpenAI: {e}"

# 🔄 Обробка вхідних повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print("📩 Отримано повідомлення:", user_message)

    bot_response = generate_openai_response(user_message)

    print("🤖 Відповідь від OpenAI:", bot_response)
    await update.message.reply_text(bot_response[:4000])  # 🔒 Telegram максимум 4096 символів

# 📌 Стартова команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('👋 Привіт! Я бот на базі ChatGPT. Напиши мені щось!')

# 🚀 Запуск бота
def main():
    print("✅ Бот запущено... Очікуємо повідомлень у Telegram")

    application = Application.builder().token(TELEGRAM_TOKEN).concurrent_updates(False).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
