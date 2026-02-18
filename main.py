from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#app.include_router(products.router)
#app.include_router(users.router)
#app.mount("/static", StaticFiles(directory="static"), name="static")
#app.include_router(basic_auth_users.router)
#app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


@app.get("/")
async def root():
    return "Hola FastAPI"

@app.get("/url")
async def url():
    return {"url":"https://mouredev.com/python"}

# Iniciar el server: uvicorn main:app --reload
# Detener el server ctrl +C
# Documentacion automatica http://127.0.0.1.8000/ docs (swagger) redoc (Redocly)