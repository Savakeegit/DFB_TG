import datetime
import jwt
from decouple import config

API_DFB_SECRET_KEY = config('API_DFB_SECRET_KEY')

def create_access_token(user_id):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    payload = {
        "user_id": user_id,
        "exp": expiration,
        "jti": f'JWT:Access:{str(user_id)}',
        "token_class": "AccessToken",
        "token_type": "access",
    }
    token = jwt.encode(payload, API_DFB_SECRET_KEY, algorithm="HS256")
    return token

def decode_access_token(token):
    try:
        jwt.decode(token, API_DFB_SECRET_KEY, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        return False