from app import app, db_connection
from flask import jsonify,request

@app.route('/procesar_busqueda', methods=['POST'])
def procesar_busqueda():
    search_filter = request.form.get('search_filter')
    
    # Aquí asumimos que deseas buscar coincidencias en la columna 'piecemark'
    cursor = db_connection.cursor()
    query = "SELECT * FROM tekladata WHERE PIECEMARK LIKE %s"
    cursor.execute(query, ('%' + search_filter + '%',))
    resultados = cursor.fetchall()
    cursor.close()

    # Convertir los resultados a una lista de diccionarios o similar, según sea necesario
    search_results = [{"ID": res[0], "PIECEMARK": res[1],"ESP": res[2],"LINEA": res[3],"CLASS": res[4],"QTY": res[5],"WEIGHT": res[6],"RATIO": res[7],"ZONA": res[8],"TRASLADO": res[9],"PRE_ENSAMBLE": res[10],"MONTAJE": res[11],"TORQUE": res[12],"PUNCH": res[13]} for res in resultados]
    
    return jsonify({"search_results": search_results})
