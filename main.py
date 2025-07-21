import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import json
from utils import get_career_suggestions, generate_learning_roadmap

# Load career data and prompt templates
with open('career_data.json') as f:
    career_data = json.load(f)

with open('prompts.json') as f:
    prompts = json.load(f)

# Telegram bot token
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Define a logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=prompts['start'])

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    career_suggestions = get_career_suggestions(user_input, career_data)
    if career_suggestions:
        for career in career_suggestions:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=prompts['career_suggestion'].format(
                career_name=career['name'],
                summary=career['summary'],
                skills=', '.join(career['skills']),
                job_demand=career['job_demand'],
                alignment=career['alignment'],
                outlook=career['outlook']
            ))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=prompts['interested'])
            # Wait for user response
            user_response = await context.bot.wait_for_message(chat_id=update.effective_chat.id)
            if user_response.text.lower() == 'yes':
                learning_roadmap = generate_learning_roadmap(career['name'], career['skills'])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=prompts['learning_roadmap'].format(
                    roadmap='\n'.join(learning_roadmap)
                ))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=prompts['motivational_tips'])
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=prompts['alternative_careers'])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=prompts['no_career_suggestions'])

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
