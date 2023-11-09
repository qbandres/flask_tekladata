from flask import render_template, session, redirect, url_for, request,Response,flash  
from app import app,db_connection
from .consulta_sql import ConsultaMain
from .data_processing import DataFrameTransformer
from .data_graphic import BokehGraph
from io import BytesIO
import pandas as pd


def generate_graph_data():
    # Crea una instancia de Consulta SQL
    consulta_main = ConsultaMain()

    # Consultas SQL y creación de DataFrames
    dataFrame1 = consulta_main.regular_df("""
        SELECT MONTAJE, SUM(WEIGHT) AS WEIGHT 
        FROM tekladata 
        WHERE MONTAJE IS NOT NULL AND MONTAJE <> '0000-00-00' AND MONTAJE <> '' 
        GROUP BY MONTAJE 
        ORDER BY MONTAJE;
    """)
    dataFrame2 = consulta_main.regular_df("""
        SELECT DATE_FORMAT(MONTAJE, '%Y-%m') AS YearMonth, SUM(WEIGHT) AS TotalWeight 
        FROM tekladata 
        WHERE MONTAJE IS NOT NULL AND MONTAJE <> '0000-00-00' AND MONTAJE <> '' 
        GROUP BY YearMonth 
        ORDER BY YearMonth ASC;
    """)

    # Transformación de los DataFrames
    dataFrameTransformer = DataFrameTransformer()
    df1, df1_acum = dataFrameTransformer.df_xy(dataFrame1, 1000, 'MONTAJE', 'WEIGHT')
    df2, df2acum = dataFrameTransformer.df_xy(dataFrame2, 1000, 'YearMonth', 'TotalWeight')

    # Creación de gráficos con Bokeh
    bokehGraph = BokehGraph()
    script1, div1 = bokehGraph.scatter(df1, '2019-10-01', '2023-03-30', 90, 'Date', 'Ton', 'Montaje Diario Variación Scatter')
    script2, div2 = bokehGraph.linear(df1_acum, '2019-10-01', '2023-03-30', 10000, 'Date', 'Ton', 'Montaje Acumulado Variación Linear')
    script3, div3 = bokehGraph.bar_chartMes(df2, '2019-10-01', '2023-03-30', 700, 'Date', 'Ton', 'Montaje Mensual Variación bar_chart')

    return script1, div1, script2, div2, script3, div3

# Ruta para la página principal después de iniciar sesión
@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' not in session:
        return redirect(url_for('index'))

    # Generar datos para los gráficos
    script1, div1, script2, div2, script3, div3 = generate_graph_data()
    
    # Inicializar variables
    search_main_table = []  # Inicializar como lista vacía

    if request.method == 'POST':
        try:
            # Procesar búsqueda si hay una
            consulta_main = ConsultaMain()
            search_type = request.form['search_type_main']
            search_filter = request.form['search_filter_main']
            search_main_table = consulta_main.regular_fetchall(f"SELECT * FROM tekladata WHERE {search_type} LIKE %s", (f"%{search_filter}%",))
        except Exception as e:
            # Aquí se captura la excepción general y se muestra un mensaje al usuario
            # Deberías capturar excepciones más específicas según lo que pueda salir mal
            flash(f"Ocurrió un error al procesar la búsqueda: {e}", 'error')
            # Opcional: Registrar el error en un archivo de log o sistema de monitoreo
            app.logger.error(f"Error en /main: {e}")

    return render_template('main.html', script1=script1, div1=div1, script2=script2, div2=div2, script3=script3, div3=div3, search_main_table=search_main_table)

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