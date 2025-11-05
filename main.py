import os
from dotenv import load_dotenv
load_dotenv()
import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Simple content lists
jokes = [
    "I told my computer I needed a break — it said 'No problem, I'll go to sleep.'",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "I would tell you a UDP joke, but you might not get it."
]

motivations = [
    "Small progress each day adds up to big results. Keep going!",
    "You are capable of more than you think — try one small bold step today.",
    "Mistakes are proof you are trying. Learn, adjust, repeat."
]

productivity_tips = [
    "Use the Pomodoro technique: 25 minutes focused, 5 minutes break.",
    "Tackle your hardest task first — your future self will thank you.",
    "Batch similar tasks together to reduce context switching."
]

# Keyboard labels
BUTTON_JOKE = "Tell me a joke"
BUTTON_MOTIVATE = "Motivate me"
BUTTON_PRODUCTIVITY = "Give me a productivity tip"

reply_keyboard = ReplyKeyboardMarkup(
    [[BUTTON_JOKE], [BUTTON_MOTIVATE], [BUTTON_PRODUCTIVITY]],
    one_time_keyboard=False,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command: send welcome text and show reply keyboard."""
    user_first = update.effective_user.first_name if update.effective_user else "there"
    text = (
        f"Hi {user_first}! I'm a friendly bot. Choose an option below or type your own message:\n\n"
        f"• {BUTTON_JOKE}\n"
        f"• {BUTTON_MOTIVATE}\n"
        f"• {BUTTON_PRODUCTIVITY}"
    )
    await update.message.reply_text(text, reply_markup=reply_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Respond to the three keyboard buttons with a random selection from the lists."""
    if not update.message or not update.message.text:
        return
    text = update.message.text.strip()

    if text == BUTTON_JOKE:
        choice = random.choice(jokes)
        await update.message.reply_text(choice)
    elif text == BUTTON_MOTIVATE:
        choice = random.choice(motivations)
        await update.message.reply_text(choice)
    elif text == BUTTON_PRODUCTIVITY:
        choice = random.choice(productivity_tips)
        await update.message.reply_text(choice)
    else:
        # Fallback: simple echo + help hint
        hint = (
            "I didn't recognize that option. Try one of the buttons or type /start to see them again.\n\n"
            f"Options: {BUTTON_JOKE} | {BUTTON_MOTIVATE} | {BUTTON_PRODUCTIVITY}"
        )
        await update.message.reply_text(hint)

def main() -> None:
    """Start the bot. Must be run as a script."""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found. Please create a .env file with BOT_TOKEN=your_token_here")
        raise SystemExit("Missing BOT_TOKEN environment variable")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
