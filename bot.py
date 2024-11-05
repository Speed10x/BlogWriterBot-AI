import os
import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai
from flask import Flask, request
import re

# Initialize bot, Gemini API, and Flask app
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))  # Telegram ID of the admin

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel('gemini-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')
app = Flask(__name__)

# Helper function to create inline keyboard
def create_content_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("SEO Blog Post", callback_data="seo_blog"),
                 InlineKeyboardButton("General Blog Post", callback_data="general_blog"))
    keyboard.row(InlineKeyboardButton("Generate Image", callback_data="generate_image"))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, "Welcome to the Enhanced Blog Writer Bot! You can chat with me or use the buttons below to generate content.", reply_markup=create_content_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "seo_blog":
        bot.answer_callback_query(call.id, "Please provide a topic for your SEO-optimized blog post.")
        bot.send_message(call.message.chat.id, "What topic would you like for your SEO-optimized blog post?")
    elif call.data == "general_blog":
        bot.answer_callback_query(call.id, "Please provide a topic for your general blog post.")
        bot.send_message(call.message.chat.id, "What topic would you like for your general blog post?")
    elif call.data == "generate_image":
        bot.answer_callback_query(call.id, "Please provide a description for the image you want to generate.")
        bot.send_message(call.message.chat.id, "Describe the image you want to generate:")

@bot.message_handler(commands=['admin'])
def admin_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Sorry, this command is only available to the admin.")
        return
    bot.reply_to(message, "Welcome, Admin! You have access to special commands.")

@bot.message_handler(commands=['stats'])
def stats_command(message: Message):
    # Implement stats tracking logic here
    bot.reply_to(message, "Bot usage statistics: [Placeholder for actual stats]")

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    if message.text.startswith('/'):
        bot.reply_to(message, "Unknown command. Please use /start or /help for available options.")
        return

    try:
        # Check if the message is a response to a specific prompt
        if "SEO-optimized blog post" in bot.reply_to(message, "Generating content...").text:
            prompt = f"Write a comprehensive, SEO-optimized blog article about {message.text}. Include a catchy title, introduction, main content with subheadings, and a conclusion."
        elif "general blog post" in bot.reply_to(message, "Generating content...").text:
            prompt = f"Write an engaging blog post about {message.text}. Include a title, introduction, main content, and conclusion."
        elif "image you want to generate" in bot.reply_to(message, "Generating image description...").text:
            prompt = f"Describe in detail an image that represents: {message.text}"
        else:
            # General chat interaction
            prompt = f"You are a friendly AI assistant. Respond to the following message: {message.text}"

        response = text_model.generate_content(prompt)
        content = response.text

        # Split long messages if necessary
        if len(content) > 4000:
            for i in range(0, len(content), 4000):
                bot.send_message(message.chat.id, content[i:i+4000])
        else:
            bot.send_message(message.chat.id, content)

        # Offer more options after generating content
        bot.send_message(message.chat.id, "What would you like to do next?", reply_markup=create_content_keyboard())

    except Exception as e:
        bot.reply_to(message, f"An error occurred while generating content: {str(e)}")

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
