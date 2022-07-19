import pandas as pd
import numpy as np
import winsound

#%% auxiliar functions
def avisame():
    duration = 5000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)

def estacionToCod(estacion):
    return int(estacion.split('_')[0])

#%% set directory for the xlsx
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/datosValenBisi/Lluis/2018_2021'

directorio_guardar = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'

datos2019xlsx = directorio + '/Movimientos_2019.xlsx'
datos2020xlsx = directorio + '/Movimientos_2020 - copia.xlsx'
#%% read the files
meses19 = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
meses20 = ['Enero', 'Febrero', 'Marzo', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
print('Leyendo datos\n')
datos19 = pd.read_excel(datos2019xlsx, sheet_name = meses19)
datos20 = pd.read_excel(datos2020xlsx, sheet_name = meses20)
print('Datos leídos\n')

#%% files have a formating isue: we correct it
print('Arreglando el formato')

for mes in meses19:
    _ = datos19[mes]
    columnas = list(_.keys())
    if 'Estación salida ' in columnas:
        _ = _.rename(columns = {'Estación salida ': 'Estación salida'})
    if 'Estación llegada ' in columnas:
        _ = _.rename(columns = {'Estación llegada ': 'Estación llegada'})
    datos19[mes] = _

for mes in meses20:
    _ = datos20[mes]
    columnas = list(_.keys())
    if 'Estación salida ' in columnas:
        _ = _.rename(columns = {'Estación salida ': 'Estación salida'})
    if 'Estación llegada ' in columnas:
        _ = _.rename(columns = {'Estación llegada ': 'Estación llegada'})
    datos20[mes] = _
    
#%% we concatenate all the pandas dataframe created previously into two big dataframes
datos19 = pd.concat([datos19[mes] for mes in meses19], ignore_index=True)
datos20 = pd.concat([datos20[mes] for mes in meses20], ignore_index=True)

#%% we remove trips that took longer than 45 minutes
print('Eliminando viajes de más de 45 minutos')
datos19 = datos19[(datos19['Duración trayeto']<=45) & (datos19['Duración trayeto']>=3)]
datos20 = datos20[(datos20['Duración trayeto']<=45) & (datos20['Duración trayeto']>=3)]

#%% we are going to save the codes of the stations just by numeric
## we shall save a dictionary that correlates numbers and the name of the station

estaciones19 = datos19['Estación salida']
estaciones19 = list(set(list(estaciones19))) ## list of the stations number_street

estaciones20 = datos20['Estación salida']
estaciones20 = list(set(list(estaciones20))) ## list of the stations number_street

#%% saving the relations between codes and stations 
estacionescsv19 = []
for estacion in estaciones19:
    codigo = estacion.split('_')[0]
    nombre = estacion.split('_')[1:]
    nombre = ' '.join(nombre)
    estacionescsv19.append([codigo, nombre])
    
# the dictionary
estaciones19dic = {'Código estación' : np.array(estacionescsv19)[:,0], 'Nombre estación': np.array(estacionescsv19)[:,1]}
est19df = pd.DataFrame.from_dict(estaciones19dic, orient = 'columns')

est19df.to_csv(directorio_guardar + '1_relacion_numero_estacion.csv', index = False)
print('Relaciones estación-código guardadas')
#%% we only get those with actual stations as arriving stations

datos19 = datos19[datos19['Estación llegada']!= 'Especial']
datos20 = datos20[datos20['Estación llegada']!= 'Especial']

#%% we change the value of stations to only the numeric code
print('Cambiando las estaciones a numérico en las columnas')
datos19['Estación salida'] = datos19['Estación salida'].apply(estacionToCod)
datos19['Estación llegada'] = datos19['Estación llegada'].apply(estacionToCod)

datos20['Estación salida'] = datos20['Estación salida'].apply(estacionToCod)
datos20['Estación llegada'] = datos20['Estación llegada'].apply(estacionToCod)

#%% we create columns of time and date for start of a trip

fechas19 = [timestamp.date() for timestamp in datos19['Alquiler']]
fechas20 = [timestamp.date() for timestamp in datos20['Alquiler']]

horas19salida = [timestamp.time() for timestamp in datos19['Alquiler']]
horas20salida = [timestamp.time() for timestamp in datos20['Alquiler']]

datos19['dia alquiler'] = fechas19
datos20['dia alquiler'] = fechas20
datos19['hora alquiler'] = horas19salida
datos20['hora alquiler'] = horas20salida
print('Columnas para las fechas y las horas creadas')
#%% we remove columns that are not going to be used
datos19 = datos19.drop(columns = ['Alquiler', 'Devolución','Tipo de abono'])
datos20 = datos20.drop(columns = ['Alquiler', 'Devolución','Tipo de abono'])

#%% we save this data as pickle to make it fast for reading in the future

datos19.to_pickle(directorio_guardar + '1_movimientos2019procesado.pkl')
datos20.to_pickle(directorio_guardar + '1_movimientos2020procesado.pkl')

avisame()