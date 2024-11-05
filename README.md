# Automatic Blog Writing Telegram Bot

This Telegram bot uses the ChatGPT API to automatically generate SEO-friendly blog articles based on user-provided topics.

## Features

- Generates SEO-optimized blog articles
- Uses OpenAI's GPT-3.5-turbo model
- Easy to use Telegram interface
- Deployable on Render

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/Speed10x/BlogWriterBot-AI
   cd blog-writer-bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a new bot on Telegram by talking to [@BotFather](https://t.me/BotFather) and get your bot token.

4. Set up your OpenAI API key by following the instructions on the [OpenAI website](https://platform.openai.com/account/api-keys).

5. Set your bot token and OpenAI API key as environment variables:
   ```
   export TELEGRAM_BOT_TOKEN=your_bot_token_here
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

6. Run the bot:
   ```
   python bot.py
   ```

## Usage

1. Start a chat with your bot on Telegram.
2. Send a topic for which you want a blog article.
3. The bot will generate and send back an SEO-friendly blog article on the given topic.

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
   - `OPENAI_API_KEY` with your OpenAI API key
6. Deploy the bot.

## License

This project is licensed under the MIT License.
