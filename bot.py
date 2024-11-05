import os
import telebot
from telebot.types import Message
import google.generativeai as genai
from flask import Flask, request

# Initialize bot, Gemini API, and Flask app
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, "Welcome to the Blog Writer Bot! Send me a topic, and I'll generate an SEO-friendly blog article for you.")

@bot.message_handler(func=lambda message: True)
def generate_blog(message: Message):
    topic = message.text
    bot.reply_to(message, f"Generating a blog article about '{topic}'. This may take a moment...")

    try:
        # Generate blog content using Gemini
        prompt = f"Write a comprehensive, SEO-optimized blog article about {topic}. Include a catchy title, introduction, main content with subheadings, and a conclusion."
        response = model.generate_content(prompt)

        blog_content = response.text

        # Send the generated blog content to the user
        bot.send_message(message.chat.id, blog_content)

    except Exception as e:
        bot.reply_to(message, f"An error occurred while generating the blog article: {str(e)}")

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://file-converter-bot-98ux.onrender.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
