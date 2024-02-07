import telegram
import asyncio


async def send_mail():
    print('send_mail')
    bot = telegram.Bot("6195527429:AAF4l0_OAktQ43p6DhWjLmRXnMv-8zRSrac")
    async with bot:
        print(await bot.get_me())
        chat_id = (await bot.get_updates())
        print(chat_id)

if __name__ == "__main__":
    asyncio.run(send_mail())