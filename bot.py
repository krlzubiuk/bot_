import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Hugging Face API Token — берется из переменной окружения
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HF_API_KEY = os.getenv("HF_API_KEY")

# 💬 Отправка запроса в Hugging Face
def generate_response_from_hf(prompt: str) -> str:
    try:
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}"
        }
        payload = {
            "inputs": prompt
        }

        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            return f"❌ Hugging Face API помилка: {result['error']}"
        else:
            return "⚠️ Не вдалося зчитати відповідь з Hugging Face."

    except Exception as e:
        return f"❌ Hugging Face API помилка: {e}"

# 🤖 Обработка сообщений от пользователя
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print("📩 Отримано повідомлення:", user_message)
    bot_response = generate_response_from_hf(user_message)
    print("🤖 Відповідь від HF:", bot_response)
    await update.message.reply_text(bot_response)

# 📌 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Я бот на базі Hugging Face. Напиши мені щось!")

# 🚀 Запуск бота
def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN or not HF_API_KEY:
        print("❌ TELEGRAM_TOKEN або HF_API_KEY не встановлено!")
        return

    print("✅ Бот запущено... Очікуємо повідомлень у Telegram")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
