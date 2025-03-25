import os
import telebot
import openai
from dotenv import load_dotenv  # ✅ Safe तरीके से API Keys लोड करने के लिए

# ✅ API Keys को .env फाइल से लोड करो
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ OpenAI Client Initialize करें
openai.api_key = OPENAI_API_KEY 

# ✅ Telegram Bot Initialize करें
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_openai_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"⚠ OpenAI Error: {str(e)}"

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    user_input = message.text
    ai_response = get_openai_response(user_input)
    bot.reply_to(message, ai_response)

print("🤖 Telegram AI Bot is Running... (Waiting for messages...)")

# ✅ Google Colab या Server में Background Thread में चलाएं
import threading

def start_bot():
    bot.polling(non_stop=True)

thread = threading.Thread(target=start_bot)
thread.start()
