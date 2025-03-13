import os
from io import BytesIO
from pkgutil import get_data

from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile

from keyboards.dog import dog_menu_kb
from settings import API_URL

router = Router()

class DogState(StatesGroup):
    dog_add_start = State()
    dog_add_name = State()
    dog_add_gender = State()
    dog_add_breed = State()
    dog_add_color = State()
    dog_add_birth = State()
    #dog_add_photo = State()
    #dog_add_extra = State()

@router.callback_query(F.data == 'dogs')
async def dogs_menu(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    headers = {
        'Authorization': f'Bearer {state_data['access_token']}',
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{API_URL}/dogs/', headers=headers) as response:
            response_data = await response.json()
            print(response_data)
    pet_names = []
    for el in response_data:
        pet_names.append(el['name'])
    print(pet_names)
    await call.message.answer(f'Твои питомцы:\n{pet_names}')
    await call.message.answer(text=f'Что дальше?',
                         reply_markup=dog_menu_kb())


@router.callback_query(F.data == 'dog_add')
async def dog_add_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text=f'Сейчас добавим собачку. Введи ее кличку.')
    await state.set_state(DogState.dog_add_name)


@router.message(F.text, DogState.dog_add_name)
async def dog_add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=f'Если мальчик, то введи 1, а если девочка, то 2.')
    await state.set_state(DogState.dog_add_gender)


@router.message(F.text, DogState.dog_add_gender)
async def dog_add_gender(message: Message, state: FSMContext):
    gender_list = ["1", "2"]
    if message.text in gender_list:
        await state.update_data(gender=message.text)
        await message.answer(text=f'Укажи породу, только напиши полностью и правильно.')
        await state.set_state(DogState.dog_add_breed)
    else:
        await message.answer(text=f'Если мальчик, то введи 1, а если девочка, то 2.')
        await state.set_state(DogState.dog_add_name)



@router.message(F.text, DogState.dog_add_breed)
async def dog_add_breed(message: Message, state: FSMContext):
    await state.update_data(breed=message.text)
    await message.answer(text=f'Какого цвета основной окрас?')
    await state.set_state(DogState.dog_add_color)


@router.message(F.text, DogState.dog_add_color)
async def dog_add_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    await message.answer(text=f'А когда родился? Формат: 2000-12-31.')
    await state.set_state(DogState.dog_add_birth)


@router.message(F.text, DogState.dog_add_birth)
async def dog_add_birth(message: Message, state: FSMContext):
    await state.update_data(date_of_birth=message.text)

    state_data = await state.get_data()
    print(f'добавление: {state_data}')
    headers = {
        'Authorization': f'Bearer {state_data['access_token']}',
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/dogs/', headers=headers, json={
            'name' : state_data['name'],
            'gender' : state_data['gender'],
            'breed' : state_data['breed'],
            'color' : state_data['color'],
            'date_of_birth' : state_data['date_of_birth'],
        }) as response:
            if response.status == 201:
                reserved_data = {
                    'telegram_id': state_data['telegram_id'],
                    'username': state_data['username'],
                    'access_token': state_data['access_token'],
                }
                await state.clear()
                await state.update_data(reserved_data)
                state_data = await state.get_data()
                print(f'после добавления: {state_data}')
                await message.answer('Собачка добавлена.')
            else:
                await message.answer('Начнем заново. Введи кличку собачки.')
                await state.set_state(DogState.dog_add_start)