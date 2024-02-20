import telegram
import asyncio
import os
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Use os.getenv to retrieve environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
async def send_mail():
    print('send_mail')
    bot = telegram.Bot(TELEGRAM_TOKEN)
    async with bot:
        print(await bot.get_me())
        chat_id = (await bot.get_updates())
        print(chat_id)

if __name__ == "__main__":
    asyncio.run(send_mail())