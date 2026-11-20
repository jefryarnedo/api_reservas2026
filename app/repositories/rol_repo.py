from app.core.database import Database
from app.models.rol import Rol

<<<<<<< HEAD

=======
>>>>>>> origin/main
class RolRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
<<<<<<< HEAD
            # Incluye perfiles inactivos para que el administrador pueda reactivarlos.
            cursor.execute("SELECT * FROM rol ORDER BY id_rol ASC;")
            return cursor.fetchall()
=======
            cursor.execute("SELECT * FROM rol WHERE estado = TRUE ORDER BY id_rol ASC;")
            roles = cursor.fetchall()
            return roles
>>>>>>> origin/main
        except Exception as e:
            raise Exception(f"Error al obtener roles: {str(e)}")
        finally:
            conn.close()

    def obtener_por_id(self, rol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
<<<<<<< HEAD
            cursor.execute(
                "SELECT * FROM rol WHERE id_rol = %s AND estado = TRUE;",
                (rol_id,)
            )
            return cursor.fetchone()
=======
            cursor.execute("SELECT * FROM rol WHERE id_rol = %s AND estado = TRUE;", (rol_id,))
            rol = cursor.fetchone()
            return rol
>>>>>>> origin/main
        except Exception as e:
            raise Exception(f"Error al obtener rol por ID: {str(e)}")
        finally:
            conn.close()

    def crear(self, rol: Rol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
<<<<<<< HEAD
            cursor.execute(
                "INSERT INTO rol (nombre, descripcion) VALUES (%s, %s) RETURNING id_rol;",
                (rol.nombre, rol.descripcion)
            )
            fila = cursor.fetchone()
            conn.commit()
            return fila["id_rol"] if isinstance(fila, dict) else fila[0]
=======
            query = "INSERT INTO rol (nombre, descripcion) VALUES (%s, %s) RETURNING id_rol;"
            cursor.execute(query, (rol.nombre, rol.descripcion))
            nuevo_id = cursor.fetchone()['id_rol']
            conn.commit()
            return nuevo_id
>>>>>>> origin/main
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear rol: {str(e)}")
        finally:
            conn.close()

    def actualizar(self, rol_id: int, rol: Rol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
<<<<<<< HEAD
            cursor.execute(
                "UPDATE rol SET nombre = %s, descripcion = %s "
                "WHERE id_rol = %s AND estado = TRUE RETURNING id_rol;",
                (rol.nombre, rol.descripcion, rol_id)
            )
=======
            query = "UPDATE rol SET nombre = %s, descripcion = %s WHERE id_rol = %s AND estado = TRUE RETURNING id_rol;"
            cursor.execute(query, (rol.nombre, rol.descripcion, rol_id))
>>>>>>> origin/main
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar rol: {str(e)}")
        finally:
            conn.close()

<<<<<<< HEAD
    def cambiar_estado(self, rol_id: int, estado: bool):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE rol SET estado = %s WHERE id_rol = %s "
                "RETURNING id_rol, estado;",
                (estado, rol_id)
            )
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al cambiar el estado del perfil: {str(e)}")
        finally:
            conn.close()

    def eliminar(self, rol_id: int):
        # Mantiene compatibilidad con DELETE: desactivar sin borrar físicamente.
        return self.cambiar_estado(rol_id, False) is not None
=======
    def eliminar(self, rol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE rol SET estado = FALSE WHERE id_rol = %s RETURNING id_rol;", (rol_id,))
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar rol: {str(e)}")
        finally:
            conn.close()
>>>>>>> origin/main
