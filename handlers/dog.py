from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from decouple import config

from keyboards.dog import dog_menu_kb, only_add_dog_kb

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

@router.callback_query(F.data == 'dogs_menu')
async def dogs_menu(call: CallbackQuery):
    await call.message.answer(text=
                              f'Меню управления твоими собачками и их задачами.\n',
                              reply_markup=dog_menu_kb()
                                  )


@router.callback_query(F.data == 'dog_add')
async def dog_add_start(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text=f'Сейчас добавим собачку. Всего потребуется 5 шагов.\n'
                                   f' Шаг 1: введи ее кличку.')
    await state.set_state(DogState.dog_add_name)


@router.message(F.text, DogState.dog_add_name)
async def dog_add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=f'Шаг 2: введи м для мальчика или ж для девочки.')
    await state.set_state(DogState.dog_add_gender)


@router.message(F.text, DogState.dog_add_gender)
async def dog_add_gender(message: Message, state: FSMContext):
    gender_options = ('м', 'ж', 'М', 'Ж',)
    if message.text in gender_options:
        await state.update_data(gender=message.text)
        await message.answer(text=f'Шаг 3: укажи породу, только напиши полностью и правильно.')
        await state.set_state(DogState.dog_add_breed)
    else:
        await message.answer(
            text=f'Ты сделал что-то не то...\nВведи 1 для мальчика или 2 для девочки.')
        await state.set_state(DogState.dog_add_gender)


@router.message(F.text, DogState.dog_add_breed)
async def dog_add_breed(message: Message, state: FSMContext):
    await state.update_data(breed=message.text)
    await message.answer(text=f'Шаг 4: укажи основной окрас.')
    await state.set_state(DogState.dog_add_color)


@router.message(F.text, DogState.dog_add_color)
async def dog_add_color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    await message.answer(text=f'Шаг 5: Введи дату рождения.\n'
                              f'(Формат для примера: 2000-12-31. Цифрами через дефис.)')
    await state.set_state(DogState.dog_add_birth)


@router.message(F.text, DogState.dog_add_birth)
async def dog_add_birth(message: Message, state: FSMContext):
    await state.update_data(date_of_birth=message.text)

    state_data = await state.get_data()
    headers = {

    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{config('API_URL')}/dogs/', headers=headers, json={
            'name' : state_data['name'],
            'gender' : state_data['gender'],
            'breed' : state_data['breed'],
            'color' : state_data['color'],
            'date_of_birth' : state_data['date_of_birth'],
        }) as response:
            if response.status == 201:
                if state_data['gender'] == '1':
                    await message.answer(f'Пёс по имени {state_data['name']} добавлен.\n'
                                         f'Его порода {state_data['breed']}.\n'
                                         f'Имеет {state_data['color']} окрас.\n'
                                         f'Родился {state_data['date_of_birth']}.\n'
                                         )
                    await state.clear()
                    await message.answer('Нажми /start.')
                else:
                    await message.answer(f'Собачка по имени {state_data['name']} добавлена.\n'
                                         f'Ее порода {state_data['breed']}.\n'
                                         f'Имеет {state_data['color']} окрас.\n'
                                         f'Родилась {state_data['date_of_birth']}.\n'
                                         )
                    await state.clear()
                    await message.answer('Нажми /start.')
            else:
                await message.answer('Начнем заново. Введи кличку собачки.')
                await state.set_state(DogState.dog_add_start)


@router.callback_query(F.data == 'my_dogs')
async def dogs_menu(call: CallbackQuery):
    headers = {

    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f'{config('API_URL')}/dogs/', headers=headers) as response:
            dogs_list = await response.json()
            dogs_names = []
            for dog in dogs_list:
                dogs_names.append(dog['name'])
    if not dogs_list:
        await call.message.answer(text=f'Ты еще не добавил ни одну собачку.\n',
                                  )
    else:
        await call.message.answer(text=f'Твои питомцы:\n'
                                       f'{dogs_names}'
                                  )