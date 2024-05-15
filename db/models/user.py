from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    # El campo 'id' es opcional y no se utilizará para almacenar el ID generado automáticamente por MongoDB
    id: Optional[str] = None