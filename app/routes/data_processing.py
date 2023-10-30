import pandas as pd

class DataFrameTransformer:
    def __init__(self):
        pass

    def df_xy(self,df,factor,name_x,name_y): # el factor es si deseas dividir la columna Y 

        # Suponiendo que df es tu DataFrame
        df = df[[name_x, name_y]]
        df.columns = ['x', 'y']

        # Reemplazar '' con NaN para manejarlos de manera uniforme
        df.replace('', pd.NA, inplace=True)
        df = df.dropna(subset=['y'])
        

        df['y'] = df.y/factor

        #Calculos para el df-acum
        df_acum = df.copy()
        # Agregando la columna 'z' con la suma acumulada de 'y'
        df_acum['z'] = df_acum['y'].cumsum()
        del df_acum['y']
        df_acum.columns = ['x', 'y']

        return df,df_acum

    def some_calculation_2(self):
        # Realizar cálculos y retornar resultados
        pass
    # ... (añade más funciones según lo necesites)