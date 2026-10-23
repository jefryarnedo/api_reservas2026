from fastapi import APIRouter, HTTPException
from app.models.reserva import Reserva
from app.repositories.reserva_repo import ReservaRepository

router = APIRouter(prefix="/reservas", tags=["Gestión de Reservas"])
repo = ReservaRepository()

@router.get("/")
def listar_reservas():
    try:
        return repo.obtener_todas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{reserva_id}")
def obtener_reserva(reserva_id: int):
    try:
        reserva = repo.obtener_por_id(reserva_id)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def crear_reserva(reserva: Reserva):
    try:
        nuevo_id = repo.crear(reserva)
        return {"mensaje": "Reserva creada exitosamente", "id_reserva": nuevo_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{reserva_id}")
def actualizar_reserva(reserva_id: int, reserva: Reserva):
    try:
        exito = repo.actualizar(reserva_id, reserva)
        if not exito:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return {"mensaje": "Reserva actualizada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: int):
    try:
        exito = repo.eliminar(reserva_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return {"mensaje": "Reserva eliminada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))