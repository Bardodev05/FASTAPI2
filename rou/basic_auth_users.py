from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
class UserDB(User):
    password: str 
    
users_db = {
    "Anderson": {
        "username": "Anderson",
        "full_name": "Anderson MOlina",
        "email": "andersmolina133",
        "disabled": False,
        "password": "1234"
    },
    "Andersondev": {
        "username": "Anderson de",
        "full_name": "Anderson MOlina de",
        "email": "andersmolina133de",
        "disabled": True,
        "password": "12346789"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])    
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token) 
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El usuario no está autenticado")
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario inactivo")
    
    return user
        
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto", headers={"WWW-Authenticate": "Bearer"})
    
    if not form.password == user.password:  
        raise HTTPException(status_code=400, detail="La contraseña no es correcta")
    
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user
