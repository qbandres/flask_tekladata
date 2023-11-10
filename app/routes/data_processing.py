import pandas as pd

class DataFrameTransformer:
    def __init__(self):
        pass

    def df_xy(self,df,factor,name_x,name_y): # el factor es si deseas dividir la columna Y 

        # Suponiendo que df es tu DataFrame
        df = df[[name_x, name_y]].copy()
        df.columns = ['x', 'y']

        # Reemplazar '' con NaN para manejarlos de manera uniforme
        df.replace('', pd.NA, inplace=True)
        df = df.dropna()
        df['y'] = df.y/factor

        df = df.groupby('x')['y'].sum().reset_index()
        print(df)

        #Calculos para el df-acum
        df_acum = df.copy()
        # Agregando la columna 'z' con la suma acumulada de 'y'
        df_acum['z'] = df_acum['y'].cumsum()
        del df_acum['y']
        df_acum.columns = ['x', 'y']

        return df,df_acum

    def group_x(self,df,columnGroup,columnSum):
        df_agrupado = df.groupby(columnGroup)[columnSum].sum().reset_index()
        return df_agrupado
    

    def list_tuple(self,listado):
        if len(listado) == 1:
            tupla = f"('{listado[0]}',)"
        else:
            tupla = str(tuple(listado))
        return tupla
    
    def max_min (self,data):

        data['x'] = pd.to_datetime(data['x'])
        # Suponiendo que data es tu DataFrame y que contiene una columna 'x' de fechas
        x_start = pd.to_datetime(data['x'].min())  # Fecha inicial
        x_end = pd.to_datetime(data['x'].max())    # Fecha final

        # Calcular la diferencia en días
        date_range = x_end - x_start

        # Calcular 5% de ese rango
        ten_percent = date_range * 0.05

        # Extender el rango en un 10%
        x_start = x_start - ten_percent
        x_end = x_end + ten_percent

        y_start = 0                # Límite inferior de y
        y_end = float(data['y'].max())*1.1    # Límite superior de y (valor máximo)

        return x_start,x_end, y_start, y_end
        
    
    # ... (añade más funciones según lo necesites)