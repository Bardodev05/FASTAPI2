# Se importa la clase FastAPI del módulo fastapi
from fastapi import FastAPI
from rou import users,product
from fastapi.staticfiles import StaticFiles

# Se crea una nueva instancia de la aplicación FastAPI
app = FastAPI()

# routers
app.include_router(product.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"),name="static")


# Se define una ruta raíz ("/") que responde a las solicitudes GET
@app.get("/")
# Se define una función asíncrona llamada "root" que manejará las solicitudes GET a la ruta raíz
async def root():
    # La función retorna un mensaje simple indicando "Hola FastAPI"
    return "Hola FastAPI"

# Define una ruta "/url" que responde a las solicitudes GET
@app.get("/url")
# Define una función asíncrona llamada "url" que manejará las solicitudes GET a la ruta "/url"
async def url():
    # Retorna un diccionario con una clave "url_curso" y el valor de la URL del curso
    return { "url_curso": "https://bardodev.com/python" }
