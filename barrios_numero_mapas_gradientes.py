# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 01:39:56 2022

@author: haffa
"""

import pandas as pd
import winsound

estaciones_barrios = pd.read_csv('./0_relacion_estaciones_barrio.csv')
#estaciones_numeros = pd.read_csv('./1_relacion_numero_estacion.csv')
#estaciones_coordenadas = pd.read_excel('./Estaciones_barrio.xlsx')
#vecCar = pd.read_csv('./9_1_vectoresCaracteristicasClusterControl2019.csv')
datos_barrios = pd.read_csv('./3cbe5690-942a-4656-beee-6fdaeb2dfa40.csv')

def numest_to_numbarr(numest):
    return estaciones_barrios.loc[numest - 1]['Código barrio']

def avisame():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

for year in [2019,2020]:
    for tipo_viaje in ['salida', 'llegada']:
        print('Evaluando ' + str(year) + ': ' + tipo_viaje)
        movimientos = pd.read_pickle('./4_movimientos'+ str(year) +'Mas24_finales.pkl')
        print('\t Transformando la estación a barrio')
        barrios19 = movimientos['Estación '+ tipo_viaje].apply(numest_to_numbarr)
        print('\t Hecho')
        barrios19_veces = barrios19.value_counts()
        codigos_barrios = list(barrios19_veces.keys())
        veces_barrios   = barrios19_veces.values
        nombre_barrios  = [estaciones_barrios[estaciones_barrios['Código barrio'] == numest]['Barrio de la estación'].unique()[0] for numest in codigos_barrios]
        poligono_barrios = [datos_barrios[datos_barrios['nombre'] == nombre]['WKT'].unique()[0] for nombre in nombre_barrios]
        dicc = {
                'Nombre del barrio' : nombre_barrios,
                'Código barrio'     : codigos_barrios,
                'Número de ' + tipo_viaje + 's' : veces_barrios,
                'WKT'               : poligono_barrios
                }
        df = pd.DataFrame.from_dict(dicc)
        df.to_csv('barrios_numero_' + tipo_viaje +'s_'+ str(year) + '.csv', index = False)
        print('\t Datos guardados. Subproceso finalizado')
        
avisame()