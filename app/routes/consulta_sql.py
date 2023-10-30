from app import app, db_connection, usuarios
import pandas as pd


class ConsultaMain:
    def __init__(self):
        pass
    def regular_fetchall(self,query): #Se ingresara como variabel el query
        # Consulta a la base de datos para obtener datos de la tabla "tekladata"
        cursor = db_connection.cursor()
        cursor.execute(query)
        table_data = cursor.fetchall()
        cursor.close()
        return table_data

    def regular_df(self,query1):
        # Consulta a la base de datos para obtener datos de la tabla "tekladata"
        cursor = db_connection.cursor()
        cursor.execute(query1)
        table_data1 = cursor.fetchall()
        
        # Obtener dinámicamente los nombres de las columnas
        column_names = [description[0] for description in cursor.description]
        cursor.close()

        # Crear el DataFrame
        df = pd.DataFrame(table_data1, columns=column_names)
        return df
    # ... (añade más funciones según lo necesites)

