import json
import os
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get['ALGORITHMS']
API_AUDIENCE = os.environ.get('API_AUDIENCE')

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
'''
Get the access token from the autherization header
'''


def get_token_auth_header():

    if "Authorization" in request.headers:

        ''' Get the autherization header '''
        auth = request.headers['Authorization']

        authsplit = auth.split(' ')

        if authsplit[0].lower() != 'bearer':
            ''' Throw a 401 if the header is not a bearer type '''
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Autherization header must start with "Bearer'
            }, 401)

        elif len(authsplit) == 1:
            ''' Throw a 401 as there is no token '''
            raise AuthError({
                'code': 'invalid_header',
                'description': 'No Token in Header'
            }, 401)

        elif len(authsplit) > 2:
            ''' Throw a 401 as not bearer token '''
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must be a bearer token'
            }, 401)

        token = authsplit[1]
        return token

    ''' Throw a 401 as header missing'''
    raise AuthError({
        'code': 'autherization_header_missing',
        'description': 'Autherization header is missing.'

    }, 401)


def check_permissions(permission, payload):
    ''' If permissions not included in payload throw 401 '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'No permissions in token'
        }, 401)

    ''' If permision not in permissions array throw 403 not authorised '''
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'not_authorised',
            'description': 'Not Authorized'
        }, 403)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
