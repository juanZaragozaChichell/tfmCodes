# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 19:12:43 2022

@author: haffa
"""


import pandas as pd
import datetime
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
    caracteristicas_previas = pd.read_csv(directorio + '5_vectoresCaracteristicasLyon' + str(anyo) + '.csv')
    caracteristicas = {}
    identificador = 0
    numerovueltas=0
    print('Users loop begins')
    for usuario in usuarios:
        
        identificador = usuario ## esto es para seguirle la pista si falla en algún sitio
        
        edaduser = list(usuarios19_20[usuarios19_20['abonado'] == usuario]['edad'])[0]
        caracteristicas_usuario = caracteristicas_previas[caracteristicas_previas['abonado'] == usuario]
        caracteristicas_usuario = caracteristicas_usuario.to_dict(orient='records')
        caracteristicas_usuario = caracteristicas_usuario[0]
        viajes_usuario = viajes[viajes['abonado'] == usuario]
        
        ############################################
        # caracteristicas sociales para los dos años
        ############################################
        
        caracteristicasSociales = usuarios19_20[usuarios19_20['abonado'] == usuario]
        
        caracteristicas_usuario['codigo postal'] = caracteristicasSociales['código postal'].values[0]
        caracteristicas_usuario['sexo'] = list(caracteristicasSociales['sexo'])[0]
        caracteristicas_usuario['edad'] = list(caracteristicasSociales['edad'])[0]
        caracteristicas_usuario['idioma'] = list(caracteristicasSociales['idioma'])[0]
        
        
        viajes_mayo_diciembre = viajes_usuario[viajes_usuario['dia alquiler'] >= datetime.date(anyo,5,1)]
       
        ## viajes en cada mes de pandemia
        viajesmayo       = viajes_usuario[(viajes_usuario['dia alquiler']>= datetime.date(anyo,5,1))  & (viajes_usuario['dia alquiler']< datetime.date(anyo,6,1))]
        viajesjunio      = viajes_usuario[(viajes_usuario['dia alquiler']>= datetime.date(anyo,6,1))  & (viajes_usuario['dia alquiler']< datetime.date(anyo,7,1))]
        viajesjulio      = viajes_usuario[(viajes_usuario['dia alquiler']>= datetime.date(anyo,7,1))  & (viajes_usuario['dia alquiler']< datetime.date(anyo,8,1))]
        viajesagosto     = viajes_usuario[(viajes_usuario['dia alquiler']>= datetime.date(anyo,8,1))  & (viajes_usuario['dia alquiler']< datetime.date(anyo,9,1))]
        viajesseptiembre = viajes_usuario[(viajes_usuario['dia alquiler']>= datetime.date(anyo,9,1))  & (viajes_usuario['dia alquiler']< datetime.date(anyo,10,1))]
        viajesoctubre    = viajes_usuario[(viajes_usuario['dia alquiler']>= datetime.date(anyo,10,1)) & (viajes_usuario['dia alquiler']< datetime.date(anyo,11,1))]
        viajesnoviembre  = viajes_usuario[(viajes_usuario['dia alquiler']>= datetime.date(anyo,11,1)) & (viajes_usuario['dia alquiler']< datetime.date(anyo,12,1))]
        viajesdiciembre  = viajes_usuario[ viajes_usuario['dia alquiler']>= datetime.date(anyo,12,1)]
        
        
        viajes_prohibidos_mayo = viajesmayo[
           ((viajesmayo['hora alquiler'] <= datetime.time(6,0,0)) |
           ((viajesmayo['hora alquiler'] >= datetime.time(10,0,0)) & (viajesmayo['hora alquiler'] < datetime.time(20,0,0))) |
           (viajesmayo['hora alquiler'] >= datetime.time(23,0,0))) &
           (viajesmayo['dia alquiler']>datetime.date(anyo,5,1))]
        caracteristicas_usuario['viajes prohibidos mayo']       = len(viajes_prohibidos_mayo)/(0.0001+len(viajesmayo))
        
        if edaduser != 7:    
            viajes_prohibidos_junio = viajesjunio[
                (((viajesjunio['hora alquiler'] >= datetime.time(10,0,0)) & (viajesjunio['hora alquiler'] < datetime.time(12,0,0))) |
                ((viajesjunio['hora alquiler'] >= datetime.time(19,0,0)) & (viajesjunio['hora alquiler'] < datetime.time(20,0,0)))) &
                ((viajesjunio['dia alquiler']>=datetime.date(anyo,6,1)) & (viajesjunio['dia alquiler']<=datetime.date(anyo,6,15)))]
            caracteristicas_usuario['viajes prohibidos junio']       = len(viajes_prohibidos_junio)/(0.0001+len(viajesjunio))
        else:
            #los mayores de 70 no tenían horario prohibido
            caracteristicas_usuario['viajes prohibidos junio']       = 0
            
        viajes_prohibidos_octubre = viajesoctubre[
            (viajesoctubre['hora alquiler'] <= datetime.time(6,0,0)) &
            (viajesoctubre['dia alquiler']>datetime.date(anyo,10,25))]
        
        caracteristicas_usuario['viajes prohibidos octubre']       = len(viajes_prohibidos_octubre)/(0.0001+len(viajesoctubre))
    
        viajes_prohibidos_noviembre = viajesnoviembre[
            (viajesnoviembre['hora alquiler'] <= datetime.time(6,0,0)) &
            (viajesnoviembre['dia alquiler']>datetime.date(anyo,11,1))]
        
        caracteristicas_usuario['viajes prohibidos noviembre']       = len(viajes_prohibidos_noviembre)/(0.0001+len(viajesnoviembre))
    
        viajes_prohibidos_diciembre = viajesdiciembre[
            (
                (viajesdiciembre['hora alquiler'] <= datetime.time(6,0,0)) &
                (
                    (
                        (viajesdiciembre['dia alquiler']>=datetime.date(anyo,12,1)) &
                        (viajesdiciembre['dia alquiler']<=datetime.date(anyo,12,18))
                    ) |
                        (viajesdiciembre['dia alquiler']==datetime.date(anyo,12,24))
                )
            ) |
            (
                (
                    (viajesdiciembre['hora alquiler'] <= datetime.time(6,0,0))|
                    (viajesdiciembre['hora alquiler'] >= datetime.time(23,0,0))
                ) &
                (
                    (viajesdiciembre['dia alquiler'] >= datetime.date(anyo,12,18))
                )
            )]
        
        caracteristicas_usuario['viajes prohibidos diciembre']       = len(viajes_prohibidos_diciembre)/(0.0001+len(viajesdiciembre))
        
            
        caracteristicas[usuario] = caracteristicas_usuario
        numerovueltas+=1
        if numerovueltas%500 == 0 or numerovueltas == 1:
            print(str(anyo) + 'lyon + social + prohibido - Van ', numerovueltas)
        
    
    #%%save as pickle
    
    caracteristicasDf = pd.DataFrame.from_dict(caracteristicas, orient = 'index')
    caracteristicasDf.to_csv(directorio + '6_vectoresCaracteristicasLyonYSocial' + str(anyo) +'.csv', index = False)
    
avisame()