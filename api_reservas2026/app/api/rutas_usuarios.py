from fastapi import APIRouter, HTTPException
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

router = APIRouter(prefix="/usuarios", tags=["Gestión de Usuarios"])
repo = UsuarioRepository()

@router.get("/")
def listar_usuarios():
    try:
        return repo.obtener_todos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    try:
        usuario = repo.obtener_por_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_usuario(usuario: Usuario):
    try:
        nuevo_id = repo.crear(usuario)
        return {"mensaje": "Usuario creado exitosamente", "id_usuario": nuevo_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: Usuario):
    try:
        exito = repo.actualizar(usuario_id, usuario)
        if not exito:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": "Usuario actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    try:
        exito = repo.eliminar(usuario_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"mensaje": "Usuario eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))