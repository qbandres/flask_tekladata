from app import app, db_connection
from flask import render_template, request, session, redirect, url_for, jsonify
from .consulta_sql import ConsultaMain


@app.route('/agregar_montaje')
def agregar_montaje():
    cursor = db_connection.cursor()
    cursor.execute("SELECT id, piecemark, esp, linea, class, qty, weight, ratio, zona FROM est_tekladata WHERE ID = 1")
    datos_estaticos = cursor.fetchone()
    cursor.close()

    # Obtén el filtro de búsqueda del parámetro de consulta
    search_filter = request.args.get('search_filter', '')

    return render_template('agregar_montaje.html', datos_estaticos=datos_estaticos, search_filter=search_filter)

@app.route('/actualizar_montaje', methods=['POST'])
def actualizar_montaje():
    if 'username' in session:
        # Convertir ImmutableMultiDict a un diccionario mutable
        data = dict(request.form)

        # Reemplazar fechas vacías con '00-00-0000'
        for field in ['traslado', 'preEnsamble', 'montaje', 'torque', 'punch']:
            if not data[field]:
                data[field] = None

        cursor = db_connection.cursor()
        query = """
            UPDATE est_tekladata SET 
                TRASLADO = %s, 
                PRE_ENSAMBLE = %s, 
                MONTAJE = %s, 
                TORQUE = %s, 
                PUNCH = %s 
            WHERE ID = %s
        """
        cursor.execute(query, (
            data['traslado'], 
            data['preEnsamble'], 
            data['montaje'], 
            data['torque'], 
            data['punch'], 
            data['id']
        ))
        db_connection.commit()
        cursor.close()
        return jsonify({"success": True})
    else:
        return redirect(url_for('index'))

@app.route('/procesar_busqueda_actualizar', methods=['POST'])
def handle_procesar_busqueda_actualizar():
    consulta = ConsultaMain()
    return consulta.procesar_busqueda_actualizar()
