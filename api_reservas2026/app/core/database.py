from __future__ import annotations

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor


# app/core/database.py -> project root is two levels above this file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"

# Load the .env belonging to this backend, not one from another working
# directory. override=True prevents stale Windows environment variables
# (for example DB_HOST=localhost) from overriding the project's settings.
load_dotenv(dotenv_path=ENV_FILE, override=True)


class Database:
    def __init__(self) -> None:
        self.host = os.getenv("DB_HOST")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.port = os.getenv("DB_PORT", "5432")
        self.sslmode = os.getenv("DB_SSLMODE", "require")

    def get_connection(self):
        required = {
            "DB_HOST": self.host,
            "DB_NAME": self.database,
            "DB_USER": self.user,
            "DB_PASSWORD": self.password,
            "DB_PORT": self.port,
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise RuntimeError(
                "Faltan variables de conexión en el archivo .env: "
                + ", ".join(missing)
                + f". Archivo esperado: {ENV_FILE}"
            )

        try:
            return psycopg2.connect(
                host=self.host,
                dbname=self.database,
                user=self.user,
                password=self.password,
                port=int(self.port),
                sslmode=self.sslmode,
                connect_timeout=10,
                cursor_factory=RealDictCursor,
            )
        except psycopg2.Error as exc:
            # No se imprime ni se devuelve la contraseña.
            raise RuntimeError(
                "No fue posible conectar con PostgreSQL. "
                f"Revisa DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT y DB_SSLMODE "
                f"en {ENV_FILE}. Detalle del controlador: {exc}"
            ) from exc
