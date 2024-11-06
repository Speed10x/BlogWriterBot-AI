# Multi-Personality Telegram Bot

This Telegram bot uses the Google Gemini API to provide multiple functionalities, including SEO-optimized blog post generation, a virtual girlfriend experience, and general chat capabilities.

## Features

1. SEO Blog Post Generation Mode:
   - Generates high-quality, SEO-optimized blog posts based on user-provided topics
   - Performs keyword density checks and readability analysis
   - Provides SEO reports with suggestions for improvement

2. Virtual Girlfriend Mode:
   - Simulates a friendly, engaging companion using casual language
   - Provides supportive messages and friendly conversations

3. General Chat Mode:
   - Offers regular conversational responses on various topics
   - Provides information and answers questions

4. Admin Commands:
   - View bot usage statistics
   - Access admin-only features

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/multi-personality-bot.git
   cd multi-personality-bot
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
2. Use the /start or /help command to get started.
3. Choose a mode using the provided buttons:
   - SEO Blog Post
   - Virtual Girlfriend
   - General Chat
4. Interact with the bot based on the selected mode.
5. Use the /mode command to switch between modes at any time.

## Admin Commands

- `/admin`: Access admin-only features
- `/stats`: View bot usage statistics

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
