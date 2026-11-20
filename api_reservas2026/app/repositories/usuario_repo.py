from app.core.database import Database
from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        if conn is None:
            raise Exception("No fue posible conectar con PostgreSQL.")
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        u.id_usuario,
                        u.nombre_completo,
                        u.correo_electronico,
                        u.telefono,
                        u.id_rol,
                        r.nombre AS nombre_rol,
                        u.id_facultad,
                        f.nombre_facultad,
                        u.estado,
                        u.creado,
                        u.actualizado
                    FROM usuario AS u
                    LEFT JOIN rol AS r ON r.id_rol = u.id_rol
                    LEFT JOIN facultad AS f ON f.id_facultad = u.id_facultad
                    ORDER BY u.id_usuario ASC;
                    """
                )
                return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {e}") from e
        finally:
            conn.close()

    def obtener_por_id(self, usuario_id: int):
        conn = self.db.get_connection()
        if conn is None:
            raise Exception("No fue posible conectar con PostgreSQL.")
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        u.id_usuario,
                        u.nombre_completo,
                        u.correo_electronico,
                        u.telefono,
                        u.id_rol,
                        r.nombre AS nombre_rol,
                        u.id_facultad,
                        f.nombre_facultad,
                        u.estado,
                        u.creado,
                        u.actualizado
                    FROM usuario AS u
                    LEFT JOIN rol AS r ON r.id_rol = u.id_rol
                    LEFT JOIN facultad AS f ON f.id_facultad = u.id_facultad
                    WHERE u.id_usuario = %s;
                    """,
                    (usuario_id,),
                )
                return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error al obtener usuario por ID: {e}") from e
        finally:
            conn.close()

    def crear(self, usuario: Usuario):
        conn = self.db.get_connection()
        if conn is None:
            raise Exception("No fue posible conectar con PostgreSQL.")
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO usuario
                        (nombre_completo, correo_electronico, telefono, id_rol, id_facultad, estado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_usuario;
                    """,
                    (
                        usuario.nombre_completo.strip(),
                        str(usuario.correo_electronico).strip().lower(),
                        usuario.telefono.strip() if usuario.telefono else None,
                        usuario.id_rol,
                        usuario.id_facultad,
                        usuario.estado,
                    ),
                )
                fila = cursor.fetchone()
                conn.commit()
                return fila["id_usuario"]
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear usuario: {e}") from e
        finally:
            conn.close()

    def actualizar(self, usuario_id: int, usuario: Usuario):
        conn = self.db.get_connection()
        if conn is None:
            raise Exception("No fue posible conectar con PostgreSQL.")
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE usuario
                    SET nombre_completo = %s,
                        correo_electronico = %s,
                        telefono = %s,
                        id_rol = %s,
                        id_facultad = %s,
                        estado = %s,
                        actualizado = CURRENT_TIMESTAMP
                    WHERE id_usuario = %s
                    RETURNING id_usuario;
                    """,
                    (
                        usuario.nombre_completo.strip(),
                        str(usuario.correo_electronico).strip().lower(),
                        usuario.telefono.strip() if usuario.telefono else None,
                        usuario.id_rol,
                        usuario.id_facultad,
                        usuario.estado,
                        usuario_id,
                    ),
                )
                actualizado = cursor.fetchone()
                conn.commit()
                return actualizado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar usuario: {e}") from e
        finally:
            conn.close()

    def eliminar(self, usuario_id: int):
        conn = self.db.get_connection()
        if conn is None:
            raise Exception("No fue posible conectar con PostgreSQL.")
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE usuario SET estado = FALSE, actualizado = CURRENT_TIMESTAMP WHERE id_usuario = %s RETURNING id_usuario;",
                    (usuario_id,),
                )
                eliminado = cursor.fetchone()
                conn.commit()
                return eliminado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al desactivar usuario: {e}") from e
        finally:
            conn.close()
