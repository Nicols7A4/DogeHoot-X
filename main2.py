from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

CONFIG_BD = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'dogehoot',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# --- BASE DE DATOS ---

def obtener_conexion():
    try:
        # Primero, conexión sin base de datos para crearla si no existe
        conexion_inicial = pymysql.connect(host=CONFIG_BD['host'], user=CONFIG_BD['user'], password=CONFIG_BD['password'])
        with conexion_inicial.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS dogehoot")
        conexion_inicial.close()

        # Conexión definitiva a la base de datos 'dogehoot'
        conexion = pymysql.connect(**CONFIG_BD)

        # Se asegura de que la tabla 'usuario' exista
        with conexion.cursor() as cursor:
            sentencia_sql = """
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre_completo VARCHAR(100) NOT NULL,
                nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
                correo_electronico VARCHAR(255) NOT NULL UNIQUE,
                contrasena VARCHAR(255) NOT NULL,
                tipo_cuenta VARCHAR(20) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
            cursor.execute(sentencia_sql)
        conexion.commit()
        return conexion
    except pymysql.err.OperationalError as error:
        print(f"Error de conexión a la Base de Datos: {error}")
        raise

def verificar_credenciales(correo, contrasena):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM usuario WHERE correo_electronico = %s AND contrasena = %s"
            cursor.execute(sql, (correo, contrasena))
            usuario_encontrado = cursor.fetchone()
            return usuario_encontrado
    finally:
        if conexion:
            conexion.close()

def crear_nuevo_usuario(nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cursor:
            # 1. Verificar si el usuario o correo ya existen
            sql_verificar = "SELECT id_usuario FROM usuario WHERE nombre_usuario = %s OR correo_electronico = %s"
            cursor.execute(sql_verificar, (nombre_usuario, correo))
            if cursor.fetchone():
                return False, "El nombre de usuario o correo ya está en uso."

            # 2. Si no existen, insertar el nuevo usuario
            sql_insertar = """
                INSERT INTO usuario (nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta)
                VALUES (%s, %s, %s, %s, %s)
            """
            valores = (nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta)
            cursor.execute(sql_insertar, valores)
        
        conexion.commit()
        return True, "¡Usuario registrado con éxito!"
    finally:
        if conexion:
            conexion.close()

# --- RUTAS DE LA APLICACIÓN (Controladores) ---

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
                return render_template('login.html', mensaje="Por favor, completa todos los campos.")
            
            usuario = verificar_credenciales(correo, contrasena)

            if usuario:
                return redirect(url_for('home')) # Redirige a la página principal de la app
            else:
                return render_template('login.html', mensaje="Credenciales incorrectas. Inténtalo de nuevo.")

        # Manejo centralizado de errores de base de datos
        except pymysql.err.OperationalError:
            return render_template('error_sistema.html', mensaje='El servicio de Base de Datos no está disponible.')
        except pymysql.err.ProgrammingError:
            return render_template('error_sistema.html', mensaje='Error en la consulta: La tabla o una de sus columnas no existe.')
        except Exception as error:
            return render_template('error_sistema.html', mensaje=f'Ocurrió un error inesperado: {str(error)}')

    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre_completo = request.form.get('nombre', '').strip()
            nombre_usuario = request.form.get('usuario', '').strip()
            correo = request.form.get('correo', '').strip()
            contrasena = request.form.get('contrasena', '').strip()
            tipo_cuenta = request.form.get('tipoCuenta', '').strip()

            # Validaciones básicas
            if not all([nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta]):
                return render_template('registro.html', mensaje="Por favor, completa todos los campos.")
            if len(contrasena) < 3:
                return render_template('registro.html', mensaje="La contraseña debe tener al menos 3 caracteres.")
            
            # Intentar crear el usuario
            fue_exitoso, mensaje_resultado = crear_nuevo_usuario(nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta)

            if fue_exitoso:
                return render_template('registro.html', mensaje=mensaje_resultado, exito=True)
            else:
                return render_template('registro.html', mensaje=mensaje_resultado)

        # Manejo centralizado de errores de base de datos
        except pymysql.err.OperationalError:
            return render_template('error_sistema.html', mensaje='El servicio de Base de Datos no está disponible.')
        except pymysql.err.ProgrammingError:
            return render_template('error_sistema.html', mensaje='Error en la consulta: La tabla "usuario" o una de sus columnas no existe.')
        except Exception as error:
            return render_template('error_sistema.html', mensaje=f'Ocurrió un error inesperado: {str(error)}')
    
    return render_template('registro.html')

@app.route('/home')
def home():
    return render_template('home.html')

# --- EJECUCIÓN DE LA APLICACIÓN ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)