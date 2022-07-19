# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 11:22:23 2022

@author: haffa
"""

import pandas as pd

#%% load the data
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'

### trayectos de 19 y 20 donde cada usuario tiene al menos 18 viajes al año y al menos 5 son en época de confinamiento
viajes2019 = pd.read_pickle(directorio + '2_movimientos2019Mas24.pkl')  
viajes2020 = pd.read_pickle(directorio + '2_movimientos2020Mas24.pkl')
viajes2019 = viajes2019.rename(columns = {'Abonado':'abonado'})
viajes2020 = viajes2020.rename(columns = {'Abonado':'abonado'})


usuarios19_20 = pd.read_pickle(directorio + '3_singleusers_numerico.pkl')  ### datos de usuario recientes

#%% select only users that appear in both sides

usuarios19_20 = usuarios19_20[usuarios19_20['abonado'].isin(list(viajes2019['abonado'].unique()))]
viajes2019_c = viajes2019[viajes2019['abonado'].isin(list(usuarios19_20['abonado'].unique()))]
viajes2020_c = viajes2020[viajes2020['abonado'].isin(list(usuarios19_20['abonado'].unique()))]

#%% save the new data

usuarios19_20.to_pickle(directorio + '4_singleusers_numerico_finales.pkl')
viajes2019_c.to_pickle(directorio + '4_movimientos2019Mas24_finales.pkl')
viajes2020_c.to_pickle(directorio + '4_movimientos2020Mas24_finales.pkl')