import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація клієнта OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Функція генерації відповіді
def generate_openai_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти — доброзичливий Telegram-бот на базі ChatGPT."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            timeout=10
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Помилка при зверненні до OpenAI: {e}"

# Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    bot_response = generate_openai_response(user_message)
    await update.message.reply_text(bot_response)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('👋 Привіт! Я бот на базі ChatGPT. Напиши мені щось!')

# Запуск бота
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущено... Очікуємо повідомлень")
    application.run_polling()

if __name__ == '__main__':
    main()
