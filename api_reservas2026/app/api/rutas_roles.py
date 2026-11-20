from fastapi import APIRouter, HTTPException
from app.models.rol import Rol
from app.repositories.rol_repo import RolRepository

router = APIRouter(prefix="/roles", tags=["Gestión de Roles"])
repo = RolRepository()

@router.get("/")
def listar_roles():
    try:
        return repo.obtener_todos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{rol_id}")
def obtener_rol(rol_id: int):
    try:
        rol = repo.obtener_por_id(rol_id)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_rol(rol: Rol):
    try:
        nuevo_id = repo.crear(rol)
        return {"mensaje": "Rol creado exitosamente", "id_rol": nuevo_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{rol_id}")
def actualizar_rol(rol_id: int, rol: Rol):
    try:
        exito = repo.actualizar(rol_id, rol)
        if not exito:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"mensaje": "Rol actualizado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{rol_id}")
def eliminar_rol(rol_id: int):
    try:
        exito = repo.eliminar(rol_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"mensaje": "Rol eliminado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))