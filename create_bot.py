import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.fsm.storage.redis import RedisStorage
from redis import Redis

storage = RedisStorage.from_url(config('REDIS_URL'))
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
# admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TELEGRAM_BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)