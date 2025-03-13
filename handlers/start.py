from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from custom_funcs.jwt_tokens import get_refresh_token_by_id, refreshed_tokens_by_old_refresh, verify_jwt_token, \
    update_refresh_token
from descriptions import menu_descs as mtxt
from create_bot import bot
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
from keyboards.main_menu import main_menu_kb
from settings import API_URL

router = Router()

class Start(StatesGroup):
    registration = State()
    recreate_jwt = State()

base_data = {
    'telegram_id':None,
    'username':None,
    'refresh_token':None,
    'access_token':None,
}

@router.message(F.text == '/start' or F.text == '/меню' or F.text == '/menu')
async def start(message: Message, state: FSMContext):
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            # заполнение базового словаря
            if base_data['telegram_id'] is None or base_data['username'] is None:
                await state.update_data(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                )
                state_data = await state.get_data()
                base_data['telegram_id'] = state_data['telegram_id']
                base_data['username'] = state_data['username']

            # обновление username если пользователь сменил никнейм в тг
            if base_data['username'] != message.from_user.username:
                # !!! добавить обновление в БД
                base_data['username'] = message.from_user.username


            refresh_token_from_instance = await get_refresh_token_by_id(base_data['telegram_id'])
            if refresh_token_from_instance:
                base_data['refresh_token'] = refresh_token_from_instance
            else:
                await message.answer(
                    text=f'Привет! Для входа придумай короткий код (аки пароль). Он пригодится для входа в дальнейшем.'
                )
                await state.set_state(Start.registration)

            verify_refresh = await verify_jwt_token(base_data['refresh_token'])
            if verify_refresh == 200:
                if base_data['access_token'] is None:
                    refreshed_tokens = await refreshed_tokens_by_old_refresh(refresh_token_from_instance)
                    base_data['access_token'], base_data['refresh_token'] = refreshed_tokens['access'], refreshed_tokens['refresh']
                    await update_refresh_token(base_data['telegram_id'], refreshed_tokens['refresh'])
                    await state.clear()

                verify_access = await verify_jwt_token(base_data['access_token'])
                if verify_access == 200:
                    await message.answer(text=f'{mtxt.menu_welcome_text}\n\n'
                                              f'{mtxt.menu_pet_button}\n'
                                              f'{mtxt.menu_pet_search_button}\n'
                                              f'{mtxt.menu_vets_button}\n'
                                              f'{mtxt.menu_walks_button}\n'
                                              f'{mtxt.menu_guides_button}\n'
                                              f'{mtxt.menu_profile_button}',
                                         reply_markup=main_menu_kb())
            elif verify_refresh == 401:
                await message.answer(
                    text=f'Введи пароль.'
                )
                await state.set_state(Start.recreate_jwt)


@router.message(F.text, Start.registration)
async def registration(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/users/registration/', data=await state.get_data()) as response:
            if response.status == 201:
                await state.clear()
                await message.answer('Регистрация успешна. Введи /start | /menu | /меню , чтобы попасть в главное меню.')
            else:
                await message.answer(
                    f'Введи другой код.'
                )
                await state.set_state(Start.registration)


@router.message(F.text, Start.recreate_jwt)
async def recreate_jwt(message: Message, state: FSMContext):
    await state.update_data(telegram_id=message.from_user.id, password=message.text)
    state_data = await state.get_data()
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/auth/jwt/create/', json={
            'telegram_id': state_data['telegram_id'],
            'password': state_data['password'],
        }) as response:
            if response.status == 200:
                tokens = await response.json()
                base_data['access_token'], base_data['refresh_token'] = tokens['access'], tokens['refresh']
                await update_refresh_token(base_data['telegram_id'], tokens['refresh'])
                await state.clear()
                await message.answer('Доступ восстановлен.\nВведи /start | /menu | /меню , чтобы попасть в главное меню.')
            else:
                await message.answer(
                    f'Пароль неверный.'
                )
                await state.set_state(Start.recreate_jwt)




