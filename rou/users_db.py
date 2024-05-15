

from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")  # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/")  # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    existing_user = search_user("email", user.email)
    if existing_user:
        # Devuelve el usuario existente en lugar de lanzar una excepción
        return existing_user
    else:
        result = db_client.users.insert_one(user.dict(exclude_unset=True))
        if result.acknowledged:
            return user_schema(result.inserted_id)
        else:
            raise HTTPException(status_code=500, detail="Error al crear el usuario")



@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"error": "No se ha eliminado el usuario"}




def search_user(field: str, key):
    user = db_client.users.find_one({field: key})
    if user:
        # Devuelve el usuario en formato JSON
        return user_schema(user)
    else:
        # Devuelve un mensaje de error si el usuario no se encuentra
        return {"error": "No se ha encontrado el usuario"}
