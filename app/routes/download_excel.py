import pandas as pd
from flask import Response
from app import app, db_connection
from io import BytesIO

@app.route('/download_excel')
def download_excel():
    cursor = db_connection.cursor()

    # Obtener todos los datos de la tabla "tekladata"
    cursor.execute("SELECT * FROM tekladata")
    table_data = cursor.fetchall()

    # Convertir los datos a DataFrame de pandas
    df = pd.DataFrame(table_data, columns=[i[0] for i in cursor.description])

    # Cerrar cursor
    cursor.close()

    # Convertir el DataFrame a Excel usando un buffer en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    output.seek(0)  # Regresar al inicio del BytesIO buffer

    # Crear respuesta para descargar
    response = Response(output.getvalue(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = "attachment; filename=datos_tekladata.xlsx"
    
    return response