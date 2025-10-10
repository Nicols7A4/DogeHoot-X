# cuestionario.py
# CRUD para la entidad "cuestionario"
# Requiere: from bd import obtener_conexion

from bd import obtener_conexion

# ---------------------------
# CREATE
# ---------------------------
def insertar_cuestionario(titulo, descripcion, es_publico, id_propietario):
    """
    Inserta un cuestionario.
    es_publico: bool | int (True/1 = público, False/0 = privado)
    """
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO cuestionario (titulo, descripcion, es_publico, id_propietario)
            VALUES (%s, %s, %s, %s)
            """,
            (titulo, descripcion, 1 if es_publico else 0, id_propietario)
        )
    conexion.commit()
    conexion.close()


# ---------------------------
# READ
# ---------------------------
def obtener_cuestionarios():
    """
    Devuelve todos los cuestionarios.
    """
    conexion = obtener_conexion()
    data = []
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_cuestionario, titulo, descripcion, es_publico, id_propietario,
                   fecha_creacion, fecha_actualizacion
            FROM cuestionario
            ORDER BY fecha_creacion DESC, id_cuestionario DESC
            """
        )
        data = cursor.fetchall()
    conexion.close()
    return data


def obtener_cuestionarios_por_propietario(id_propietario):
    """
    Devuelve los cuestionarios filtrados por propietario (docente).
    """
    conexion = obtener_conexion()
    data = []
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_cuestionario, titulo, descripcion, es_publico, id_propietario,
                   fecha_creacion, fecha_actualizacion
            FROM cuestionario
            WHERE id_propietario = %s
            ORDER BY fecha_creacion DESC, id_cuestionario DESC
            """,
            (id_propietario,)
        )
        data = cursor.fetchall()
    conexion.close()
    return data


def obtener_cuestionarios_publicos():
    """
    Devuelve sólo los cuestionarios marcados como públicos (repositorio).
    """
    conexion = obtener_conexion()
    data = []
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_cuestionario, titulo, descripcion, es_publico, id_propietario,
                   fecha_creacion, fecha_actualizacion
            FROM cuestionario
            WHERE es_publico = 1
            ORDER BY fecha_creacion DESC, id_cuestionario DESC
            """
        )
        data = cursor.fetchall()
    conexion.close()
    return data


def buscar_cuestionarios(texto):
    """
    Búsqueda simple por título o descripción.
    """
    like = f"%{texto}%"
    conexion = obtener_conexion()
    data = []
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_cuestionario, titulo, descripcion, es_publico, id_propietario,
            fecha_creacion, fecha_actualizacion
            FROM cuestionario
            WHERE titulo LIKE %s OR descripcion LIKE %s
            ORDER BY fecha_creacion DESC, id_cuestionario DESC
            """,
            (like, like)
        )
        data = cursor.fetchall()
    conexion.close()
    return data


def obtener_cuestionario_por_id(id_cuestionario):
    """
    Devuelve un cuestionario por su ID.
    """
    conexion = obtener_conexion()
    row = None
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_cuestionario, titulo, descripcion, es_publico, id_propietario,
            fecha_creacion, fecha_actualizacion
            FROM cuestionario
            WHERE id_cuestionario = %s
            """,
            (id_cuestionario,)
        )
        row = cursor.fetchone()
    conexion.close()
    return row


# ---------------------------
# UPDATE
# ---------------------------
def actualizar_cuestionario(titulo, descripcion, es_publico, id_propietario, id_cuestionario):
    """
    Actualiza título, descripción, visibilidad y propietario.
    """
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            UPDATE cuestionario
            SET titulo = %s,
                descripcion = %s,
                es_publico = %s,
                id_propietario = %s
            WHERE id_cuestionario = %s
            """,
            (titulo, descripcion, 1 if es_publico else 0, id_propietario, id_cuestionario)
        )
    conexion.commit()
    conexion.close()


def publicar_cuestionario(id_cuestionario, publicar=True):
    """
    Cambia el estado público/privado del cuestionario.
    publicar=True -> es_publico = 1
    """
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            """
            UPDATE cuestionario
            SET es_publico = %s
            WHERE id_cuestionario = %s
            """,
            (1 if publicar else 0, id_cuestionario)
        )
    conexion.commit()
    conexion.close()


# ---------------------------
# DELETE
# ---------------------------
def eliminar_cuestionario(id_cuestionario):
    """
    Elimina un cuestionario por ID.
    OJO: si tienes FK a preguntas/opciones, configura ON DELETE CASCADE en la BD
    o borra en orden desde el backend.
    """
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM cuestionario WHERE id_cuestionario = %s", (id_cuestionario,))
    conexion.commit()
    conexion.close()


def eliminar_cuestionarios_all():
    """
    Borra todos los cuestionarios (uso sólo para pruebas).
    """
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM cuestionario")
    conexion.commit()
    conexion.close()
