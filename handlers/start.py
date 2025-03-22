import asyncio

from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from decouple import config
from create_bot import bot
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from keyboards.start import main_menu_kb
from utils.jwt_tokens import create_access_token, decode_access_token
from utils.redis import get_redis

router = Router()

@router.message(F.text == '/start')
async def start(message: Message, state: FSMContext):
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await state.clear()
            redis = await get_redis()
            async with aiohttp.ClientSession() as session:
                async with session.post(
                        url=f'{config('API_URL')}/users/registration/',
                        json=
                        {
                            'telegram_id': message.from_user.id,
                            'username': message.from_user.username
                        }) as response:
                    if response.status == 201:

                        await redis.set(f'user:{message.from_user.id}', 'True')
                        await redis.set(
                            f'user:{message.from_user.id}:access_token',
                            f'{create_access_token(message.from_user.id)}'
                        )
                        await redis.close()
                        await asyncio.sleep(1)
                        await message.answer('Нажмите /menu, чтобы увидеть список основных команд.')


@router.message(F.text == '/menu')
async def menu(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):

        await state.clear()
        await state.update_data(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
        )
        user_data = await state.get_data()

        redis = await get_redis()
        await redis.set(
            f'user:{message.from_user.id}:access_token',
            f'{create_access_token(message.from_user.id)}'
        )
        token = await redis.get(f'user:{message.from_user.id}:access_token')
        dt = token.decode('utf-8')
        print(dt)
        headers = {
            'Authorization': f'Bearer {dt}'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f'{config('API_URL')}/dogs/', headers=headers) as response:
                print(response.status)
        if await redis.get(f'user:{user_data['telegram_id']}') is None:
            await redis.close()
            await asyncio.sleep(1)
            await message.answer(text=f'Для начала введите /start')
        else:
            await redis.close()
            await message.answer(
                text=f'Ты находишься в главном меню. Что будем делать дальше?',
                reply_markup=main_menu_kb()
            )



