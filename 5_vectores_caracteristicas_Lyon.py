# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 16:35:28 2022

@author: haffa
"""

import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import winsound

#%% auxiliar functions

def avisame():
    duration = 5000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
  
def datetoweek(date):
    return date.isocalendar()[1]

#%% load the data
print('Loading data')
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'

usuarios19_20 = pd.read_pickle(directorio + '4_singleusers_numerico_finales.pkl')  ### datos de usuario recientes
estaciones_barrios = pd.read_csv(directorio + '0_relacion_estaciones_barrio.csv')

#%% select users
usuarios = list(usuarios19_20['abonado'].unique())

#%% characteristics for each year

anyos = [2019, 2020]
for anyo in anyos:
    print(str(anyo) + ' has started')
    caracteristicas = {}
    identificador = 0
    numerovueltas=0
    mayo_1 = datetime.date(anyo,5,1)
    diciembre_31 = datetime.date(anyo,12,1)
    incremento = diciembre_31 - mayo_1
    numero_dias_total = incremento.days
    
    viajes = pd.read_pickle(directorio + '4_movimientos' + str(anyo) + 'Mas24_finales.pkl')  
    viajes = viajes.rename(columns = {'Abonado':'abonado'})
    viajes_toweeks = viajes['dia alquiler'].apply(datetoweek)
    viajes['número semana'] = viajes_toweeks
    print('Starting loop of users')
    for usuario in usuarios:
        
        identificador = usuario ## esto es para seguirle la pista si falla en algún sitio
        
        #edaduser = list(usuarios19_20[usuarios19_20['abonado'] == usuario]['edad'])[0]
        caracteristicas_usuario = {}
        viajes_usuario = viajes[viajes['abonado'] == usuario]
        
        caracteristicas_usuario['abonado'] = usuario
        
        viajes_mayo_diciembre = viajes_usuario[viajes_usuario['dia alquiler'] >= datetime.date(anyo,5,1)]
        numero_viajes_total = len(viajes_mayo_diciembre)
        caracteristicas_usuario['viajes mayo-diciembre'] = numero_viajes_total ## numero total de viajes entre mayo y diciembre
        
        dias = viajes_usuario['dia alquiler']
        dias_numero  = [(dia,dia.weekday()) for dia in dias]
        
        ## media de viajes a la semana (en las semanas en que hace viajes)
        semanas_hay_viajes = list(viajes_usuario['número semana'].sort_values().unique())
        viajes_por_semana = []
        
        for numero_semana in semanas_hay_viajes:
            _ = viajes_usuario[viajes_usuario['número semana'] == numero_semana]
            viajes_por_semana.append(len(_))
        
        viajes_por_semana_media = np.array(viajes_por_semana).mean()
        caracteristicas_usuario['viajes a la semana'] = viajes_por_semana_media
        
        ## viajes cada dia de la semana (normalizado de modo que la suma da 1)
        nombres_dias_semana = ['lunes','martes','miércoles','jueves','viernes','sábado','domingo']
        
        
        for i,dia in enumerate(nombres_dias_semana):
            _ = [diita[1] for diita in dias_numero if diita[1]==i]
            caracteristicas_usuario['viajes ' + dia] = len(_)/numero_viajes_total
        
        ###################
        #cosas de los meses
        ###################
        
        ## viajes en cada mes de pandemia
        meses_confinamiento = ['mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
        
        fecha_inicio  = mayo_1
        fecha_fin     = datetime.date(anyo,5,31)
        for mes in meses_confinamiento:
            viajes_mes = viajes_usuario[(viajes_usuario['dia alquiler']>= fecha_inicio)  & (viajes_usuario['dia alquiler']< fecha_fin)]
            caracteristicas_usuario['viajes ' + mes] = len(viajes_mes)/numero_viajes_total
            fecha_inicio = fecha_inicio + relativedelta(months = 1)
            fecha_fin = fecha_fin + relativedelta(months = 1)
            
        caracteristicas[usuario] = caracteristicas_usuario
        numerovueltas+=1
        if numerovueltas%500 == 0 or numerovueltas == 1:
            print(str(anyo) + 'Lyon - Van ', numerovueltas)
        

#%% save as pickle

    caracteristicasDf = pd.DataFrame.from_dict(caracteristicas, orient = 'index')
    caracteristicasDf.to_csv(directorio + '5_vectoresCaracteristicasLyon' + str(anyo) + '.csv', index = False)

avisame()