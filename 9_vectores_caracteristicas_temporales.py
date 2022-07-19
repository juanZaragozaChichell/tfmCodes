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

usuarios = list(usuarios19_20['abonado'].unique())
#%% select only users that appear in both sides

for anyo in [2019, 2020]:
    print('loading data for '+ str(anyo))
    caracteristicas_previas = pd.read_csv(directorio + '7_vectoresCaracteristicasGenerales' + str(anyo) +'.csv')
    puntos_control = pd.read_csv(directorio + '8_usuariosControl_normalizados'+str(anyo)+'.csv')
    datos_estadisticos = pd.read_csv(directorio + '8_usuariosEstadisticas' + str(anyo) + '.csv')
    caracteristicas_control = {}
    caracteristicas_estadisticas = {}
    identificador = 0
    numerovueltas=0
    print('Users loop begins')
    for usuario in usuarios:
        
        identificador = usuario ## esto es para seguirle la pista si falla en algún sitio
        caracteristicas_usuario = caracteristicas_previas[caracteristicas_previas['abonado'] == usuario]
        caracteristicas_usuario = caracteristicas_usuario.to_dict(orient='records')
        caracteristicas_usuario = caracteristicas_usuario[0]
        
        caracteristicas_control_usuario = caracteristicas_usuario.copy()
        caracteristicas_estadisticas_usuario = caracteristicas_usuario.copy()
        
        puntos_control_usuario = puntos_control[puntos_control['Unnamed: 0'] == usuario]
        puntos_control_usuario = puntos_control_usuario.drop(columns = ['Unnamed: 0'])
        puntos_control_usuario = puntos_control_usuario.to_dict(orient='records')
        puntos_control_usuario = puntos_control_usuario[0]
        
        datos_est = datos_estadisticos[datos_estadisticos['Unnamed: 0'] == usuario]
        datos_est = datos_est.drop(columns = ['Unnamed: 0'])
        datos_est = datos_est.to_dict(orient='records')
        datos_est = datos_est[0]
        
        
        for name in puntos_control_usuario.keys():
            caracteristicas_control_usuario[name] = puntos_control_usuario[name]
        
        
        for name in datos_est.keys():
            caracteristicas_estadisticas_usuario[name] = datos_est[name]
        
        
        
        
        
        
        caracteristicas_control[usuario]      = caracteristicas_control_usuario
        caracteristicas_estadisticas[usuario] = caracteristicas_estadisticas_usuario
        numerovueltas+=1
        if numerovueltas%500 == 0 or numerovueltas == 1:
            print(str(anyo) + ' Van ', numerovueltas)
        
    
    #%%save as pickle
    
    caracteristicasDf = pd.DataFrame.from_dict(caracteristicas_control, orient = 'index')
    caracteristicasDf.to_csv(directorio + '9_1_vectoresCaracteristicasControl' + str(anyo) +'.csv', index = False)
    
    caracteristicasDf = pd.DataFrame.from_dict(caracteristicas_estadisticas, orient = 'index')
    caracteristicasDf.to_csv(directorio + '9_2_vectoresCaracteristicasEstadisticas' + str(anyo) +'.csv', index = False)
    
avisame()