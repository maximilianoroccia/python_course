from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/user", tags=["users"])

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id= 1, name="Maxi", surname="Roccia", url="https://www.linkedin.com/in/maximiliano-e-roccia/", age=42),
              User(id= 2, name="Vico", surname="Farias", url="https://www.linkedin.com/in/virginia-farias/", age=32)]

@router.get("/usersjson")
async def usersjson(): 
    return [{"name": "Maxi", "surname": "Roccia", "url": "https://www.linkedin.com/in/maximiliano-e-roccia/"},
            {"name": "Vico", "surname": "Farias", "url": "https://www.linkedin.com/in/virginia-farias/"}]

@router.get("/list")
async def users():
    return users_list

#path
@router.get("/{id}")
async def user(id: int):
    return search_user(id)

#query    
@router.get("/")
async def user(id: int):
     return search_user(id)

    
@router.post("/", response_model=User, status_code=201)
async def user(user: User):
   if type(search_user(user.id)) == User:
       raise HTTPException(status_code=404, detail="usuario existente")
   else:
       users_list.append(user)


@router.put("/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error":"no se ha actualizado el usuario"}
    else:
        return user
    
@router.delete("/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index] 
            found = True
    if not found:
        return {"error":"no se ha borrado el usuario"}


   
def search_user(id: int):
    users = filter (lambda user: user.id == id, users_list)
    try: 
        return list(users)[0]
    except:
        return {"error":"No user"}