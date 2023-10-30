from flask import render_template,request,session,redirect,url_for
from app import app,usuarios


# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in usuarios and usuarios[username] == password:
        # Iniciar sesión y redirigir a la página principal
        session['username'] = username
        return redirect(url_for('main'))
    else:
        # Mostrar un mensaje de error en caso de credenciales incorrectas
        return render_template('index.html', error='Credenciales incorrectas')