from app.core.database import Database
from app.models.modulosxrol import ModulosXRol

class ModulosXRolRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM modulosxrol WHERE estado = TRUE ORDER BY id_modulosxrol ASC;")
            asignaciones = cursor.fetchall()
            return asignaciones
        except Exception as e:
            raise Exception(f"Error al obtener asignaciones de módulos por rol: {str(e)}")
        finally:
            conn.close()

    def obtener_por_id(self, modulosxrol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM modulosxrol WHERE id_modulosxrol = %s AND estado = TRUE;", (modulosxrol_id,))
            asignacion = cursor.fetchone()
            return asignacion
        except Exception as e:
            raise Exception(f"Error al obtener asignación por ID: {str(e)}")
        finally:
            conn.close()

    def obtener_por_rol(self, rol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                SELECT mr.id_modulosxrol, mr.id_rol, mr.id_modulo, m.nombre, m.ruta_url
                FROM modulosxrol mr
                JOIN modulo m ON m.id_modulo = mr.id_modulo
                WHERE mr.id_rol = %s AND mr.estado = TRUE AND m.estado = TRUE
                ORDER BY m.nombre ASC;
            """
            cursor.execute(query, (rol_id,))
            modulos = cursor.fetchall()
            return modulos
        except Exception as e:
            raise Exception(f"Error al obtener módulos del rol: {str(e)}")
        finally:
            conn.close()

    def crear(self, modulosxrol: ModulosXRol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO modulosxrol (id_rol, id_modulo)
                VALUES (%s, %s) RETURNING id_modulosxrol;
            """
            cursor.execute(query, (modulosxrol.id_rol, modulosxrol.id_modulo))
            nuevo_id = cursor.fetchone()['id_modulosxrol']
            conn.commit()
            return nuevo_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al asignar módulo a rol: {str(e)}")
        finally:
            conn.close()

    def actualizar(self, modulosxrol_id: int, modulosxrol: ModulosXRol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE modulosxrol
                SET id_rol = %s, id_modulo = %s
                WHERE id_modulosxrol = %s AND estado = TRUE RETURNING id_modulosxrol;
            """
            cursor.execute(query, (modulosxrol.id_rol, modulosxrol.id_modulo, modulosxrol_id))
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar asignación: {str(e)}")
        finally:
            conn.close()

    def eliminar(self, modulosxrol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE modulosxrol SET estado = FALSE WHERE id_modulosxrol = %s RETURNING id_modulosxrol;", (modulosxrol_id,))
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar asignación: {str(e)}")
        finally:
            conn.close()