from app.core.database import Database
from app.models.usuario import Usuario

class UsuarioRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuario WHERE estado = TRUE ORDER BY id_usuario ASC;")
            usuarios = cursor.fetchall()
            return usuarios
        except Exception as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")
        finally:
            conn.close()

    def obtener_por_id(self, usuario_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s AND estado = TRUE;", (usuario_id,))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            raise Exception(f"Error al obtener usuario por ID: {str(e)}")
        finally:
            conn.close()

    def crear(self, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO usuario (nombre_completo, correo_electronico, telefono, id_rol, id_facultad) 
                VALUES (%s, %s, %s, %s, %s) RETURNING id_usuario;
            """
            cursor.execute(query, (usuario.nombre_completo, usuario.correo_electronico, usuario.telefono, usuario.id_rol, usuario.id_facultad))
            nuevo_id = cursor.fetchone()['id_usuario']
            conn.commit()
            return nuevo_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear usuario: {str(e)}")
        finally:
            conn.close()

    def actualizar(self, usuario_id: int, usuario: Usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE usuario
                SET nombre_completo = %s, correo_electronico = %s, telefono = %s, id_rol = %s, id_facultad = %s
                WHERE id_usuario = %s AND estado = TRUE RETURNING id_usuario;
            """
            cursor.execute(query, (usuario.nombre_completo, usuario.correo_electronico, usuario.telefono, usuario.id_rol, usuario.id_facultad, usuario_id))
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar usuario: {str(e)}")
        finally:
            conn.close()

    def eliminar(self, usuario_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuario SET estado = FALSE WHERE id_usuario = %s RETURNING id_usuario;", (usuario_id,))
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar usuario: {str(e)}")
        finally:
            conn.close()