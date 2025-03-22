import asyncio
from create_bot import bot, dp, scheduler

from handlers.start import router as start_module
from handlers.dog import router as dog_module


# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()

    dp.include_router(start_module)
    dp.include_router(dog_module)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())