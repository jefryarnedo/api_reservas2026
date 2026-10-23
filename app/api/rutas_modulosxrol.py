from fastapi import APIRouter, HTTPException
from app.models.modulosxrol import ModulosXRol
from app.repositories.modulosxrol_repo import ModulosXRolRepository

router = APIRouter(prefix="/modulos-roles", tags=["Permisos de Módulos por Rol"])
repo = ModulosXRolRepository()

@router.get("/")
def listar_asignaciones():
    try:
        return repo.obtener_todos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rol/{rol_id}")
def listar_modulos_de_rol(rol_id: int):
    try:
        return repo.obtener_por_rol(rol_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{modulosxrol_id}")
def obtener_asignacion(modulosxrol_id: int):
    try:
        asignacion = repo.obtener_por_id(modulosxrol_id)
        if not asignacion:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")
        return asignacion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_asignacion(modulosxrol: ModulosXRol):
    try:
        nuevo_id = repo.crear(modulosxrol)
        return {"mensaje": "Módulo asignado al rol exitosamente", "id_modulosxrol": nuevo_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{modulosxrol_id}")
def actualizar_asignacion(modulosxrol_id: int, modulosxrol: ModulosXRol):
    try:
        exito = repo.actualizar(modulosxrol_id, modulosxrol)
        if not exito:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")
        return {"mensaje": "Asignación actualizada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{modulosxrol_id}")
def eliminar_asignacion(modulosxrol_id: int):
    try:
        exito = repo.eliminar(modulosxrol_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Asignación no encontrada")
        return {"mensaje": "Asignación eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))