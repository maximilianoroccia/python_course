from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
SECRET_KEY="2a0f3d8ea6563bee690ed211df9d96cf83edb7a4bb8ee5eb738e4a04d634de77"
ACCESS_TOKEN_DURATION = 1 # minutos
router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"],deprecated="auto")


class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "maxi": {
        "username": "maxi",
        "fullname": "Maxi Roccia",
        "email": "maxiroccia@gmail.com",
        "disabled": False,
        "password": "$2a$12$MzXLcCocDPnnmSEssqUom.1RIfbmjXmzUAIm4gqWCGVyD8hXMPwWC"
    },
    "maxi2": {
        "username": "maxi2",
        "fullname": "Maxi 2 Roccia",
        "email": "maxiroccia2@gmail.com",
        "disabled": True,
        "password": "$2a$12$SMAGqCfZT23GHN7Ujebu3OR5ACZUsKirTc6TpaaKgCAWfNqjGLbRW"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Usuario no autorizaado", 
        headers={"www-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception  

    except JWTError: 
        raise exception

    return search_user(username)


async def currente_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user 

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code= 400, detail="Contraseña incorrecta")
    
    access_token = {"sub": user.username,
                    "exp": datetime.now() + timedelta(minutes = ACCESS_TOKEN_DURATION)}

    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), 
        "token_type": "bearer"
        } 

@router.get("/users/me")
async def me(user: User = Depends(currente_user)): return user