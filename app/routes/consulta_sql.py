from app import app, db_connection, usuarios
import pandas as pd


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


