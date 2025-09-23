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