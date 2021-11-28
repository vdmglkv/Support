import datetime
import jwt
from django.conf import settings


def generate_access_token(user):

    access_token_payload = {
            'id': user.id,
            'email': user.email,
            'isStaff?': user.is_admin,
            'expire': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=10)),
            'create': str(datetime.datetime.utcnow())
        }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
            'id': user.id,
            'email': user.email,
            'isStaff?': user.is_admin,
            'expire': str(datetime.datetime.utcnow() + datetime.timedelta(days=1)),
            'create': str(datetime.datetime.utcnow())
        }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token
