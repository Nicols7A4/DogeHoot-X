from bd import obtener_conexion


def insertar_usuario(nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "INSERT INTO usuario(nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta) "
            "VALUES (%s, %s, %s, %s, %s)",
            (nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta)
        )
    conexion.commit()
    conexion.close()


def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id_usuario, nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta, fecha_registro FROM usuario")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
    conexion.commit()
    conexion.close()


def eliminar_usuario_all():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM usuario")
    conexion.commit()
    conexion.close()


def obtener_usuario_por_id(id_usuario):
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id_usuario, nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta, fecha_registro "
            "FROM usuario WHERE id_usuario = %s", (id_usuario,)
        )
        usuario = cursor.fetchone()
    conexion.close()
    return usuario


def actualizar_usuario(nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta, id_usuario):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE usuario SET nombre_completo = %s, nombre_usuario = %s, correo_electronico = %s, contrasena = %s, tipo_cuenta = %s "
            "WHERE id_usuario = %s",
            (nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta, id_usuario)
        )
    conexion.commit()
    conexion.close()
