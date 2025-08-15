import json
from functools import wraps
from flask import request, abort
from jose import jwt
from urllib.request import urlopen
import os

# === CONFIG ===

USE_AUTH0 = os.getenv("USE_AUTH0", "false").lower() == "true"  # mock mode if false
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-auth0-domain.auth0.com")
ALGORITHMS = ["RS256"]
API_AUDIENCE = os.getenv("API_AUDIENCE", "casting")

# === MOCK ROLE TOKENS FOR LOCAL DEV ===

MOCK_PERMISSIONS = {
    'assistant': ['get:actors', 'get:movies'],
    'director': ['get:actors', 'get:movies', 'post:actors', 'patch:actors', 'delete:actors', 'patch:movies'],
    'producer': ['get:actors', 'get:movies', 'post:actors', 'patch:actors', 'delete:actors',
                 'patch:movies', 'post:movies', 'delete:movies']
}

# === AUTH ERROR EXCEPTION ===

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# === TOKEN PARSING ===

def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description": "Authorization header is expected."}, 401)

    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must start with Bearer."}, 401)
    elif len(parts) != 2:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found."}, 401)

    return parts[1]

# === DECODE JWT ===

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "Token expired."}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description": "Incorrect claims. Check audience and issuer."}, 401)
        except Exception as e:
            raise AuthError({"code": "invalid_header",
                             "description": "Unable to parse authentication token."}, 400)

    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find the appropriate key."}, 400)

# === PERMISSION CHECK ===

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({"code": "invalid_claims",
                         "description": "Permissions not included in JWT."}, 403)
    if permission not in payload['permissions']:
        raise AuthError({"code": "unauthorized",
                         "description": f"Permission {permission} not found."}, 403)
    return True

# === DECORATOR ===

def requires_auth(permission=''):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()

            if USE_AUTH0:
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            else:
                # Mock mode
                role = token.lower()
                permissions = MOCK_PERMISSIONS.get(role)
                if not permissions or permission not in permissions:
                    raise AuthError({"code": "unauthorized",
                                     "description": f"Permission '{permission}' not allowed for role '{role}'."}, 403)

            return f(*args, **kwargs)
        return wrapper
    return decorator


