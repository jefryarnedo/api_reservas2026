from fastapi import APIRouter, HTTPException
from app.models.autenticacion import LoginRequest
from app.repositories.autenticacion_repo import (
    AutenticacionRepository, verificar_password, crear_token
)

router = APIRouter(prefix="/autenticacion", tags=["Autenticación"])
repo = AutenticacionRepository()


@router.post("/login")
def iniciar_sesion(datos: LoginRequest):
    try:
        usuario = repo.buscar_por_correo(str(datos.correo))
    except Exception as exc:
        # No exponer detalles de conexión o SQL al cliente.
        raise HTTPException(status_code=500, detail="No fue posible consultar las credenciales.") from exc

    if not usuario or not verificar_password(datos.password, usuario["password_hash"]):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")

    if not usuario["estado"]:
        raise HTTPException(status_code=403, detail="El usuario está inactivo.")

    try:
        token = crear_token(usuario)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 28800,
        "usuario": {
            "id_usuario": usuario["id_usuario"],
            "nombre_completo": usuario["nombre_completo"],
            "correo_electronico": usuario["correo_electronico"],
            "id_rol": usuario["id_rol"],
            "nombre_rol": usuario["nombre_rol"],
            "id_facultad": usuario["id_facultad"],
        },
    }
