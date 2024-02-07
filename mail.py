import telegram
import asyncio


async def send_mail():
    print('send_mail')
    bot = telegram.Bot("Token")
    async with bot:
        print(await bot.get_me())
        chat_id = (await bot.get_updates())
        print(chat_id)

if __name__ == "__main__":
    asyncio.run(send_mail())