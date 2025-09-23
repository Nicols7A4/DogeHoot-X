from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

app = Flask(__name__)


def conectar_a_bd():
    conexion = None
    return conexion


def obtener_usuario():
    user_id = request.args.get('user_id')
    if not user_id:
        return redirect(url_for('inicio'))
    user = None  # Buscar en BD
    return user

# Funcion para conectar a la base de datos y asegurar que la tabla exista - Lo agrego Pame
def conexion(host='localhost', user='root', password='', charset='utf8mb4'):
    """Ensure the dogehoot database and usuario table exist, then return a connection."""
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        charset=charset,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS dogehoot")
        connection.select_db('dogehoot')
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
                    correo_electronico VARCHAR(255) NOT NULL UNIQUE,
                    contrasena VARCHAR(255) NOT NULL,
                    tipo char(1) not null
                )
                """
            )
        return connection
    except Exception:
        connection.close()
        #raise
        return None

@app.route('/')
def inicio():
    return """
                <h1>Hola</h1>
                <a href="/login">Login</a>
                <a href="/registro">Registro</a>
            """

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    # return render_template('registro.html')
    return redirect(url_for('verificarRegistro'))

@app.route('/verificarRegistro', methods=['GET','POST'])
def verificarRegistro():
    return render_template('registro.html')

def nuevoUsuario():
    nombre = request.form['nombre']
    usuario =  request.form['usuario']
    correo =  request.form['correo']
    contrasena =  request.form['contrasena']
    tipoCuenta =  request.form['tipoCuenta']
    connection = conexion()
    
    print(nombre, usuario, correo, contrasena, tipoCuenta)
    
    if connection:
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT `correo_electronico`,`contrasena` FROM `usuario` WHERE `nombre_usuario`=%s or `correo_electronico`=%s"
                cursor.execute(sql, (id))
                result = cursor.fetchone()
            if result:
                connection.commit()
                return "<p>El usuario o el correo ya se encuentra en uso, por favor eliga otro</p>"
            else:
                sql = "INSERT INTO `usuario` (`correo_electronico`) VALUES (%s)"
                cursor.execute(sql, (id))
                result = cursor.fetchone()
                connection.commit()
                return "<p>Registro correcto, inicie sesión para comprobar su cuenta</p>"
        return "<p>VACIO</p>"
    return "<p>No fue posible contactar con la base de datos</p>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correologin']
        password = request.form['contrasenaLogin']
        error = None

        print(correo, password)

        usuario = None
        conn = None
        try:
            conn = conexion()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id_usuario FROM usuario WHERE correo_electronico=%s AND contrasena=%s",
                    (correo, password)
                )
                usuario = cursor.fetchone()
        except Exception as exc:
            error = f'Error al consultar la base de datos: {exc}'
        finally:
            if conn is not None:
                conn.close()

        if usuario and not error:
            error = 'Inicio de sesion correcto. Bienvenido al sistema!'
        elif not error:
            error = 'Las credenciales ingresadas son incorrectas'

        return render_template('login.html', mensaje=error)

    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')
