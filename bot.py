import os
import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import google.generativeai as genai
from flask import Flask, request
import re
from textstat import flesch_kincaid_grade, flesch_reading_ease

# Initialize bot, Gemini API, and Flask app
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
ADMIN_ID = int(os.environ.get('ADMIN_ID'))

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
app = Flask(__name__)

# Store user states and modes
user_states = {}
user_modes = {}

def create_mode_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("SEO Blog Post", callback_data="seo_mode"),
                 InlineKeyboardButton("Virtual Girlfriend", callback_data="girlfriend_mode"))
    keyboard.row(InlineKeyboardButton("General Chat", callback_data="general_mode"))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, "Welcome to the Multi-Personality Bot! Choose a mode to get started:", reply_markup=create_mode_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in ["seo_mode", "girlfriend_mode", "general_mode"]:
        user_modes[call.message.chat.id] = call.data
        if call.data == "seo_mode":
            bot.answer_callback_query(call.id, "SEO Blog Post mode activated. Please provide a topic for your blog post.")
            bot.send_message(call.message.chat.id, "What topic would you like for your SEO-optimized blog post?")
        elif call.data == "girlfriend_mode":
            bot.answer_callback_query(call.id, "Virtual Girlfriend mode activated. How can I brighten your day?")
            bot.send_message(call.message.chat.id, "Hey there! 😊 How's your day going, sweetie?")
        else:
            bot.answer_callback_query(call.id, "General Chat mode activated. What would you like to talk about?")
            bot.send_message(call.message.chat.id, "I'm ready for a chat! What's on your mind?")

@bot.message_handler(commands=['mode'])
def change_mode(message: Message):
    bot.reply_to(message, "Choose a mode:", reply_markup=create_mode_keyboard())

@bot.message_handler(commands=['admin'])
def admin_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Sorry, this command is only available to the admin.")
        return
    bot.reply_to(message, "Welcome, Admin! You have access to special commands.")

@bot.message_handler(commands=['stats'])
def stats_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Sorry, this command is only available to the admin.")
        return
    # Implement stats tracking logic here
    stats = f"Total users: {len(user_modes)}\n"
    stats += f"SEO mode users: {sum(1 for mode in user_modes.values() if mode == 'seo_mode')}\n"
    stats += f"Girlfriend mode users: {sum(1 for mode in user_modes.values() if mode == 'girlfriend_mode')}\n"
    stats += f"General chat users: {sum(1 for mode in user_modes.values() if mode == 'general_mode')}"
    bot.reply_to(message, stats)

def generate_seo_content(topic):
    prompt = f"""
    Write a comprehensive, SEO-optimized blog article about {topic}. 
    Include the following:
    1. A catchy title with the main keyword
    2. An engaging introduction
    3. Main content with at least 3 subheadings
    4. A conclusion with a call-to-action
    5. Ensure proper keyword density and use of related terms
    6. Aim for a Flesch-Kincaid Grade Level of 8-10 and a Flesch Reading Ease score of 60-70
    """
    response = model.generate_content(prompt)
    content = response.text

    # Perform SEO checks
    keyword = topic.lower()
    keyword_density = content.lower().count(keyword) / len(content.split()) * 100
    fk_grade = flesch_kincaid_grade(content)
    fk_ease = flesch_reading_ease(content)

    seo_report = f"\n\nSEO Report:\n"
    seo_report += f"Keyword density: {keyword_density:.2f}% (aim for 1-3%)\n"
    seo_report += f"Flesch-Kincaid Grade Level: {fk_grade:.1f} (aim for 8-10)\n"
    seo_report += f"Flesch Reading Ease: {fk_ease:.1f} (aim for 60-70)\n"

    return content + seo_report

def generate_girlfriend_response(message):
    prompt = f"""
    You are a friendly, caring virtual girlfriend. Respond to the following message in a warm, 
    supportive manner, using casual language and emojis where appropriate: {message}
    Keep the response brief and engaging, as if texting a partner.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_general_chat_response(message):
    prompt = f"""
    You are a helpful AI assistant. Respond to the following message in a friendly and 
    informative manner: {message}
    Provide a concise and engaging response.
    """
    response = model.generate_content(prompt)
    return response.text

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    chat_id = message.chat.id
    mode = user_modes.get(chat_id, "general_mode")

    try:
        if mode == "seo_mode":
            content = generate_seo_content(message.text)
        elif mode == "girlfriend_mode":
            content = generate_girlfriend_response(message.text)
        else:
            content = generate_general_chat_response(message.text)

        # Split long messages if necessary
        if len(content) > 4000:
            for i in range(0, len(content), 4000):
                bot.send_message(chat_id, content[i:i+4000])
        else:
            bot.send_message(chat_id, content)

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
