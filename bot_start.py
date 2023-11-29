import asyncio
from aiogram import Dispatcher, Bot
from bot_answers import bot_commands, bot_messages, state_handler

bot = Bot("5647971616:AAEUmfKipJ7t2rk-tbIHcYHGfZWNTyg5WaM")


async def main():
    
    dp = Dispatcher()

    dp.include_routers(
        state_handler.router,
        bot_commands.router,
        bot_messages.router,

    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())