from flask import Flask, request, render_template, redirect, url_for
import pymysql.cursors

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hola</h1>"