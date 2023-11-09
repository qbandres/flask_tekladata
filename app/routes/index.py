from flask import render_template,request,session,redirect,url_for,flash
from app import app,usuarios


# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        # Aquí iría la lógica de verificación de las credenciales del usuario

        if username in usuarios and usuarios[username] == password:
            # Iniciar sesión y redirigir a la página principal
            session['username'] = username
            return redirect(url_for('main'))
        else:
            # Mostrar un mensaje de error en caso de credenciales incorrectas
            flash('Credenciales incorrectas', 'error')
            return render_template('index.html')

    except Exception as e:
        # Capturar cualquier otra excepción inesperada durante el proceso de inicio de sesión
        flash(f'Error inesperado al intentar iniciar sesión: {str(e)}', 'error')
        app.logger.error(f'Error inesperado en login: {str(e)}')
        return render_template('index.html')