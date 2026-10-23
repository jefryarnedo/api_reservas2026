from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre_completo: str
    correo_electronico: str
    telefono: Optional[str] = None
    id_rol: int
    id_facultad: Optional[int] = None