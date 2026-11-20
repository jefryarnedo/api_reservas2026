from fastapi import APIRouter, HTTPException
import logging

from app.models.autenticacion import LoginRequest
from app.repositories.autenticacion_repo import (
    AutenticacionRepository,
    verificar_password,
    crear_token,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/autenticacion", tags=["Autenticación"])
repo = AutenticacionRepository()


@router.post("/login")
def iniciar_sesion(datos: LoginRequest):
    """
    Valida las credenciales del usuario y devuelve un token de acceso.
    Los errores internos se registran en la terminal del backend sin
    exponer detalles de PostgreSQL al cliente.
    """
    try:
        usuario = repo.buscar_por_correo(str(datos.correo))
    except Exception as exc:
        logger.exception(
            "Error al consultar las credenciales del usuario (tipo de error: %s)",
            type(exc).__name__,
        )
        raise HTTPException(
            status_code=500,
            detail="No fue posible consultar las credenciales.",
        ) from exc

    if not usuario or not verificar_password(
        datos.password,
        usuario["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos.",
        )

    if not usuario["estado"]:
        raise HTTPException(
            status_code=403,
            detail="El usuario está inactivo.",
        )

    try:
        token = crear_token(usuario)
    except RuntimeError as exc:
        logger.exception("No fue posible generar el token de acceso.")
        raise HTTPException(
            status_code=500,
            detail=(
                "No fue posible generar el token de acceso. "
                "Revisa la configuración del backend."
            ),
        ) from exc

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
