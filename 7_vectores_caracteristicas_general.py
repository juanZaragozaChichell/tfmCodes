# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 20:36:56 2022

@author: haffa
"""

import pandas as pd
import winsound

def avisame():
    duration = 5000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

#%% load the data
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
usuarios19_20 = pd.read_pickle(directorio + '4_singleusers_numerico_finales.pkl')  ### datos de usuario recientes
estaciones_barrios = pd.read_csv(directorio + '0_relacion_estaciones_barrio.csv')
usuarios = list(usuarios19_20['abonado'].unique())
#%% select only users that appear in both sides

for anyo in [2019, 2020]:
    print('loading data for '+ str(anyo))
    viajes = pd.read_pickle(directorio + '4_movimientos' + str(anyo) + 'Mas24_finales.pkl')  
    viajes = viajes.rename(columns = {'Abonado':'abonado'})
    caracteristicas_previas = pd.read_csv(directorio + '6_vectoresCaracteristicasLyonYSocial' + str(anyo) + '.csv')
    caracteristicas = {}
    identificador = 0
    numerovueltas=0
    print('Users loop begins')
    for usuario in usuarios:
        
        identificador = usuario ## esto es para seguirle la pista si falla en algún sitio
        caracteristicas_usuario = caracteristicas_previas[caracteristicas_previas['abonado'] == usuario]
        caracteristicas_usuario = caracteristicas_usuario.to_dict(orient='records')
        caracteristicas_usuario = caracteristicas_usuario[0]
        viajes_usuario = viajes[viajes['abonado'] == usuario]
        
        ## las estaciones
        ## las dos estaciones de salida principales
        estaciones = viajes_usuario['Estación salida']
        estacionS1 = estaciones.idxmax()
        estacionS1val = estaciones[estacionS1]
        barrioS1 = estaciones_barrios.iloc[estacionS1val-1]['Código barrio']
        estaciones = estaciones.drop(labels = [estacionS1])
        estacionS2 = estaciones.idxmax()
        estacionS2val = estaciones[estacionS2]
        barrioS2 = estaciones_barrios.iloc[estacionS2val-1]['Código barrio']
        caracteristicas_usuario['barrio estación más salidas 1'] = barrioS1
        caracteristicas_usuario['barrio estación más salidas 2'] = barrioS2
        
        ## las dos estaciones de llegada principales
        estaciones = viajes_usuario['Estación llegada']
        estacionS1 = estaciones.idxmax()
        estacionS1val = estaciones[estacionS1]
        barrioS1 = estaciones_barrios.iloc[estacionS1val-1]['Código barrio']
        estaciones = estaciones.drop(labels = [estacionS1])
        estacionS2 = estaciones.idxmax()
        estacionS2val = estaciones[estacionS2]
        barrioS2 = estaciones_barrios.iloc[estacionS2val-1]['Código barrio']
        caracteristicas_usuario['barrio estación más llegadas 1'] = barrioS1
        caracteristicas_usuario['barrio estación más llegadas 2'] = barrioS2
            
        caracteristicas[usuario] = caracteristicas_usuario
        numerovueltas+=1
        if numerovueltas%500 == 0 or numerovueltas == 1:
            print(str(anyo) + 'generales - Van ', numerovueltas)
        
    
    #%%save as pickle
    
    caracteristicasDf = pd.DataFrame.from_dict(caracteristicas, orient = 'index')
    caracteristicasDf.to_csv(directorio + '7_vectoresCaracteristicasGenerales' + str(anyo) +'.csv', index = False)
    
avisame()