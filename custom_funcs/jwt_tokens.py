from aiogram.client.session import aiohttp

from settings import API_URL, BOT_SECRET_KEY

headers = {
    'X-Bot-Secret-Key': BOT_SECRET_KEY,
}

async def update_refresh_token(telegram_id, refresh_token):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/users/edit-refresh-token/',
                                json={
                                    'telegram_id': telegram_id,
                                    'refresh_token': refresh_token,
                                },
                                headers=headers) as response:
            if response.status == 200:
                return True
            else:
                return False

async def get_refresh_token_by_id(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/users/get-refresh-token/',
                                json={
                                    'telegram_id': telegram_id,
                                },
                                headers=headers) as response:
            if response.status == 200:
                user_refresh_token = await response.json()
                return user_refresh_token['refresh_token']
            else:
                return False

async def verify_jwt_token(token):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/auth/jwt/verify/',
                                json={
                                    'token': token,
                                },
                                headers=headers) as verify_response:
            return verify_response.status

async def refreshed_tokens_by_old_refresh(refresh_token):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/auth/jwt/refresh/',
                                json={
                                    'refresh': refresh_token,
                                },
                                headers=headers) as response:
            if response.status == 200:
                tokens = await response.json()
                return tokens
            else:
                return False

async def create_new_tokens_by_refresh(telegram_id, password):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f'{API_URL}/auth/jwt/refresh/',
                                json={
                                    'telegram_id': telegram_id,
                                    'password': password,
                                },
                                headers=headers) as response:
            if response.status == 200:
                tokens = await response.json()
                await update_refresh_token(telegram_id, tokens['refresh'])
                return tokens
            else:
                return False