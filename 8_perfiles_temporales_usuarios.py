# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 12:25:25 2022

@author: haffa

In this script, temporal profile of users is created
"""

import pandas as pd
import numpy as np
from scipy.special import comb
import winsound


#%% auxiliar funtions

def avisame():
    duration = 5000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    
## hour to sec transforms hh:mm:ss into sec
## mod20min transforms sec to the chunk between 0,71 it belongs
def hour_to_sec(t):
    return t.hour*3600 + t.minute*60 + t.second
def mod20min(t):
    sec = hour_to_sec(t)
    r = sec%1200
    n = int((sec-r)/1200)
    return n

## auxiliar functions for control points

def puntosControl(puntos, valort,n):
    return np.matmul(A(n,valort,puntos),puntos)

def A(n, valort, puntos):
    _ = M(n,valort,puntos)
    __ = np.matmul(_.transpose(), _)
    mt = np.linalg.inv(__)
    return np.matmul(mt,_.transpose())
    
def M(n,valort, puntos):
    return np.array( [ [bernstein_poly(n,i,valort[j]) for i in range(n+1)] for j in range(len(puntos))] )
def bernstein_poly(n,i,t):
    """
     The Bernstein polynomial of n, i as a function of t
    """
    return comb(n, i) * ( t**i ) * (1 - t)**(n-i)

#%% load the data
print('Loading data')
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
datos19 = pd.read_pickle(directorio + '4_movimientos2019Mas24_finales.pkl')
datos20 = pd.read_pickle(directorio + '4_movimientos2020Mas24_finales.pkl')

datos19 = datos19.rename(columns = {'Abonado':'abonado'})
datos20 = datos20.rename(columns = {'Abonado':'abonado'})

#%% divide a day in 20 minutes chuncks

#20 minutes are 1200sec and a day is 24h*3600 sec = 86400 sec which gives 72 chuncks
day_discretized = range(0,72)

#%% first thing is going to be to change the "hora alquiler" to the bloc of 20 min it belongs
datos19['hora alquiler'] = datos19['hora alquiler'].apply(mod20min)
datos20['hora alquiler'] = datos20['hora alquiler'].apply(mod20min)

#%% create histogram for every user
print('Creating histograms')
usuarios = list(datos20['abonado'].unique()) ## it has the same users as datos19

histogramas19 = {}
histogramas20 = {}

diccionario_duraciones19 = {}
diccionario_duraciones20 = {}

for user in usuarios:
    histi = np.zeros(72)
    histi2 = np.zeros(72)
    viajesuser19 = datos19[datos19['abonado'] == user]
    viajesuser20 = datos20[datos20['abonado'] == user]

    duraciones19 = viajesuser19['Duración trayeto'].describe()[1:]
    duraciones20 = viajesuser20['Duración trayeto'].describe()[1:]
    diccionario_duraciones19[user] = duraciones19
    diccionario_duraciones20[user] = duraciones20

    for i in range(72):
        _ = viajesuser19[viajesuser19['hora alquiler'] == i]
        __ = viajesuser20[viajesuser20['hora alquiler'] == i]
        histi[i] = len(_)
        histi2[i] = len(__)
    histogramas19[user] = histi
    histogramas20[user] = histi2
    

#%% dictionary of durations as dataframe
diccionario_duraciones19Df = pd.DataFrame.from_dict(diccionario_duraciones19, orient = 'columns')
diccionario_duraciones19Df = diccionario_duraciones19Df.T
diccionario_duraciones19Df = diccionario_duraciones19Df.rename(columns = {llave : llave + ' duración' for llave in diccionario_duraciones19Df.keys()})

diccionario_duraciones20Df = pd.DataFrame.from_dict(diccionario_duraciones20, orient = 'columns')
diccionario_duraciones20Df = diccionario_duraciones20Df.T
diccionario_duraciones20Df = diccionario_duraciones20Df.rename(columns = {llave : llave + ' duración' for llave in diccionario_duraciones20Df.keys()})

#%% histograms as dataframes
histogramas19df = pd.DataFrame.from_dict(histogramas19, orient = 'columns')
histogramas20df = pd.DataFrame.from_dict(histogramas20, orient = 'columns')
#%% save them for the future
histogramas19df.to_csv(directorio + '8_histogramas2019.csv')
histogramas20df.to_csv(directorio + '8_histogramas2020.csv')

print('Histogams created and saved\n Starting control points evaluation')
#%% creating control points for the histograms

diccionarioControl19 = {}
diccionarioControl20 = {}
for user in usuarios:
    puntos = np.array([range(72),histogramas19[user]]).transpose()
    pC = puntosControl(puntos, np.linspace(0,1,72),7)
    diccionarioControl19[user] = [item for sublist in pC for item in sublist]
    
    puntos = np.array([range(72),histogramas20[user]]).transpose()
    pC = puntosControl(puntos, np.linspace(0,1,72),7)
    diccionarioControl20[user] = [item for sublist in pC for item in sublist]

#%% we save them as csv

usuariosControl19 = pd.DataFrame.from_dict(diccionarioControl19, orient = 'index', columns = ['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8'])
usuariosControl20 = pd.DataFrame.from_dict(diccionarioControl20, orient = 'index', columns = ['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8'])

usuariosControl19 = pd.concat([usuariosControl19,diccionario_duraciones19Df], axis = 1)
usuariosControl20 = pd.concat([usuariosControl20,diccionario_duraciones20Df], axis = 1)

columnas_a_borrar = ['X' + str(i) for i in range(1,9)]
usuariosControl19 = usuariosControl19.drop(columns = columnas_a_borrar)
usuariosControl20 = usuariosControl20.drop(columns = columnas_a_borrar)

usuariosControl20.to_csv(directorio + '8_usuariosControl2020.csv')
usuariosControl19.to_csv(directorio + '8_usuariosControl2019.csv')
print('Control points evaluated and saved\n Normalized histograms and its control points start evaluating')
#%% histogramas normalized

histogramas19 = {user : (1/max(histogramas19[user]))*np.array(histogramas19[user]) for user in usuarios}
histogramas20 = {user : (1/max(histogramas20[user]))*np.array(histogramas20[user]) for user in usuarios}

#%% histograms normalized as dataframes
histogramas19df = pd.DataFrame.from_dict(histogramas19, orient = 'columns')
histogramas20df = pd.DataFrame.from_dict(histogramas20, orient = 'columns')
#%% save normalized histograms  for the future
histogramas19df.to_csv(directorio + '8_histogramas_normalizados2019.csv')
histogramas20df.to_csv(directorio + '8_histogramas_normalizados2020.csv')

#%% creating control points for the histograms normalized

diccionarioControl19 = {}
diccionarioControl20 = {}
for user in usuarios:
    puntos = np.array([range(72),histogramas19[user]]).transpose()
    pC = puntosControl(puntos, np.linspace(0,1,72),7)
    diccionarioControl19[user] = [item for sublist in pC for item in sublist]
    
    puntos = np.array([range(72),histogramas20[user]]).transpose()
    pC = puntosControl(puntos, np.linspace(0,1,72),7)
    diccionarioControl20[user] = [item for sublist in pC for item in sublist]

#%% we save them as csv

usuariosControl19 = pd.DataFrame.from_dict(diccionarioControl19, orient = 'index', columns = ['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8'])
usuariosControl20 = pd.DataFrame.from_dict(diccionarioControl20, orient = 'index', columns = ['X1', 'Y1', 'X2', 'Y2', 'X3', 'Y3', 'X4', 'Y4', 'X5', 'Y5', 'X6', 'Y6', 'X7', 'Y7', 'X8', 'Y8'])

usuariosControl19 = pd.concat([usuariosControl19,diccionario_duraciones19Df], axis = 1)
usuariosControl20 = pd.concat([usuariosControl20,diccionario_duraciones20Df], axis = 1)

columnas_a_borrar = ['X' + str(i) for i in range(1,9)]
usuariosControl19 = usuariosControl19.drop(columns = columnas_a_borrar)
usuariosControl20 = usuariosControl20.drop(columns = columnas_a_borrar)

usuariosControl20.to_csv(directorio + '8_usuariosControl_normalizados2020.csv')
usuariosControl19.to_csv(directorio + '8_usuariosControl_normalizados2019.csv')
print('Normalized control points evaluated and saved\n Start the statistical data ')


#%% now an statistical version is created

diccionarioEstadisticas19 = {}
diccionarioEstadisticas20 = {}
columnas = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
for us in usuarios:
    horas = datos19[datos19['abonado'] == us]['hora alquiler']
    _ = horas.describe()
    diccionarioEstadisticas19[us] = [_[columna] for columna in columnas]
    
    horas = datos20[datos20['abonado'] == us]['hora alquiler']
    _ = horas.describe()
    diccionarioEstadisticas20[us] = [_[columna] for columna in columnas]
    
usuariosEstadisticas19 = pd.DataFrame.from_dict( diccionarioEstadisticas19, orient = 'index', columns = columnas)
usuariosEstadisticas20 = pd.DataFrame.from_dict( diccionarioEstadisticas20, orient = 'index', columns = columnas)

usuariosEstadisticas19 = pd.concat([usuariosEstadisticas19,diccionario_duraciones19Df], axis = 1)
usuariosEstadisticas20 = pd.concat([usuariosEstadisticas20,diccionario_duraciones20Df], axis = 1)

usuariosEstadisticas19 = usuariosEstadisticas19.drop(columns = ['count'])
usuariosEstadisticas20 = usuariosEstadisticas20.drop(columns = ['count'])

#%% now we save it as pkl

usuariosEstadisticas19.to_csv(directorio + '8_usuariosEstadisticas2019.csv')
usuariosEstadisticas20.to_csv(directorio + '8_usuariosEstadisticas2020.csv')
print('Statistical data saved and evaluated')

#%% tell me you've finished

avisame()
