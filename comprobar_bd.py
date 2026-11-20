from app.core.database import Database


def comprobar_base_datos():
    conexion = None

    try:
        conexion = Database().get_connection()

        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT
                    current_database() AS base_datos,
                    current_schema() AS esquema,
                    current_user AS usuario
            """)

            resultado = cursor.fetchone()

            print("\nCONEXIÓN EXITOSA")
            print(f"Base de datos: {resultado['base_datos']}")
            print(f"Esquema: {resultado['esquema']}")
            print(f"Usuario de conexión: {resultado['usuario']}")

            cursor.execute("""
                SELECT to_regclass('usuario_credencial')
                    AS tabla_credencial
            """)

            tabla = cursor.fetchone()

            if tabla["tabla_credencial"] is None:
                print("\nLa tabla usuario_credencial no existe")
            else:
                print("\nLa tabla usuario_credencial existe")

    except Exception as error:
        print("\nERROR AL CONECTAR O CONSULTAR LA BASE DE DATOS")
        print(f"{type(error).__name__}: {error}")

    finally:
        if conexion is not None:
            conexion.close()


if __name__ == "__main__":
    comprobar_base_datos()