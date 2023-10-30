from flask import render_template, session, redirect, url_for, request
from app import app
from .consulta_sql import ConsultaMain
from .data_processing import DataFrameTransformer
from .data_graphic import BokehGraph

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
            # print(f"Ocurrió un error: {e}")
            search_main_table = []  # Asigna una lista vacía en caso de error

    return render_template('main.html', script1=script1, div1=div1, script2=script2, div2=div2, script3=script3, div3=div3, search_main_table=search_main_table)


# No necesitas una ruta separada para /procesar_busqueda ya que /main maneja ambos GET y POST
