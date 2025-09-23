from flask import Flask, request, render_template, redirect, url_for, flash
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para usar flash messages

# ====================================
# FUNCIONES DE BASE DE DATOS
# ====================================

def conectar_bd():
    """Conecta a la base de datos MySQL y crea la BD y tabla si no existen"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        
        # Crear base de datos si no existe
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS dogehoot")
        
        # Seleccionar la base de datos
        connection.select_db('dogehoot')
        
        # Crear tabla usuario si no existe (sin borrar datos existentes)
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuario (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_completo VARCHAR(100) NOT NULL,
                    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
                    correo_electronico VARCHAR(255) NOT NULL UNIQUE,
                    contrasena VARCHAR(255) NOT NULL,
                    tipo_cuenta VARCHAR(20) NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        return connection
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def validar_usuario(correo, contrasena):
    """Valida las credenciales del usuario"""
    connection = conectar_bd()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_usuario, nombre_completo, nombre_usuario, tipo_cuenta FROM usuario WHERE correo_electronico=%s AND contrasena=%s",
                (correo, contrasena)
            )
            usuario = cursor.fetchone()
            return usuario
    except Exception as e:
        print(f"Error validando usuario: {e}")
        return None
    finally:
        connection.close()

def listar_usuarios():
    """Lista todos los usuarios registrados para debug"""
    connection = conectar_bd()
    if not connection:
        print("No se pudo conectar a la BD")
        return []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM usuario")
            usuarios = cursor.fetchall()
            print(f"DEBUG - Usuarios en la BD: {usuarios}")
            return usuarios
    except Exception as e:
        print(f"Error listando usuarios: {e}")
        return []
    finally:
        connection.close()

def registrar_usuario(nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta):
    """Registra un nuevo usuario en la base de datos"""
    connection = conectar_bd()
    if not connection:
        return False, "Error de conexión a la base de datos"
    
    try:
        with connection.cursor() as cursor:
            # Verificar si el usuario o correo ya existen
            cursor.execute(
                "SELECT id_usuario FROM usuario WHERE nombre_usuario=%s OR correo_electronico=%s",
                (nombre_usuario, correo)
            )
            if cursor.fetchone():
                return False, "El nombre de usuario o correo electrónico ya están en uso"
            
            # Insertar nuevo usuario
            cursor.execute(
                "INSERT INTO usuario (nombre_completo, nombre_usuario, correo_electronico, contrasena, tipo_cuenta) VALUES (%s, %s, %s, %s, %s)",
                (nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta)
            )
            return True, "Usuario registrado exitosamente"
    except Exception as e:
        print(f"Error registrando usuario: {e}")
        return False, f"Error en el registro: {str(e)}"
    finally:
        connection.close()

# ====================================
# RUTAS PRINCIPALES
# ====================================

@app.route('/')
def inicio():
    """Página de inicio - Landing page"""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DogeHoot-X</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                background-color: #f5f5f5; 
                margin: 0; 
                padding: 50px;
            }
            h1 { 
                color: #4a90e2; 
                font-size: 3rem; 
                margin-bottom: 1rem;
            }
            p { 
                font-size: 1.2rem; 
                color: #666; 
                margin-bottom: 2rem;
            }
            .btn { 
                display: inline-block; 
                padding: 12px 30px; 
                margin: 10px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-size: 1.1rem; 
                transition: all 0.3s;
            }
            .btn-primary { 
                background-color: #4a90e2; 
                color: white; 
            }
            .btn-primary:hover { 
                background-color: #357abd; 
            }
            .btn-secondary { 
                background-color: #6c757d; 
                color: white; 
            }
            .btn-secondary:hover { 
                background-color: #545b62; 
            }
        </style>
    </head>
    <body>
        <h1>🐕 DogeHoot-X</h1>
        <p>¡Bienvenido a la plataforma de cuestionarios más divertida!</p>
        <a href="/login" class="btn btn-primary">Iniciar Sesión</a>
        <a href="/registro" class="btn btn-secondary">Registrarse</a>
    </body>
    </html>
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if request.method == 'POST':
        correo = request.form.get('correologin', '').strip()
        contrasena = request.form.get('contrasenaLogin', '').strip()
        
        print(f"DEBUG LOGIN - Intentando login con:")
        print(f"  correo: '{correo}'")
        print(f"  contrasena: '{contrasena}'")
        
        if not correo or not contrasena:
            return render_template('login.html', mensaje="Por favor, completa todos los campos")
        
        usuario = validar_usuario(correo, contrasena)
        print(f"DEBUG LOGIN - Resultado validación: {usuario}")
        
        if usuario:
            # Aquí podrías usar sesiones para mantener al usuario logueado
            # session['usuario_id'] = usuario['id_usuario']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', mensaje="Credenciales incorrectas")
    
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios"""
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre', '').strip()
        nombre_usuario = request.form.get('usuario', '').strip()
        correo = request.form.get('correo', '').strip()
        contrasena = request.form.get('contrasena', '').strip()
        tipo_cuenta = request.form.get('tipoCuenta', '').strip()
        
        # Debug: imprimir los valores recibidos
        print(f"DEBUG - Datos recibidos:")
        print(f"  nombre_completo: '{nombre_completo}'")
        print(f"  nombre_usuario: '{nombre_usuario}'")
        print(f"  correo: '{correo}'")
        print(f"  contrasena: '{contrasena}'")
        print(f"  tipo_cuenta: '{tipo_cuenta}'")
        
        # Validaciones básicas
        if not all([nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta]):
            return render_template('registro.html', mensaje="Por favor, completa todos los campos")
        
        if len(contrasena) < 3:  # Reducido para pruebas
            return render_template('registro.html', mensaje="La contraseña debe tener al menos 3 caracteres")
        
        # Intentar registrar usuario
        exito, mensaje = registrar_usuario(nombre_completo, nombre_usuario, correo, contrasena, tipo_cuenta)
        
        if exito:
            return render_template('registro.html', mensaje=mensaje, exito=True)
        else:
            return render_template('registro.html', mensaje=mensaje)
    
    return render_template('registro.html')

@app.route('/home')
def home():
    """Página principal después del login"""
    # Aquí podrías verificar si el usuario está logueado
    # if 'usuario_id' not in session:
    #     return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/debug')
def debug():
    """Ruta de debug para ver usuarios registrados"""
    usuarios = listar_usuarios()
    return f"<h1>Debug - Usuarios registrados:</h1><pre>{usuarios}</pre><br><a href='/'>Volver al inicio</a>"

# ====================================
# FUNCIÓN PRINCIPAL
# ====================================

if __name__ == '__main__':
    app.run(debug=True)
