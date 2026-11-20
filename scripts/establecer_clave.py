"""Crea o restablece la contraseña de un usuario por correo.
Ejecutar desde la raíz del backend: python scripts/establecer_clave.py correo@dominio.com
Solicita la contraseña sin mostrarla en pantalla.
"""
import getpass
import hashlib
import os
import sys
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.core.database import Database


def hash_password(password: str) -> str:
    salt = secrets.token_urlsafe(16)
    rounds = 310_000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), rounds).hex()
    return f"pbkdf2_sha256${rounds}${salt}${digest}"


def main():
    if len(sys.argv) != 2:
        print("Uso: python scripts/establecer_clave.py correo@dominio.com")
        raise SystemExit(2)
    correo = sys.argv[1].strip().lower()
    password = getpass.getpass("Nueva contraseña (mínimo 12 caracteres): ")
    confirmacion = getpass.getpass("Confirma la contraseña: ")
    if len(password) < 12:
        print("La contraseña debe tener al menos 12 caracteres.")
        raise SystemExit(2)
    if password != confirmacion:
        print("Las contraseñas no coinciden.")
        raise SystemExit(2)

    conn = Database().get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario, estado FROM usuario WHERE LOWER(correo_electronico) = %s",
                (correo,),
            )
            usuario = cursor.fetchone()
            if not usuario:
                raise SystemExit("No existe un usuario con ese correo.")
            if not usuario["estado"]:
                raise SystemExit("El usuario está inactivo; actívalo antes de asignarle una contraseña.")
            cursor.execute(
                """
                INSERT INTO usuario_credencial (id_usuario, password_hash, actualizado)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (id_usuario) DO UPDATE
                SET password_hash = EXCLUDED.password_hash,
                    actualizado = CURRENT_TIMESTAMP;
                """,
                (usuario["id_usuario"], hash_password(password)),
            )
        conn.commit()
        print(f"Contraseña configurada correctamente para {correo}.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
