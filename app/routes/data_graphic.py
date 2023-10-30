
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool,ColumnDataSource,NumeralTickFormatter,Range1d
from bokeh.models.formatters import DatetimeTickFormatter
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class BokehGraph:
    def __init__(self):
        pass

    #Solo deb recibir 2 columnas x | y y con los titulos X | Y el x tiene que ser fecha
    def linear(self,data,fi,ff,ymax,name_x,name_y,title):
            
        # Asegurarse de que 'Montaje' sea de tipo datetime
        data['x'] = pd.to_datetime(data['x'])

        # Convertir el DataFrame a ColumnDataSource para Bokeh
        source = ColumnDataSource(data)

        # Define los rangos para cada eje
        x_start = pd.to_datetime(fi)
        x_end = pd.to_datetime(ff)
        y_start = 0
        y_end = ymax

        # Crear un gráfico con la fecha en el eje x y el peso en el eje y
        p = figure(title=title, 
                x_axis_label=name_x, 
                y_axis_label=name_y,
                x_axis_type='datetime',
            x_range=Range1d(x_start, x_end),
            y_range=Range1d(y_start, y_end),sizing_mode="stretch_both")
        
        # Añadir una línea
        p.line(x='x',y='y', source=source, line_width=2)

        # Formato para el eje x (fechas)
        # p.xaxis.formatter = DatetimeTickFormatter(days=["%Y-%m-%d"], months=["%Y-%m-%d"], years=["%Y-%m-%d"])

        # Formato para el eje y (peso) para evitar la notación científica
        p.yaxis.formatter = NumeralTickFormatter(format="0,0")
        # Alinear el título a la izquierda
        p.title.align = "right"


        # Añadir una herramienta de hover para mostrar información detallada
        hover = HoverTool()
        hover.tooltips = [
            ('Fecha de Montaje', "@x{%F}"),
            ('Peso','@y{0,0}')
        ]
        hover.formatters = {'@x': 'datetime'}
        p.add_tools(hover)

        # Devolver el script y el div
        script, div = components(p)
        return script, div

    def scatter(self, data, fi, ff, ymax, name_x, name_y, title):
        
        # Asegurarse de que 'x' sea de tipo datetime
        data['x'] = pd.to_datetime(data['x'])

        # Convertir el DataFrame a ColumnDataSource para Bokeh
        source = ColumnDataSource(data)

        # Define los rangos para cada eje
        x_start = pd.to_datetime(fi)
        x_end = pd.to_datetime(ff)
        y_start = 0
        y_end = ymax

        # Crear un gráfico con la fecha en el eje x y el peso en el eje y
        p = figure(title=title, 
                x_axis_label=name_x, 
                y_axis_label=name_y,
                x_axis_type='datetime',
            x_range=Range1d(x_start, x_end),
            y_range=Range1d(y_start, y_end),sizing_mode="stretch_both")
        
        # Añadir puntos para el gráfico de dispersión
        p.scatter(x='x', y='y', source=source, size=8, color="navy", alpha=0.5)

        # Formato para el eje y (peso) para evitar la notación científica
        p.yaxis.formatter = NumeralTickFormatter(format="0,0")
        # Alinear el título a la izquierda
        p.title.align = "right"


        # Añadir una herramienta de hover para mostrar información detallada
        hover = HoverTool()
        hover.tooltips = [
            ('Fecha de Montaje', "@x{%F}"),
            ('Peso', '@y')
        ]
        hover.formatters = {'@x': 'datetime'}
        p.add_tools(hover)

        # Devolver el script y el div
        script, div = components(p)
        return script, div
    
    def bar_chartMes(self, data, fi, ff, ymax, name_x, name_y, title):
        
        # Convertir 'x' a datetime y luego a formato año-mes
        data['x'] = pd.to_datetime(data['x']).dt.to_period('M').dt.to_timestamp()

        # Agrupar por mes y sumar/agregar los valores de 'y'
        data = data.groupby('x').agg({'y': 'sum'}).reset_index()

        # Convertir el DataFrame a ColumnDataSource para Bokeh
        source = ColumnDataSource(data)

        # Define los rangos para cada eje
        x_start = pd.to_datetime(fi)
        x_end = pd.to_datetime(ff)
        y_start = 0
        y_end = ymax

        # Crear un gráfico...
        p = figure(title=title, 
                x_axis_label=name_x, 
                y_axis_label=name_y,
                x_axis_type='datetime',
                x_range=Range1d(x_start, x_end),
                y_range=Range1d(y_start, y_end),
                sizing_mode="stretch_both")
        
        # Alinear el título a la izquierda
        p.title.align = "right"
        
        # Ajustar el ancho de la barra para un mes aproximado
        bar_width = 30 * 24 * 60 * 60 * 1000  # ancho en milisegundos para un mes aproximado
        p.vbar(x='x', top='y', width=bar_width, source=source, color="navy", alpha=0.5)

        # Añadir una herramienta de hover para mostrar información detallada
        hover = HoverTool()
        hover.tooltips = [
            ('Fecha de Montaje', "@x{%F}"),
            ('Peso', '@y')
        ]
        hover.formatters = {'@x': 'datetime'}
        p.add_tools(hover)

        
        # Devolver el script y el div
        script, div = components(p)
        return script, div
    
    def bar_chartDia(self, data, fi, ff, ymax, name_x, name_y, title):
        
        # Convertir el DataFrame a ColumnDataSource para Bokeh
        source = ColumnDataSource(data)

        # Define los rangos para cada eje
        x_start = pd.to_datetime(fi)
        x_end = pd.to_datetime(ff)
        y_start = 0
        y_end = ymax

        # Crear un gráfico...
        p = figure(title=title, 
                x_axis_label=name_x, 
                y_axis_label=name_y,
                x_axis_type='datetime',
                x_range=Range1d(x_start, x_end),
                y_range=Range1d(y_start, y_end),
                sizing_mode="stretch_both")
        
        # Alinear el título a la izquierda
        p.title.align = "right"
        
        # Ajustar el ancho de la barra para un mes aproximado
        bar_width = 24 * 60 * 60 * 1000  # ancho en milisegundos para un mes aproximado
        p.vbar(x='x', top='y', width=bar_width, source=source, color="navy", alpha=0.5)

        # Añadir una herramienta de hover para mostrar información detallada
        hover = HoverTool()
        hover.tooltips = [
            ('Fecha de Montaje', "@x{%F}"),
            ('Peso', '@y')
        ]
        hover.formatters = {'@x': 'datetime'}
        p.add_tools(hover)

        
        # Devolver el script y el div
        script, div = components(p)
        return script, div

