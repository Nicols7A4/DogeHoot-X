from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

def conectar_bd():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS dogehoot")
        
        connection.select_db('dogehoot')
        
        # with connection.cursor() as cursor:
        #     cursor.execute("""
        #         CREATE TABLE IF NOT EXISTS usuario (
        #             id_usuario INT AUTO_INCREMENT PRIMARY KEY,
        #             nombre_completo VARCHAR(100) NOT NULL,
        #             nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
        #             correo_electronico VARCHAR(255) NOT NULL UNIQUE,
        #             contrasena VARCHAR(255) NOT NULL,
        #             tipo_cuenta VARCHAR(20) NOT NULL,
        #             fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #         )
        #     """)
        # connection.commit() # Aseguramos la creación de la tabla
        return connection
    except pymysql.err.OperationalError as e:
        print(f"Error de conexión operacional: {e}")
        raise 
    except Exception as e:
        print(f"Error inesperado en la conexión a la BD: {e}")
        raise

def validar_usuario(correo, contrasena):
    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario, nombre_completo, nombre_usuario, tipo_cuenta FROM usuarios WHERE correo_electronico=%s AND contrasena=%s",
                (correo, contrasena)
            )
            usuario = cursor.fetchone()
            return usuario
    except pymysql.err.ProgrammingError as e:
        print(f"Error de programación en la validación: {e}")
        raise # Relanzamos para que la ruta lo maneje
    finally:
        if connection:
            connection.close()

# def listar_usuarios():
#     connection = conectar_bd()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM usuario")
#             usuarios = cursor.fetchall()
#             print(f"DEBUG - Usuarios en la BD: {usuarios}")
#             return usuarios
#     except pymysql.err.ProgrammingError as e:
#         print(f"Error de programación al listar: {e}")
#         raise 
#     finally:
#         if connection:
#             connection.close()

def registrar_usuario(nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta):
    """Registra un nuevo usuario. Lanza excepciones si falla."""
    connection = conectar_bd()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario FROM usuario WHERE nombre_usuario=%s OR correo_electronico=%s",
                (nombre_usuario, correo)
            )
            if cursor.fetchone():
                return False, "El nombre de usuario o correo electrónico ya están en uso"
            
            cursor.execute(
                "INSERT INTO usuario (nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta) VALUES (%s, %s, %s, %s, %s)",
                (nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta)
            )
            connection.commit()
            return True, "Usuario registrado exitosamente"
    except pymysql.err.ProgrammingError as e:
        print(f"Error de programación en el registro: {e}")
        raise 
    finally:
        if connection:
            connection.close()

# ====================================


@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            correo = request.form.get('correologin', '').strip()
            contrasena = request.form.get('contrasenaLogin', '').strip()
            
            if not correo or not contrasena:
                return render_template('login.html', mensaje="Por favor, completa todos los campos")
            
            usuario = validar_usuario(correo, contrasena)
            
            if usuario:
                return redirect(url_for('home'))
            else:
                return render_template('login.html', mensaje="Credenciales incorrectas")

        except pymysql.err.OperationalError:
            return render_template('error_sistema.html', mensaje='El servicio de Base de Datos no está disponible.')
        except pymysql.err.ProgrammingError:
            return render_template('error_sistema.html', mensaje='Error en la consulta: La tabla o una de sus columnas no existe.')
        except Exception as e:
            return render_template('error_sistema.html', mensaje=f'Ocurrió un error inesperado: {str(e)}')

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            nombre_completo = request.form.get('nombre', '').strip()
            nombre_usuario = request.form.get('usuario', '').strip()
            correo = request.form.get('correo', '').strip()
            contrasena = request.form.get('contrasena', '').strip()
            tipo_cuenta = request.form.get('tipoCuenta', '').strip()
            
            if not all([nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta]):
                return render_template('registro.html', mensaje="Por favor, completa todos los campos")
            
            if len(contrasena) < 3:
                return render_template('registro.html', mensaje="La contraseña debe tener al menos 3 caracteres")
            
            exito, mensaje = registrar_usuario(nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta)
            
            if exito:
                return render_template('registro.html', mensaje=mensaje, exito=True)
            else:
                return render_template('registro.html', mensaje=mensaje)

        except pymysql.err.OperationalError:
            return render_template('error_sistema.html', mensaje='El servicio de Base de Datos no está disponible.')
        except pymysql.err.ProgrammingError:
            return render_template('error_sistema.html', mensaje='Error en la consulta: La tabla "usuario" o una de sus columnas no existe.')
        except Exception as e:
            return render_template('error_sistema.html', mensaje=f'Ocurrió un error inesperado: {str(e)}')

    return render_template('registro.html')

@app.route("/api_insertarusuarios", methods=["POST"])
def api_insertarusuarios():
    rpta = dict()
    try:
        nombre_completo = request.json["nombre_completo"]
        nombre_usuario = request.json["nombre_usuario"]
        correo_electronico = request.json["correo_electronico"]
        contrasena = request.json["contrasena"]
        tipo_cuenta = request.json["tipo_cuenta"]

        controlador_usuarios.insertar_usuario(
            nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta
        )

        rpta["code"] = 1
        rpta["data"] = {}
        rpta["message"] = "Usuario insertado correctamente"

    except Exception as e:
        rpta["code"] = 0
        rpta["data"] = []
        rpta["message"] = "Ocurrió el siguiente error: " + repr(e)

    return jsonify(rpta)


@app.route("/api_actualizarusuarios", methods=["PUT"])
def api_actualizarusuarios():
    rpta = dict()
    try:
        id_usuario = request.json["id_usuario"]
        nombre_completo = request.json["nombre_completo"]
        nombre_usuario = request.json["nombre_usuario"]
        correo_electronico = request.json["correo_electronico"]
        contrasena = request.json["contrasena"]
        tipo_cuenta = request.json["tipo_cuenta"]

        controlador_usuarios.actualizar_usuario(
            nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta, id_usuario
        )

        rpta["code"] = 1
        rpta["data"] = {}
        rpta["message"] = "Usuario actualizado correctamente"

    except Exception as e:
        rpta["code"] = 0
        rpta["data"] = []
        rpta["message"] = "Ocurrió el siguiente error: " + repr(e)

    return jsonify(rpta)


@app.route("/api_eliminarusuario", methods=['POST'])
def api_eliminarusuario():
    rpta = dict()
    try:
        id_usuario = request.json["id_usuario"]
        controlador_usuarios.eliminar_usuario(id_usuario)
        rpta["code"] = 1
        rpta["data"] = {}
        rpta["message"] = "Usuario eliminado correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["data"] = {}
        rpta["message"] = "Ocurrió el siguiente error: %s" % repr(e)
    return jsonify(rpta)


@app.route("/api_obtenerusuarios")
def api_obtenerusuarios():
    rpta = dict()
    try:
        usuarios = controlador_usuarios.obtener_usuarios()
        rpta["code"] = 1
        rpta["data"] = usuarios
        rpta["message"] = "Usuarios obtenidos correctamente"
    except Exception as e:
        rpta["code"] = 0
        rpta["data"] = []
        rpta["message"] = "Ocurrió el siguiente error: %s" % repr(e)
    return jsonify(rpta)

@app.route('/home')
def home():
    return render_template('home.html')

