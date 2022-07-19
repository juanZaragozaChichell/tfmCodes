import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from myusefulgraphics import plotDonut

#%% loading data that will generally be used
print('Starting process...')
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
graphics_path = directorio + 'graphics_clusters_pc_new/'
idioma_numero = pd.read_csv(directorio + '3_relacion_idioma_numero.csv')
edad_numero   = pd.read_csv(directorio + '3_relacion_edad_numero.csv')
sexo_numero   = pd.read_csv(directorio + '3_relacion_sexo_numero.csv')

edad_numero['Rango de edad'] = ['Younger than 14 yo','14 - 17 yo','18 - 25 yo', '26 - 35 yo','36 - 45 yo', '46 - 55 yo','56 - 75 yo','Older than 75 yo']
sexo_numero['Sexo'] = ['Male', 'Female']
idioma_numero['Idioma'] = ['Spanish','English','Valencian','French']

anyos = [2019, 2020]

datos_nombre = {
    '5_'   : ['Lyon', 'BD1'],
    '7_'   : ['Generales','BD2'],
    '9_1_' : ['Control','BD3.1'],
    '9_2_' : ['Estadisticas','BD3.2']
    }

#%% iterate over each year and over every database with liars information

for year in anyos:
    print('Starts year ' + str(year))
    for num_dato in datos_nombre:
        tipo_dato = datos_nombre[num_dato][0]
        print('\t starts data base ' + tipo_dato)

        ## read data and determine the clusters
        raw_data = pd.read_csv(directorio + num_dato + 'vectoresCaracteristicasCluster' + tipo_dato + str(year) + '.csv')
        raw_data = raw_data.drop(columns = ['Unnamed: 0'])
        clusters = raw_data['Cluster'].unique()
    
        
        ## within every database, iterate over the different clusters it has
        for cluster in clusters:
            ## select elements of database within that cluster
            data_of_cluster = raw_data[raw_data['Cluster'] == cluster]
                    
            ## count how many men/women, english/spanish/... there are in such cluster
            edades  = data_of_cluster['edad'].value_counts()
            sexos   = data_of_cluster['sexo'].value_counts()
            idiomas = data_of_cluster['idioma'].value_counts()
            
            
            idioma_labels = [idioma_numero.loc[idioma]['Idioma'] for idioma in idiomas.keys()]
            sexo_labels = [sexo_numero.loc[Sexo]['Sexo'] for Sexo in sexos.keys()]
            edad_labels = [edad_numero.loc[edad]['Rango de edad'] for edad in edades.keys()]
            
            ## plot that information in a donut
            picture = plotDonut(edades,idiomas,sexos,edad_labels, idioma_labels, sexo_labels, year, '- Data of elements from cluster ' + str(cluster) + '\n'
            + datos_nombre[num_dato][1] + '\t' + str(year))
            picture.savefig(graphics_path + 'donutTodosCluster_' + str(cluster) + '_' +datos_nombre[num_dato][1] +'_' + str(year) +'.png')


            ## determine biggest liars
            raw_data['porcentaje medio viajes prohibidos'] = (raw_data['viajes prohibidos mayo'] +
                                                                    raw_data['viajes prohibidos junio'] +
                                                                    raw_data['viajes prohibidos octubre'] +
                                                                    raw_data['viajes prohibidos noviembre'] +
                                                                    raw_data['viajes prohibidos diciembre'])/5
            
            usuarios_mas_viajes_prohibidos = raw_data[raw_data['porcentaje medio viajes prohibidos']>=
                                                    raw_data['porcentaje medio viajes prohibidos'].describe()['mean']]
            ## description of the liars within that cluster
            liars_of_cluster = data_of_cluster[data_of_cluster['abonado'].isin(usuarios_mas_viajes_prohibidos['abonado'])]
            idiomas_umvp = liars_of_cluster['idioma'].value_counts()
            sexo_umvp    = liars_of_cluster['sexo'].value_counts()
            edad_umvp    = liars_of_cluster['edad'].value_counts()
            
            idioma_labels = [idioma_numero.loc[idioma]['Idioma'] for idioma in idiomas_umvp.keys()]
            sexo_labels = [sexo_numero.loc[Sexo]['Sexo'] for Sexo in sexo_umvp.keys()]
            edad_labels = [edad_numero.loc[edad]['Rango de edad'] for edad in edad_umvp.keys()]
            
            picture = plotDonut(edad_umvp,idiomas_umvp,sexo_umvp,edad_labels, idioma_labels, sexo_labels, year, '- Users with the most trips during non-allowed hours from cluster ' + str(cluster) + '\n '+ datos_nombre[num_dato][1] + str(year))
            picture.savefig(graphics_path + 'donutIlicitosCluster_' + str(cluster) + '_' + datos_nombre[num_dato][1] + '_' + str(year) +'.png')
            
            plt.close('all')
            print('\t pictures of cluster ' + str(cluster) + ' for data ' + datos_nombre[num_dato][1] + ': DONE')

print('ALL DONE')



