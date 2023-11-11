from flask import render_template, session, redirect, url_for, request,flash  
from app import app,db_connection
from .consulta_sql import ConsultaMain
from .data_processing import DataFrameTransformer
from .data_graphic import BokehGraph


def generate_graph_data():
    # Crea una instancia de Consulta SQL
    consulta_main = ConsultaMain()

    # Consultas SQL y creación de DF
    dataFrame1 = consulta_main.regular_df("""
        SELECT MONTAJE, SUM(WEIGHT) AS WEIGHT 
        FROM est_tekladata 
        WHERE MONTAJE IS NOT NULL AND MONTAJE <> '0000-00-00' AND MONTAJE <> '' 
        GROUP BY MONTAJE 
        ORDER BY MONTAJE;
    """)
    dataFrame2 = consulta_main.regular_df("""
        SELECT DATE_FORMAT(MONTAJE, '%Y-%m') AS YearMonth, SUM(WEIGHT) AS TotalWeight 
        FROM est_tekladata 
        WHERE MONTAJE IS NOT NULL AND MONTAJE <> '0000-00-00' AND MONTAJE <> '' 
        GROUP BY YearMonth 
        ORDER BY YearMonth ASC;
    """)

    # Transformación de los DF
    dataFrameTransformer = DataFrameTransformer()
    df1, df1_acum = dataFrameTransformer.df_xy(dataFrame1, 1000, 'MONTAJE', 'WEIGHT')
    df2, df2acum = dataFrameTransformer.df_xy(dataFrame2, 1000, 'YearMonth', 'TotalWeight')

    # Creación de gráficos con Bokeh
    bokehGraph = BokehGraph()
    script1, div1 = bokehGraph.scatter(df1,'Date', 'Ton', 'Montaje Diario Variación Scatter')
    script2, div2 = bokehGraph.linear(df1_acum,'Date', 'Ton', 'Montaje Acumulado Variación Linear')
    script3, div3 = bokehGraph.bar_chartMes(df2,'Date', 'Ton', 'Montaje Mensual Variación bar_chart')

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
            search_main_table = consulta_main.regular_fetchall(f"SELECT * FROM est_tekladata WHERE {search_type} LIKE %s", (f"%{search_filter}%",))
        except Exception as e:
            # Aquí se captura la excepción general y se muestra un mensaje al usuario
            # Deberías capturar excepciones más específicas según lo que pueda salir mal
            flash(f"Ocurrió un error al procesar la búsqueda: {e}", 'error')
            # Opcional: Registrar el error en un archivo de log o sistema de monitoreo
            app.logger.error(f"Error en /main: {e}")

    return render_template('main.html', script1=script1, div1=div1, script2=script2, div2=div2, script3=script3, div3=div3, search_main_table=search_main_table)

@app.route('/download_excel')
def download_excel():
    consulta = ConsultaMain()
    return consulta.descargar_excel("SELECT * FROM est_tekladata", "datos_est_tekladata.xlsx")
