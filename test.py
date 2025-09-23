from flask import Flask, render_template, request, url_for, redirect
import pymysql.cursors

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("registro.html")

def registro():
    return render_template("registro.html")

def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='dawa_bd',
            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        return None
    
@app.route("/probarconexion")
def probarconexion():
    conexion = obtenerconexion()
    if conexion is None:
        return "<p>Error en la conexión</p>"
    return "<p>Conexión exitosa</p>"

@app.route("/verificarRegistro", methods=['POST'])
def verificarRegistro():
    return nuevoUsuario()

def nuevoUsuario():
    nombre = request.form['nombre']
    usuario =  request.form['usuario']
    correo =  request.form['correo']
    contrasena =  request.form['contrasena']
    tipoCuenta =  request.form['tipoCuenta']
    connection = obtenerconexion()
    if connection:
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT `email`,`contrasena` FROM `tabla` WHERE `usuario`=%s and `correo`=%s"
                cursor.execute(sql, (id))
                result = cursor.fetchone()
            if result:
                connection.commit()
                return "<p>El usuario o el correo ya se encuentra en uso, por favor eliga otro</p>"
            else:
                sql = "INSERT INTO `tabla` (`email`) VALUES (%s)"
                cursor.execute(sql, (id))
                result = cursor.fetchone()
                connection.commit()
                return "<p>Registro correcto, inicie sesión para comprobar su cuenta</p>"
        return "<p>VACIO</p>"
    return render_template('error_sistema.html',mensaje='Servicio de BD no disponible')
