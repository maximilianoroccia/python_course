from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"], responses={404 : {"message": "No encontrado"}})

products_list = ["producto 1", "producto 2", "producto 3"]


@router.get("/")
async def products():
    return ["producto 1", "producto 2", "producto 3"]

@router.get("/{id}")
async def products(id: int):
    return products_list[id]