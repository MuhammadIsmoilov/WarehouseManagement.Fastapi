from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from lib.config import Keys
from authlib.jose import jwt
import time


app = FastAPI()

secret = Keys()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not self.verify_jwt(credentials.credentials, request):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Not authenticated.")
    def verify_jwt(self, jwtoken: str, request: Request) -> bool:
        isTokenValid: bool = False
        try:
            endpoint_path = request.url.path
            payload = jwt.decode(jwtoken, secret.publickey) 
        except Exception as e:
            payload = None
            
        if payload:
            if time.time() < payload['expires']:
                if payload['type'] == 0:
                    isTokenValid = True
                if payload['type'] == 1 and endpoint_path.split('/')[-1] == 'refresh_token':
                    isTokenValid = True
            else:
                if payload['type'] == 0:
                    raise HTTPException(status_code=403, detail="Invalid token or expired token.")
                if payload['type'] == 1:
                    raise HTTPException(status_code=401, detail="Invalid token or expired token.")
        return isTokenValid


def access_token(login: str, user: str,):
    payload = {
        "type": 0,
        "user_id": user,
        "user_login": login,
        "expires": time.time() + 360 * 24 * 30
    }
    header = {'alg': 'RS256'}
    token = jwt.encode(header, payload, secret.privatekey)
    return token

def refresh_token(login: str, user: str):
    payload = {
        "type": 1,
        "user_id": user,
        "user_login": login,
        "expires": time.time() + 360 * 24 * 30
    }
    header = {'alg': 'RS256'}
    token = jwt.encode(header, payload, secret.privatekey)
    return token


def refresh_access_token(token):
    decoded_token = decodeJWT(token)
    return access_token(decoded_token['user_login'], decoded_token['id'])


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, secret.publickey)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=403, detail="JWT decode error: {}".format(e))

def JWTpayload(credentials: str = Depends(JWTBearer())) -> dict:
    try:
        decoded_token = jwt.decode(credentials, secret.publickey)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=403, detail="JWT payload error: {}".format(e))
