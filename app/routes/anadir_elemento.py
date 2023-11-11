from flask import render_template, request, redirect, url_for
from app import app, db_connection

# Define una ruta en tu aplicación Flask con el decorador @app.route.
@app.route('/anadir_elemento', methods=['GET', 'POST'])
def anadir_elemento():
    # Verifica si el método de la solicitud es POST (cuando se envía el formulario).
    if request.method == 'POST':
        # Obtener datos del formulario. Cada uno de estos campos corresponde a una lista
        # debido al uso de getlist. Esto sugiere que el formulario puede enviar múltiples valores
        # para cada uno de estos campos.
        IDs = request.form.getlist('ID[]')
        PIECEMARKs = request.form.getlist('PIECEMARK[]')
        ESPs = request.form.getlist('ESP[]')
        LINEAs = request.form.getlist('LINEA[]')
        CLASSes = request.form.getlist('CLASS[]')
        QTYs = request.form.getlist('QTY[]')
        WEIGHTs = request.form.getlist('WEIGHT[]')
        RATIOs = request.form.getlist('RATIO[]')
        ZONAs = request.form.getlist('ZONA[]')

        # Inicia una nueva operación en la base de datos.
        cursor = db_connection.cursor()
        # Prepara la consulta SQL para insertar datos en la tabla 'est_tekladata'.
        query = """
        INSERT INTO est_tekladata (ID, PIECEMARK, ESP, LINEA, CLASS, QTY, WEIGHT, RATIO, ZONA, TRASLADO, PRE_ENSAMBLE, MONTAJE, TORQUE, PUNCH)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL, NULL, NULL);
        """

        # Intenta ejecutar la consulta SQL para cada fila de datos obtenidos del formulario.
        try:
            for i in range(len(IDs)):
                cursor.execute(query, (IDs[i], PIECEMARKs[i], ESPs[i], LINEAs[i], CLASSes[i], QTYs[i], WEIGHTs[i], RATIOs[i], ZONAs[i]))
            db_connection.commit()  # Confirma la transacción si todas las inserciones son exitosas.
        except Exception as e:
            print("Error: ", e)  # Imprime cualquier error que ocurra durante la inserción.
            db_connection.rollback()  # Revierte la transacción en caso de error.
        finally:
            cursor.close()  # Cierra el cursor para liberar los recursos de la base de datos.

        # Redirige al usuario a otra página (usualmente la principal) después de procesar el formulario.
        return redirect(url_for('main'))

    # Si el método de la solicitud no es POST (es decir, GET), simplemente renderiza y muestra
    # el formulario para añadir elementos.
    return render_template('anadir_elemento.html')



