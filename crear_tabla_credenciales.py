from app.core.database import Database


def crear_tabla_credenciales():
    conexion = None

    try:
        conexion = Database().get_connection()

        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.usuario_credencial (
                        id_usuario INTEGER PRIMARY KEY,
                        password_hash TEXT NOT NULL,
                        actualizado TIMESTAMPTZ NOT NULL
                            DEFAULT CURRENT_TIMESTAMP,

                        CONSTRAINT fk_usuario_credencial_usuario
                            FOREIGN KEY (id_usuario)
                            REFERENCES public.usuario(id_usuario)
                            ON DELETE CASCADE
                    );
                """)

        print("Tabla usuario_credencial creada o ya existente.")

    except Exception as error:
        print("No fue posible crear la tabla.")
        print(f"Error: {type(error).__name__}: {error}")

    finally:
        if conexion is not None:
            conexion.close()


if __name__ == "__main__":
    crear_tabla_credenciales()