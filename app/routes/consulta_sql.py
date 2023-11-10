from app import db_connection
import pandas as pd
from flask import request,jsonify,Response
import ast
from io import BytesIO


class ConsultaMain:
    def __init__(self):
        pass
    def regular_fetchall(self, query, params=None):
        # Se abre una nueva conexión y se crea un nuevo cursor
        cursor = db_connection.cursor()

        # Ejecutamos la consulta. "params" es una tupla de valores
        # que se pasan de forma segura a la consulta para evitar la inyección SQL.
        cursor.execute(query, params or ())

        # Obtenemos todos los datos devueltos por la consulta
        table_data = cursor.fetchall()

        # Cerramos el cursor
        cursor.close()

        # Retornamos los datos obtenidos
        return table_data
    def regular_df(self, query, params=None):
        """
        Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de Pandas.
        
        Args:
        query (str): La consulta SQL a ejecutar.
        params (tuple, optional): Los parámetros a usar en la consulta SQL. Por defecto es None.

        Returns:
        DataFrame: Un DataFrame de Pandas con los resultados de la consulta SQL.
        """

        # Abre una nueva conexión y crea un nuevo cursor
        cursor = db_connection.cursor()

        # Ejecuta la consulta SQL, utilizando parámetros para prevenir inyección SQL
        cursor.execute(query, params or ())

        # Recupera todos los datos devueltos por la consulta
        table_data = cursor.fetchall()

        # Obtiene dinámicamente los nombres de las columnas de los metadatos de la consulta
        column_names = [description[0] for description in cursor.description]

        # Cierra el cursor
        cursor.close()

        # Crea y devuelve un DataFrame de Pandas con los datos y nombres de columna
        df = pd.DataFrame(table_data, columns=column_names)
        return df
    def procesar_busqueda_actualizar(self):
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
    
    def regular_list(self, query, params=None):
        """
        Ejecuta una consulta SQL y devuelve los resultados en un DataFrame de Pandas.
        
        Args:
        query (str): La consulta SQL a ejecutar.
        params (tuple, optional): Los parámetros a usar en la consulta SQL. Por defecto es None.

        Returns:
        DataFrame: Un DataFrame de Pandas con los resultados de la consulta SQL.
        """

        # Abre una nueva conexión y crea un nuevo cursor
        cursor = db_connection.cursor()

        # Ejecuta la consulta SQL, utilizando parámetros para prevenir inyección SQL
        cursor.execute(query, params or ())

        # Recupera todos los datos devueltos por la consulta
        table_data = cursor.fetchall()

        # Obtiene dinámicamente los nombres de las columnas de los metadatos de la consulta
        column_names = [description[0] for description in cursor.description]

        # Cierra el cursor
        cursor.close()

        # Crea una lista de diccionarios, donde cada diccionario representa una fila
        result_list = [row[0] for row in table_data]
        return result_list
    
    def procesar_busqueda_dash(self,query,search_filter1=None, search_filter2=None, search_filter3=None, search_filter4=None):
        # Inicializa la lista de parámetros.
        print(search_filter1)
        print(search_filter2)
        print(search_filter3)
        print(search_filter4)

        conditions = []
        params = []


        search_filter1 = tuple(item.strip() for item in ast.literal_eval(search_filter1))
        search_filter2 = tuple(item.strip() for item in ast.literal_eval(search_filter2))
        search_filter3 = tuple(item.strip() for item in ast.literal_eval(search_filter3))
        search_filter4 = tuple(item.strip() for item in ast.literal_eval(search_filter4))

        if search_filter1:
            conditions.append(f"ESP IN ({', '.join(['%s'] * len(search_filter1))})")
            params.extend(search_filter1)
        if search_filter2:
            conditions.append(f"LINEA IN ({', '.join(['%s'] * len(search_filter2))})")
            params.extend(search_filter2)
        if search_filter3:
            conditions.append(f"CLASS IN ({', '.join(['%s'] * len(search_filter3))})")
            params.extend(search_filter3)
        if search_filter4:
            conditions.append(f"ZONA IN ({', '.join(['%s'] * len(search_filter4))})")
            params.extend(search_filter4)

        query = "SELECT * FROM tekladata"

        # Añadir las condiciones a la consulta si existen
        if conditions:
            query += " WHERE " + " AND ".join(conditions) + ";"
        else:
            # Si no se proporcionan filtros, utilizar una consulta predeterminada
            query += " WHERE QTY > 0;"  # Reemplazar con tu condición predeterminada

        # Asumiendo que params solo contiene cadenas o números
        # (tener cuidado de la inyección de SQL si se incluyen entradas directamente de los usuarios)
        query_debug = query
        for p in params:
            # Asegurar que los marcadores de posición se reemplacen con cadenas debidamente entrecomilladas
            query_debug = query_debug.replace("%s", repr(str(p)), 1)  # reemplazar cada %s con su valor en params

        print("Consulta de depuración:", query_debug)
        print(query)



        print(query)
        print(query)
  
        # Conecta a la base de datos y ejecuta la consulta.
        cursor = db_connection.cursor()
        cursor.execute(query, tuple(params))
        resultados = cursor.fetchall()
        cursor.close()

        # Si no hay resultados, no habrá descripción y esto causará un error.
        if not resultados:
            return pd.DataFrame()  # Devuelve un DataFrame vacío si no hay resultados.

        column_names = [description[0] for description in cursor.description]

        df = pd.DataFrame(resultados, columns=column_names)

        print("el dataframes :",df)

        # Convertir los resultados a una lista de diccionarios.
        # search_results = [{"ID": res[0], "PIECEMARK": res[1], "ESP": res[2],"LINEA": res[3], "CLASS": res[4], "QTY": res[5],"WEIGHT": res[6], "RATIO": res[7], "ZONA": res[8],"TRASLADO": res[9], "PRE_ENSAMBLE": res[10], "MONTAJE": res[11],"TORQUE": res[12], "PUNCH": res[13]} for res in resultados]

        # print(search_results)

        return df
    
    def descargar_excel(self, query, file_name="datos_exportados.xlsx"):
        # Ejecuta la consulta y obtiene los resultados en un DataFrame
        df = self.regular_df(query)

        # Convertir el DataFrame a Excel usando un buffer en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        output.seek(0)  # Regresar al inicio del BytesIO buffer

        # Crear respuesta para descargar
        response = Response(output.getvalue(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
        return response


    

    


