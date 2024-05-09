# Se importa la clase FastAPI del módulo fastapi
from fastapi import APIRouter

# Se crea una nueva instancia de la aplicación FastAPI
router = APIRouter()


@router.get("/products")
async def products():
    return ["producto 1","producto 2","producto 3","producto 4","producto 5","producto 6"]