from flask import render_template, request, session, redirect, url_for, jsonify
from app import app, db_connection, usuarios

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
            UPDATE tekladata SET 
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
