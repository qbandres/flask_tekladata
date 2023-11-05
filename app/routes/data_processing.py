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
    
    # ... (añade más funciones según lo necesites)