from flask import render_template, session,redirect,url_for
from app import app
from .consulta_sql import ConsultaMain
from .data_processing import DataFrameTransformer
from .data_graphic import BokehGraph

# Ruta para la página principal después de iniciar sesión
@app.route('/main')
def main():
    if 'username' in session:
        #Vamos a crear el grafico
        # Primero Crear una instancia de Consulta SQL
        consulta_main = ConsultaMain()
        dataFrame1 = consulta_main.regular_df("""     SELECT MONTAJE, SUM(WEIGHT) AS WEIGHT 
                                                    FROM tekladata 
                                                    WHERE MONTAJE IS NOT NULL AND MONTAJE <> '0000-00-00' AND MONTAJE <> '' 
                                                    GROUP BY MONTAJE 
                                                    ORDER BY MONTAJE;""")
        dataFrame2 = consulta_main.regular_df("""   SELECT DATE_FORMAT(MONTAJE, '%Y-%m') AS YearMonth, SUM(WEIGHT) AS TotalWeight 
                                                    FROM tekladata 
                                                    WHERE MONTAJE IS NOT NULL AND MONTAJE <> '0000-00-00' AND MONTAJE <> '' 
                                                    GROUP BY YearMonth 
                                                    ORDER BY YearMonth ASC; """)

        #Convertimos los df en df de x y incluyendo el acumulado
        dataFrameTransformer = DataFrameTransformer()
        df1,df1_acum = dataFrameTransformer.df_xy(dataFrame1,1000,'MONTAJE','WEIGHT')   
        df2,df2acum = dataFrameTransformer.df_xy(dataFrame2,1000,'YearMonth','TotalWeight')


        #Convertimos esto df en script y div para exportar
        bokehGraph = BokehGraph()

        script1,div1 = bokehGraph.scatter(df1,'2019-10-01','2023-03-30',90,'Date','Ton','Montaje Diario Variación Scatter')
        script2,div2 = bokehGraph.linear(df1_acum,'2019-10-01','2023-03-30',10000,'Date','Ton','Montaje Acumualdo Variación Linear')
        script3,div3 = bokehGraph.bar_chart(df2,'2019-10-01','2023-03-30',700,'Date','Ton','Montaje Mensual Variación bar_chart')

        print(script1,div1)

        print(df1)
        print(df1_acum)
        print(df2)

        return render_template('main.html', script1=script1,div1=div1,script2=script2,div2=div2,script3=script3,div3=div3)
    else:
        # Redirigir a la página de inicio si no se ha iniciado sesión
        return redirect(url_for('index'))
