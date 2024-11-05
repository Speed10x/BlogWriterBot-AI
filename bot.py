import os
import telebot
from telebot.types import Message
from openai import OpenAI
from flask import Flask, request

# Initialize bot, OpenAI client, and Flask app
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, "Welcome to the Blog Writer Bot! Send me a topic, and I'll generate an SEO-friendly blog article for you.")

@bot.message_handler(func=lambda message: True)
def generate_blog(message: Message):
    topic = message.text
    bot.reply_to(message, f"Generating a blog article about '{topic}'. This may take a moment...")

    try:
        # Generate blog content using ChatGPT
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert SEO-friendly blog writer."},
                {"role": "user", "content": f"Write a comprehensive, SEO-optimized blog article about {topic}. Include a catchy title, introduction, main content with subheadings, and a conclusion."}
            ],
            max_tokens=1000
        )

        blog_content = response.choices[0].message.content

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
    bot.set_webhook(url='https://your-app-name.onrender.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))