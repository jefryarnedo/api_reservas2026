from app.core.database import Database
from app.models.reserva import Reserva

class ReservaRepository:
    def __init__(self):
        self.db = Database()

    def obtener_todas(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM reserva WHERE estado = TRUE ORDER BY id_reserva DESC;")
            reservas = cursor.fetchall()
            return reservas
        except Exception as e:
            raise Exception(f"Error al obtener reservas: {str(e)}")
        finally:
            conn.close()

    def obtener_por_id(self, reserva_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s AND estado = TRUE;", (reserva_id,))
            reserva = cursor.fetchone()
            return reserva
        except Exception as e:
            raise Exception(f"Error al obtener reserva por ID: {str(e)}")
        finally:
            conn.close()

    def crear(self, reserva: Reserva):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO reserva
                (id_usuario, id_espacio, id_tipo_evento, id_aprobador, fecha_reserva, hora_inicio,
                 hora_fin, cantidad_asistentes, estado_reserva, fecha_limite_aprobacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_reserva;
            """
            cursor.execute(query, (
                reserva.id_usuario, reserva.id_espacio, reserva.id_tipo_evento, reserva.id_aprobador,
                reserva.fecha_reserva, reserva.hora_inicio, reserva.hora_fin,
                reserva.cantidad_asistentes, reserva.estado_reserva, reserva.fecha_limite_aprobacion
            ))
            nuevo_id = cursor.fetchone()['id_reserva']
            conn.commit()
            return nuevo_id
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al crear reserva: {str(e)}")
        finally:
            conn.close()

    def actualizar(self, reserva_id: int, reserva: Reserva):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE reserva
                SET id_usuario = %s, id_espacio = %s, id_tipo_evento = %s, id_aprobador = %s,
                    fecha_reserva = %s, hora_inicio = %s, hora_fin = %s, cantidad_asistentes = %s,
                    estado_reserva = %s, fecha_limite_aprobacion = %s
                WHERE id_reserva = %s AND estado = TRUE
                RETURNING id_reserva;
            """
            cursor.execute(query, (
                reserva.id_usuario, reserva.id_espacio, reserva.id_tipo_evento, reserva.id_aprobador,
                reserva.fecha_reserva, reserva.hora_inicio, reserva.hora_fin,
                reserva.cantidad_asistentes, reserva.estado_reserva, reserva.fecha_limite_aprobacion,
                reserva_id
            ))
            actualizado = cursor.fetchone()
            conn.commit()
            return actualizado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al actualizar reserva: {str(e)}")
        finally:
            conn.close()

    def eliminar(self, reserva_id: int):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE reserva SET estado = FALSE WHERE id_reserva = %s RETURNING id_reserva;", (reserva_id,))
            eliminado = cursor.fetchone()
            conn.commit()
            return eliminado is not None
        except Exception as e:
            conn.rollback()
            raise Exception(f"Error al eliminar reserva: {str(e)}")
        finally:
            conn.close()