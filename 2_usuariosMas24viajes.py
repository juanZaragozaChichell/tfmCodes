# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 12:43:50 2022

@author: haffa
"""

import pandas as pd
import datetime
import winsound

#%% auxiliar functions
def avisame():
    duration = 5000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

#%% load the data
print('Leyendo datos')
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
datos19 = pd.read_pickle(directorio + '1_movimientos2019procesado.pkl')
datos20 = pd.read_pickle(directorio + '1_movimientos2020procesado.pkl')

#%% select users from both

usuarios19 = datos19['Abonado']
usuarios20 = datos20['Abonado']
#%% count how many times an user appears

users19_counted = usuarios19.value_counts()
users20_counted = usuarios20.value_counts()

#%% select only those that appear more than 18 times each year and have trips from may to decembre 
viajes_mayo_diciembre_2019 = datos19[datos19['dia alquiler'] >= datetime.date(2019,5,1)]
viajes_mayo_diciembre_2020 = datos20[datos20['dia alquiler'] >= datetime.date(2020,5,1)]

usuarios19_from_mayo = viajes_mayo_diciembre_2019['Abonado']
usuarios20_from_mayo = viajes_mayo_diciembre_2020['Abonado']
users19_from_mayo_counted = usuarios19_from_mayo.value_counts()
users20_from_mayo_counted = usuarios20_from_mayo.value_counts()

users19_unique = set(list(usuarios19_from_mayo))
users20_unique = set(list(usuarios20_from_mayo))
users_unique = list(users19_unique.intersection(users20_unique))

usersPlus24 = []
print('Verificando condiciones de usuarios')
for user in users_unique:
    if (users19_counted[user] >=18 ) and (users20_counted[user] >=18 ) and (users19_from_mayo_counted[user]>=5) and (users20_from_mayo_counted[user]>=5):
        usersPlus24.append(user)
        
#%% create df that only contain this users

usuarios19Plus24 = datos19[datos19['Abonado'].isin(usersPlus24)]
usuarios20Plus24 = datos20[datos20['Abonado'].isin(usersPlus24)]

#%% save them as pkl

usuarios19Plus24.to_pickle(directorio + '2_movimientos2019Mas24.pkl')
usuarios20Plus24.to_pickle(directorio + '2_movimientos2020Mas24.pkl')
avisame()