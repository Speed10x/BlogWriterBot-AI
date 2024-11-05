# Enhanced Blog Writer Telegram Bot

This Telegram bot uses the Google Gemini API to generate various types of content, including SEO-friendly blog articles, general blog posts, and image descriptions. It also features interactive chat capabilities and admin commands.

## Features

- Generates SEO-optimized blog articles
- Creates general blog posts
- Provides image descriptions (for potential image generation)
- Interactive chat functionality
- Button interface for easy content generation
- Admin-only commands
- Uses Google's Gemini-Pro model
- Easy to use Telegram interface
- Deployable on Render

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/Speed10x/BlogWriterBot-AI
   cd enhanced-blog-writer-bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a new bot on Telegram by talking to [@BotFather](https://t.me/BotFather) and get your bot token.

4. Set up your Google Gemini API key by following the instructions on the [Google AI Studio website](https://makersuite.google.com/app/apikey).

5. Set your bot token, Gemini API key, and admin Telegram ID as environment variables:
   ```
   export TELEGRAM_BOT_TOKEN=your_bot_token_here
   export GEMINI_API_KEY=your_gemini_api_key_here
   export ADMIN_ID=your_telegram_id_here
   ```

6. Run the bot:
   ```
   python bot.py
   ```

## Usage

1. Start a chat with your bot on Telegram.
2. Use the buttons to generate different types of content:
   - SEO Blog Post
   - General Blog Post
   - Generate Image (description)
3. Chat with the bot for general interactions.
4. Admin can use special commands like /admin and /stats.

## Admin Commands

- `/admin`: Access admin-only features
- `/stats`: View bot usage statistics (placeholder)

## Deployment on Render

1. Fork this repository to your GitHub account.
2. Create a new Web Service on Render.
3. Connect your GitHub account and select the forked repository.
4. Set the following:
   - Environment: Docker
   - Build Command: (leave empty)
   - Start Command: (leave empty)
5. Add the environment variables:
   - `TELEGRAM_BOT_TOKEN` with your bot token
   - `GEMINI_API_KEY` with your Google Gemini API key
   - `ADMIN_ID` with your Telegram user ID (for admin commands)
6. Deploy the bot.

## License

This project is licensed under the MIT License.
