from flask import render_template,request
from app import app
from .consulta_sql import ConsultaMain
from .data_processing import DataFrameTransformer
from .data_graphic import BokehGraph
from io import BytesIO
from datetime import datetime
from .data_graphic import BokehGraph


@app.route('/get-select-data', methods=['GET', 'POST'])
def get_select_data():
    # Aquí debes realizar la consulta a tu base de datos
    # Por ejemplo, obtener una lista de todas las zonas únicas
    
    consulta_sql = ConsultaMain()
    bokehGraph = BokehGraph()
    
    esp_s = consulta_sql.regular_list('SELECT DISTINCT ESP FROM tekladata;')
    linea_s = consulta_sql.regular_list('SELECT DISTINCT LINEA FROM tekladata;')
    class_s = consulta_sql.regular_list('SELECT DISTINCT CLASS FROM tekladata;')
    zona_s = consulta_sql.regular_list('SELECT DISTINCT ZONA FROM tekladata;')

    # GRAFICAR GRAFICO1 SEGUN DATOS POR DAFOULT

    df_acum = consulta_sql.regular_df('SELECT * FROM tekladata')

    transform = DataFrameTransformer()
    brutoDiario,brutoAcum = transform.df_xy(df_acum,1000,'MONTAJE','WEIGHT')

    scriptBrut, divBrut = bokehGraph.linear(brutoAcum, '2019-10-01', '2023-03-30', 10000, 'Date', 'Ton', 'Montaje Acumulado Variación Linear')
    
    # Asegúrate de que todas las variables que usas en tu plantilla estén definidas

    print('paso por selct')
    print(esp_s)
    print(linea_s)
    print(class_s)
    print(zona_s)

    return render_template(
        'dashboardFilter.html',
        esp_s=esp_s,
        linea_s=linea_s,
        class_s=class_s,
        zona_s=zona_s,scriptBrut=scriptBrut,divBrut=divBrut)


@app.route('/graphic_dash', methods=['GET', 'POST'])
def graphic_dash():

    consulta_sql = ConsultaMain()
    bokehGraph = BokehGraph()
   
    if request.method == 'POST':

        # El procesamiento del método POST actualiza tupla_esp, tupla_linea, tupla_class y tupla_zona
        esps_seleccionados = request.form.getlist('esp')
        lineas_seleccionadas = request.form.getlist('linea')
        clases_seleccionadas = request.form.getlist('class')
        zonas_seleccionadas = request.form.getlist('zona')

        dataFrameTransformer = DataFrameTransformer()

        tupla_esp = dataFrameTransformer.list_tuple(esps_seleccionados)
        tupla_linea = dataFrameTransformer.list_tuple(lineas_seleccionadas)
        tupla_class = dataFrameTransformer.list_tuple(clases_seleccionadas)
        tupla_zona = dataFrameTransformer.list_tuple(zonas_seleccionadas)

        # AQUI DEBEMOS ACTUALIZAR LOS CAMP[OR DE ESP,LINA CLASS Y ZONA PARA QUE SE ACTUALICE EL GRAFICO1
        print('paso por dash')
        print(tupla_esp)
        print(tupla_linea)
        print(tupla_class)
        print(tupla_zona)

        # GRAFICAR GRAFICO1 SEGUN DATOS POR DAFOULT
        df_acum = consulta_sql.procesar_busqueda_dash('SELECT * FROM tekladata',tupla_esp,tupla_linea,tupla_class,tupla_zona)

        print('df_acumualdo',df_acum)

        esp_s = consulta_sql.regular_list('SELECT DISTINCT ESP FROM tekladata;')
        linea_s = consulta_sql.regular_list('SELECT DISTINCT LINEA FROM tekladata;')
        class_s = consulta_sql.regular_list('SELECT DISTINCT CLASS FROM tekladata;')
        zona_s = consulta_sql.regular_list('SELECT DISTINCT ZONA FROM tekladata;')

        transform = DataFrameTransformer()
        brutoDiario,brutoAcum = transform.df_xy(df_acum,1000,'MONTAJE','WEIGHT')

        scriptBrut, divBrut = bokehGraph.linear(brutoAcum, '2019-10-01', '2023-03-30', 10000, 'Date', 'Ton', 'Montaje Acumulado Variación Linear')
    


    # Asegúrate de que todas las variables que usas en tu plantilla estén definidas
    return render_template(
        'dashboardFilter.html',
        tupla_esp=tupla_esp,
        tupla_linea=tupla_linea,
        tupla_class=tupla_class,
        tupla_zona=tupla_zona,
        scriptBrut=scriptBrut,
        divBrut=divBrut,esp_s=esp_s,linea_s=linea_s,class_s=class_s,zona_s=zona_s
    )