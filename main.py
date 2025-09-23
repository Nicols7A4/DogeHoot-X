from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

app = Flask(__name__)


def conectar_a_bd():
    conexion = None
    return conexion


def obtener_usuario():
    user_id = request.args.get('user_id')
    if not user_id: redirect(url_for('home'))
    user = None # Buscar en BD
    return user

# Funcion para conectar a la base de datos y asegurar que la tabla exista - Lo agregó Pame
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
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS dogehoot "
            )
        connection.select_db('dogehoot')
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_usuario VARCHAR(100) NOT NULL,
                    correo_electronico VARCHAR(255) NOT NULL UNIQUE,
                    contrasena VARCHAR(255) NOT NULL
                )
                """
            )
        return connection
    except Exception:
        connection.close()
        raise

@app.route('/')
def home():
    return """
                <h1>Hola</h1>
                <a href="/login">Login</a>
                <a href="/registro">Registro</a>
            """

@app.route('/registro', methods=['GET','POST'])
def registro():
    return render_template('registro.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        
        print(correo, password)
        
    return render_template('login.html')
