from flask import render_template,request
from app import app, db_connection


@app.route('/agregar_montaje')
def agregar_montaje():
    cursor = db_connection.cursor()
    cursor.execute("SELECT id, piecemark, esp, linea, class, qty, weight, ratio, zona FROM tekladata WHERE ID = 1")
    datos_estaticos = cursor.fetchone()
    cursor.close()

    # Obtén el filtro de búsqueda del parámetro de consulta
    search_filter = request.args.get('search_filter', '')

    return render_template('agregar_montaje.html', datos_estaticos=datos_estaticos, search_filter=search_filter)