from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 

router = APIRouter(prefix="/basic_auth", 
                   tags=["basic_auth_users"], 
                   responses=status.HTTP_404_NOT_FOUND: {"message": "No encontrado"})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "1234"
    },
    "maxi2": {
        "username": "maxi2",
        "fullname": "Maxi 2 Roccia",
        "email": "maxiroccia2@gmail.com",
        "disabled": True,
        "password": "4321"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def currente_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Usuario no autorizaado",
            headers={"www-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user 

    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code= 400, detail="Contraseña incorrecta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(currente_user)):
    return user