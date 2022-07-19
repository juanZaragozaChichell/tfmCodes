# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 19:37:42 2022

@author: haffa
"""

import pandas as pd
import winsound

#%% auxiliar functions
def avisame():
    duration = 5000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

#%% loading the data
print('Leyendo datos')
directorio = "D:\\Desktop\\Estudios\\UNIVERSIDAD\\Investmat\\TFM\\datosValenBisi\\Lluis"
directorio = directorio.replace('\\', '/')

#### documentos a escanear
excel1 = 'UsuariosAntiguo.xlsx'  # lo llamaré hoja0
excel2 = 'UsuariosNuevosincontraseña2.xlsx' ## este tiene siete hojas HojaN --> lo llamaré hojaN

root_excel1 = directorio + '/' + excel1
root_excel2 = directorio + '/' + excel2
hoja0 = pd.read_excel(root_excel1, sheet_name = 'Hoja1')

hojas = ['Hoja' + str(n) for n in [1,2,3,4,5,6,7]]
HojaN = pd.read_excel(root_excel2, sheet_name = hojas)

hoja1 = HojaN['Hoja1']
hoja2 = HojaN['Hoja2']
hoja3 = HojaN['Hoja3']
hoja4 = HojaN['Hoja4']
hoja5 = HojaN['Hoja5']
hoja6 = HojaN['Hoja6']
hoja7 = HojaN['Hoja7']

#%% we eliminate non-useful columns
print('Eliminando columnas inútiles')
hoja0 = hoja0.drop(columns = ['Contrat', 'Label sous-type abonné Kiwi','Dpt-Arc', 'Código ciudad', 'Fin abo', 'Nb loc',
        'Date de première création', 'Sous-type de prélèvement',
        'Type de réabonnement', 'Type de badge',
        'Label type de tarif abonné Kiwi','Estado usuario'])
hoja1 = hoja1.drop(columns = ['Dirección' , 'Final de la suscripción', 'Primer suscripción'])
hoja2 = hoja2.drop(columns = ['Dirección' ,'Final de la suscripción','Primer suscripción'])
hoja3 = hoja3.drop(columns = ['Dirección' , 'Final de la suscripción','Primer suscripción'])
hoja4 = hoja4.drop(columns = ['Dirección' ,'Final de la suscripción','Primer suscripción'])
hoja5 = hoja5.drop(columns = ['Dirección' , 'Final de la suscripción', 'Primer suscripción'])
hoja6 = hoja6.drop(columns = ['Dirección' , 'Final de la suscripción','Primer suscripción'])
hoja7 = hoja7.drop(columns = ['Dirección' , 'Final de la suscripción','Primer suscripción'])

#%% we rename the columns so that we can merge them without trouble
print('Renombrando columnas')
columnas  = ['abonado', 'código postal', 'sexo', 'edad','fecha suscripción', 'idioma']
columnas0 = {clave : columnas[i] for i, clave in enumerate(list(hoja0.keys())) }
columnasN = {clave : columnas[i] for i, clave in enumerate(list(hoja1.keys())) }

hoja0 = hoja0.rename(columns = columnas0)
hoja1 = hoja1.rename(columns = columnasN)
hoja2 = hoja2.rename(columns = columnasN)
hoja3 = hoja3.rename(columns = columnasN)
hoja4 = hoja4.rename(columns = columnasN)
hoja5 = hoja5.rename(columns = columnasN)
hoja6 = hoja6.rename(columns = columnasN)
hoja7 = hoja7.rename(columns = columnasN)

#%% we merge them all together, wliminate those that have no defined sex and no defined language
#also, we eliminate the possible NaN
print('Eligiendo los buenos por edad, sexo e idioma')
allUsers = pd.concat([hoja0, hoja1, hoja2, hoja3, hoja4, hoja5, hoja6, hoja7],ignore_index=True)
allUsers = allUsers.loc[allUsers['sexo'].isin(['Mujer', 'Hombre'])] # nos quedamos con las personas que tienen el sexo bien definido
allUsers = allUsers[allUsers['idioma'] != 'Elija un idioma de la lista'] # nos quedamos con los que tienen un idioma elegido
allUsers = allUsers.dropna()

#%% we save the relationship of age 
edades = {'Menos de 14 años' : 0, '14 - 17 años' : 1, '18 - 25 años':2,
          '26 - 35 años':3, '36 - 45 años':4, '46 - 55 años':5, '56 - 75 años':6, 'Más de 75 años':7 }
claves = list(edades.keys())
valores = [[clave,edades[clave]] for clave in claves]
edadesdf = pd.DataFrame(valores, columns = ['Rango de edad', 'Rango de edad numérico'])
edadesdf.to_csv('3_relacion_edad_numero.csv', index = False)

#%% there are users that appear more than once.prior to getting the most actual user, we change the age to numeric so that we can compare

for edad in edades:
    allUsers['edad'] = allUsers['edad'].replace([edad], edades[edad])

#%% there are users that appear more than once. We detect them and save only the last appearance

## creo un diccionario cuyas keys son el código de abonado de un usuario si ese código aparece más de una vez en la base de datos
## cada key contiene los datos repetidos del usuario
print('Eliminando repetidos')
usuarios = list(set(allUsers['abonado']))
diccionarioRepes = {}
for user in usuarios:
    repetidosusuario = allUsers[allUsers['abonado'] == user]
    if len(repetidosusuario) == 1:
        pass
    else:
        diccionarioRepes[user] = repetidosusuario
        
repes = list(diccionarioRepes.keys())  # estos son los usuarios que aparecen repetidos
for user in repes:
    # para cada usuario repetido, elimino los duplicados por fecha de suscripción
    diccionarioRepes[user] = diccionarioRepes[user].drop_duplicates(subset = ['fecha suscripción'])
    
    #ahora me quedo con el más reciente de los repetidos para ese usuario
    df = diccionarioRepes[user]
    ma = max(df['fecha suscripción'])
    diccionarioRepes[user] = df[df['fecha suscripción'] == ma]
    
#%% we eliminate repeated users from allUsers dataframe, 
#that way we will have two disoint dataframes and we'll be able to merge them perfectly

almostAllUsers = allUsers
for user in repes:
    almostAllUsers = almostAllUsers[almostAllUsers['abonado'] != user] #los voy eliminando por bloques

singleusers = almostAllUsers
for user in repes:
    _ = diccionarioRepes[user]
    singleusers = pd.concat([singleusers,_], ignore_index = True)

#%% we change the language to numeric
print('Cambiando el idioma a numérico')
idi = ['Español', 'Inglés', 'Valenciano', 'Francés']
idiomas = {idi[i] : i for i in range(4)}       # esp ->0 ing->1 val->2 fran->3
for idioma in idiomas:
    singleusers['idioma'] = singleusers['idioma'].replace([idioma], idiomas[idioma])


claves = list(idiomas.keys())
valores = [[clave,idiomas[clave]] for clave in idiomas]
idiomasdf = pd.DataFrame(valores, columns = ['Idioma', 'Idioma numérico'])
idiomasdf.to_csv('3_relacion_idioma_numero.csv', index = False)

#%%  we change the sex to numberic
print('Cambiando el sexo a numérico')
sexos = {'Hombre': 0, 'Mujer':1}

claves = list(sexos.keys())
valores = [[clave,sexos[clave]] for clave in sexos]
sexosdf = pd.DataFrame(valores, columns = ['Sexo', 'Sexo numérico'])
sexosdf.to_csv('3_relacion_sexo_numero.csv', index = False)
for sex in sexos:
    singleusers['sexo'] = singleusers['sexo'].replace([sex], sexos[sex])

#%% now we can eliminate the date of suscription
singleusers = singleusers.drop(columns=['fecha suscripción'])
singleusers.to_pickle('3_singleusers_numerico.pkl')



avisame()


