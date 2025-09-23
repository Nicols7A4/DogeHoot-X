from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

@app.route('/')
def home():
    return """
                <h1>Hola</h1>
                <a href="/login">Login</a>
                <a href="/registro">Registro</a>
            """

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/login')
def login():
    return render_template('login.html')