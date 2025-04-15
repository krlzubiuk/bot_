import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"  # или замени на свою модель

API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Я бот на базі Hugging Face. Напиши щось!")

def query_huggingface(prompt):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        if response.status_code == 200:
            result = response.json()
            return result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "🤖 Відповідь відсутня.")
        else:
            return f"❌ Hugging Face
