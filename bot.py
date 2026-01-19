# bot.py
import asyncio
import logging
from pyrogram import idle

from config import APP_NAME, TIMEZONE
from core.client import get_client
from core.dispatcher import setup_dispatcher

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s | {APP_NAME} | %(levelname)s | %(message)s'
)
logger = logging.getLogger(APP_NAME)

async def main():
    # Telegram client init
    app = get_client()

    # Setup command handlers / dispatcher
    setup_dispatcher(app)

    # Start the bot
    await app.start()
    logger.info("Bot started successfully!")
    
    # Idle to keep bot running
    await idle()
    
    # Stop gracefully
    await app.stop()
    logger.info("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot exited.")
