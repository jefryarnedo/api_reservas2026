import base64
import hashlib
import hmac
import json
import os
import time
from app.core.database import Database


def verificar_password(password: str, password_hash: str) -> bool:
    """Verifica hashes con formato pbkdf2_sha256$iteraciones$salt$hash."""
    try:
        algoritmo, iteraciones, salt, esperado = password_hash.split("$", 3)
        if algoritmo != "pbkdf2_sha256":
            return False
        calculado = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iteraciones)
        ).hex()
        return hmac.compare_digest(calculado, esperado)
    except (ValueError, TypeError):
        return False


def crear_token(usuario: dict) -> str:
    secreto = os.getenv("AUTH_SECRET")
    if not secreto or len(secreto) < 32:
        raise RuntimeError("Configura AUTH_SECRET en el .env con al menos 32 caracteres.")
    ahora = int(time.time())
    payload = {
    "sub": int(usuario["id_usuario"]),
    "correo": usuario["correo_electronico"],
    "id_rol": int(usuario["id_rol"]),
    "iat": ahora,
    "exp": ahora + 60 * 60 * 8,
}
    contenido = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    firma = hmac.new(secreto.encode(), contenido.encode(), hashlib.sha256).digest()
    firma_texto = base64.urlsafe_b64encode(firma).decode().rstrip("=")
    return f"{contenido}.{firma_texto}"


class AutenticacionRepository:
    def __init__(self):
        self.db = Database()

    def buscar_por_correo(self, correo: str):
        conn = self.db.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT u.id_usuario, u.nombre_completo, u.correo_electronico,
                           u.id_rol, r.nombre AS nombre_rol, u.id_facultad, u.estado,
                           c.password_hash
                    FROM usuario u
                    JOIN usuario_credencial c ON c.id_usuario = u.id_usuario
                    LEFT JOIN rol r ON r.id_rol = u.id_rol
                    WHERE LOWER(u.correo_electronico) = LOWER(%s)
                    LIMIT 1;
                    """,
                    (correo.strip(),),
                )
                return cursor.fetchone()
        finally:
            conn.close()
