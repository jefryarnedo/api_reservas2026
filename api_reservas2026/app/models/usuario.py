from typing import Optional
from pydantic import BaseModel, Field


class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre_completo: str = Field(min_length=2, max_length=150)
    correo_electronico: str = Field(min_length=5, max_length=254)
    telefono: Optional[str] = None
    id_rol: int
    id_facultad: Optional[int] = None
    estado: bool = True
