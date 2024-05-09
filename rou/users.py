from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Importamos las clases necesarias de FastAPI y Pydantic
# APIRouter se utiliza para crear rutas de API
# BaseModel se utiliza para definir el modelo de datos de los usuarios

# Inicializamos el router de FastAPI
router = APIRouter()

# Definimos la clase User con Pydantic para validar los datos de entrada
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Creamos una lista inicial de usuarios
users_list = [
    User(id=1, name="Anderson", surname="Molina", url="https://anderson.dev", age=35),
    User(id=2, name="Moure", surname="Dev", url="https://mouredev.com", age=35),
    User(id=3, name="Brais", surname="Dahlberg", url="https://haakon.com", age=33)
]



# Ruta para obtener todos los usuarios en formato JSON
@router.get("/usersjson")
async def usersjson():
    # Devolvemos una lista de diccionarios con los datos de los usuarios
    return [
        {"name": "Anderson", "surname": "Molina", "url": "https://anderson.dev", "age": 35},
        {"name": "Moure", "surname": "Dev", "url": "https://mouredev.com", "age": 35},
        {"name": "Haakon", "surname": "Dahlberg", "url": "https://haakon.com", "age": 33}
    ]

# Ruta para obtener todos los usuarios
@router.get("/users")
async def users():
    # Devolvemos la lista de usuarios
    return users_list

# Ruta para obtener un usuario específico por ID
@router.get("/user/{id}")  # Path parameter
async def user(id: int):
    # Buscamos al usuario por su ID y devolvemos sus datos
    return search_user(id)

# Ruta para obtener un usuario específico por ID usando parámetros de consulta
@router.get("/user/")  # Query parameter
async def user(id: int):
    # Buscamos al usuario por su ID y devolvemos sus datos
    return search_user(id)

# Ruta para crear un nuevo usuario
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    # Verificamos si el usuario ya existe antes de agregarlo
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    # Agregamos el nuevo usuario a la lista
    users_list.append(user)
    # Devolvemos el usuario creado
    return user

# Ruta para actualizar un usuario existente
@router.put("/user/")
async def user(user: User):
    # Buscamos al usuario por su ID y actualizamos sus datos
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    # Si no se encontró el usuario, devolvemos un error
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    # Si se actualizó correctamente, devolvemos el usuario actualizado
    return user

# Ruta para eliminar un usuario por su ID
@router.delete("/user/{id}")
async def user(id: int):
    # Buscamos al usuario por su ID y lo eliminamos
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    # Si no se encontró el usuario, devolvemos un error
    if not found:
        return {"error": "No se ha eliminado el usuario"}

# Función auxiliar para buscar un usuario por su ID
def search_user(id: int):
    # Filtramos la lista de usuarios para encontrar el que coincide con el ID dado
    users = filter(lambda user: user.id == id, users_list)
    # Intentamos obtener el primer resultado de la búsqueda
    try:
        return list(users)[0]
    # Si no se encuentra ningún usuario, devolvemos un mensaje de error
    except:
        return {"error": "No se ha encontrado el usuario"}
