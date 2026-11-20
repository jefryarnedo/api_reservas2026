from app.core.database import Database
from app.models.modulosxrol import ModulosXRol

<<<<<<< HEAD

=======
>>>>>>> origin/main
class ModulosXRolRepository:
    def __init__(self):
        self.db = Database()

<<<<<<< HEAD
    @staticmethod
    def _valor(fila, nombre, indice):
        """Permite trabajar con cursores que devuelven dict o tuplas."""
        if fila is None:
            return None
        return fila[nombre] if isinstance(fila, dict) else fila[indice]

=======
>>>>>>> origin/main
    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
<<<<<<< HEAD
            cursor.execute("""
                SELECT id_modulosxrol, id_rol, id_modulo, estado
                FROM modulosxrol
                ORDER BY id_rol, id_modulo, id_modulosxrol;
            """)
            return cursor.fetchall()
=======
            cursor.execute("SELECT * FROM modulosxrol WHERE estado = TRUE ORDER BY id_modulosxrol ASC;")
            asignaciones = cursor.fetchall()
            return asignaciones
>>>>>>> origin/main
        except Exception as e:
            raise Exception(f"Error al obtener asignaciones de módulos por rol: {str(e)}")
        finally:
            conn.close()

    def obtener_por_id(self, modulosxrol_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
<<<<<<< HEAD
            cursor.execute("""
                SELECT id_modulosxrol, id_rol, id_modulo, estado
                FROM modulosxrol
                WHERE id_modulosxrol = %s;
            """, (modulosxrol_id,))
            return cursor.fetchone()
=======
            cursor.execute("SELECT * FROM modulosxrol WHERE id_modulosxrol = %s AND estado = TRUE;", (modulosxrol_id,))
            asignacion = cursor.fetchone()
            return asignacion
>>>>>>> origin/main
        except Exception as e:
            raise Exception(f"Error al obtener asignación por ID: {str(e)}")
        finally:
            conn.close()

    def obtener_por_rol(self, rol_id: int):
<<<<<<< HEAD
        """Devuelve el catálogo completo de módulos y el permiso real del perfil.

        El LEFT JOIN LATERAL garantiza una fila por módulo, incluso cuando el rol
        todavía no tiene una asignación registrada para ese módulo.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT
                    m.id_modulo,
                    m.nombre,
                    m.ruta_url,
                    m.estado AS modulo_activo,
                    mr.id_modulosxrol,
                    %s AS id_rol,
                    COALESCE(mr.estado, FALSE) AS permiso_activo
                FROM modulo m
                LEFT JOIN LATERAL (
                    SELECT x.id_modulosxrol, x.estado
                    FROM modulosxrol x
                    WHERE x.id_rol = %s
                      AND x.id_modulo = m.id_modulo
                    ORDER BY x.id_modulosxrol DESC
                    LIMIT 1
                ) mr ON TRUE
                WHERE m.estado = TRUE
                ORDER BY m.id_modulo ASC;
            """, (rol_id, rol_id))
            filas = cursor.fetchall()

            # Entregar objetos JSON explícitos al frontend. RealDictCursor devuelve
            # filas tipo RealDictRow; convertirlas a dict evita diferencias de
            # serialización entre versiones de psycopg2/FastAPI.
            return [dict(fila) for fila in filas]
=======
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
>>>>>>> origin/main
        except Exception as e:
            raise Exception(f"Error al obtener módulos del rol: {str(e)}")
        finally:
            conn.close()

<<<<<<< HEAD
    def actualizar_estado(self, rol_id: int, modulo_id: int, estado: bool):
        """Activa/desactiva un permiso; crea la relación si se está habilitando."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # Verifica que el perfil y el módulo existan.
            cursor.execute("SELECT id_rol FROM rol WHERE id_rol = %s;", (rol_id,))
            if cursor.fetchone() is None:
                raise ValueError("El perfil indicado no existe.")

            cursor.execute("""
                SELECT id_modulo
                FROM modulo
                WHERE id_modulo = %s AND estado = TRUE;
            """, (modulo_id,))
            if cursor.fetchone() is None:
                raise ValueError("El módulo indicado no existe o está inactivo.")

            cursor.execute("""
                SELECT id_modulosxrol
                FROM modulosxrol
                WHERE id_rol = %s AND id_modulo = %s
                ORDER BY id_modulosxrol DESC
                LIMIT 1;
            """, (rol_id, modulo_id))
            existente = cursor.fetchone()

            if existente is not None:
                id_asignacion = self._valor(existente, "id_modulosxrol", 0)
                cursor.execute("""
                    UPDATE modulosxrol
                    SET estado = %s, actualizado = CURRENT_TIMESTAMP
                    WHERE id_modulosxrol = %s
                    RETURNING id_modulosxrol, estado;
                """, (estado, id_asignacion))
                resultado = cursor.fetchone()
            elif estado:
                cursor.execute("""
                    INSERT INTO modulosxrol (id_rol, id_modulo, estado)
                    VALUES (%s, %s, TRUE)
                    RETURNING id_modulosxrol, estado;
                """, (rol_id, modulo_id))
                resultado = cursor.fetchone()
            else:
                # Un permiso inexistente ya equivale a no tener acceso.
                resultado = None

            conn.commit()
            return {
                "id_rol": rol_id,
                "id_modulo": modulo_id,
                "id_modulosxrol": self._valor(resultado, "id_modulosxrol", 0) if resultado else None,
                "permiso_activo": bool(self._valor(resultado, "estado", 1)) if resultado else False,
            }
        except ValueError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar el permiso: {str(e)}")
        finally:
            conn.close()

    def crear(self, modulosxrol: ModulosXRol):
        """Concede acceso; reactiva la relación más reciente si ya existía."""
        resultado = self.actualizar_estado(
            int(modulosxrol.id_rol), int(modulosxrol.id_modulo), True
        )
        return resultado["id_modulosxrol"]

=======
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

>>>>>>> origin/main
    def actualizar(self, modulosxrol_id: int, modulosxrol: ModulosXRol):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
<<<<<<< HEAD
            cursor.execute("""
                UPDATE modulosxrol
                SET id_rol = %s, id_modulo = %s, actualizado = CURRENT_TIMESTAMP
                WHERE id_modulosxrol = %s
                RETURNING id_modulosxrol;
            """, (modulosxrol.id_rol, modulosxrol.id_modulo, modulosxrol_id))
=======
            query = """
                UPDATE modulosxrol
                SET id_rol = %s, id_modulo = %s
                WHERE id_modulosxrol = %s AND estado = TRUE RETURNING id_modulosxrol;
            """
            cursor.execute(query, (modulosxrol.id_rol, modulosxrol.id_modulo, modulosxrol_id))
>>>>>>> origin/main
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar asignación: {str(e)}")
        finally:
            conn.close()

    def eliminar(self, modulosxrol_id: int):
<<<<<<< HEAD
        """Retira el permiso sin borrar físicamente la relación."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE modulosxrol
                SET estado = FALSE, actualizado = CURRENT_TIMESTAMP
                WHERE id_modulosxrol = %s
                RETURNING id_modulosxrol;
            """, (modulosxrol_id,))
=======
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE modulosxrol SET estado = FALSE WHERE id_modulosxrol = %s RETURNING id_modulosxrol;", (modulosxrol_id,))
>>>>>>> origin/main
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None
        except Exception as e:
            conn.rollback()
<<<<<<< HEAD
            raise Exception(f"Error al retirar asignación: {str(e)}")
        finally:
            conn.close()
=======
            raise Exception(f"Error al eliminar asignación: {str(e)}")
        finally:
            conn.close()
>>>>>>> origin/main
