from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
from datetime import datetime

app = Flask(__name__)

# CONEXIÓN
def obtener_conexion():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='',
            database='test',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print("Error de conexión:", e)
        return None


# AGREGAR CUESTIONARIO
@app.route('/')
def formulario_cuestionario():
    return render_template('agregar_cuestionario.html')

# GUARDAR CUESTIONARIO
@app.route('/guardar', methods=['POST'])
def guardar():
    try:
        if request.is_json:
            data = request.get_json()
            titulo = data.get('titulo')
            descripcion = data.get('descripcion')
            es_publico = data.get('es_publico', False)
            id_propietario = data.get('id_propietario')
            id_cuestionario_origen = data.get('id_cuestionario_origen')
        else:
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            es_publico = True if request.form.get('es_publico') == 'on' else False
            id_propietario = request.form['id_propietario']
            id_cuestionario_origen = request.form.get('id_cuestionario_origen')

        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conexion = obtener_conexion()
        if conexion is None:
            return jsonify({'mensaje': 'Error al conectar a la base de datos'}), 500

        with conexion.cursor() as cursor:
            sql = """
                INSERT INTO cuestionario 
                (titulo, descripcion, es_publico, id_propietario, fecha_creacion, fecha_actualizacion, id_cuestionario_origen)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                titulo, 
                descripcion, 
                es_publico, 
                id_propietario, 
                fecha_actual, 
                fecha_actual, 
                id_cuestionario_origen
            ))
            conexion.commit()

        conexion.close()

        if request.is_json:
            return jsonify({'mensaje': 'Cuestionario registrado correctamente'})
        else:
            return redirect(url_for('listar'))

    except Exception as e:
        print("Error al guardar:", e)
        return jsonify({'mensaje': 'Error al registrar el cuestionario', 'error': str(e)}), 500


# LISTAR CUESTIONARIOS
@app.route('/listar')
def listar():
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return "Error al conectar a la base de datos"

        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM cuestionario")
            cuestionarios = cursor.fetchall()

        conexion.close()
        return render_template('listar_cuestionarios.html', cuestionarios=cuestionarios)
    except Exception as e:
        print("Error al listar:", e)
        return f"Error al listar los cuestionarios: {e}"


if __name__ == '__main__':
    app.run(debug=True)
