from flask import render_template, request, redirect, url_for
from app import app, db_connection

@app.route('/anadir_elemento', methods=['GET', 'POST'])
def anadir_elemento():
    if request.method == 'POST':
        # Las entradas ahora son listas
        IDs = request.form.getlist('ID[]')
        PIECEMARKs = request.form.getlist('PIECEMARK[]')
        ESPs = request.form.getlist('ESP[]')
        LINEAs = request.form.getlist('LINEA[]')
        CLASSes = request.form.getlist('CLASS[]')
        QTYs = request.form.getlist('QTY[]')
        WEIGHTs = request.form.getlist('WEIGHT[]')
        RATIOs = request.form.getlist('RATIO[]')
        ZONAs = request.form.getlist('ZONA[]')

        cursor = db_connection.cursor()
        query = """
        INSERT INTO tekladata (ID, PIECEMARK, ESP, LINEA, CLASS, QTY, WEIGHT, RATIO, ZONA, TRASLADO, PRE_ENSAMBLE, MONTAJE, TORQUE, PUNCH)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL, NULL, NULL);
        """

        # Iteramos sobre las entradas y las agregamos a la base de datos
        try:
            for i in range(len(IDs)):
                cursor.execute(query, (IDs[i], PIECEMARKs[i], ESPs[i], LINEAs[i], CLASSes[i], QTYs[i], WEIGHTs[i], RATIOs[i], ZONAs[i]))
            db_connection.commit()
        except Exception as e:
            print("Error: ", e)
            db_connection.rollback()
        finally:
            cursor.close()
        return redirect(url_for('main'))
    return render_template('anadir_elemento.html')


