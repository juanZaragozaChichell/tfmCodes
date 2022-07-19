# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 12:28:58 2022

@author: haffa
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import pairwise_distances_argmin_min
import winsound


def avisame():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    
directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
graphics_path = directorio + 'graphics_clusters_pc_new/'

datos_nombre = {
    '5_'   : ['Lyon', 'BD1'],
    '7_'   : ['Generales','BD2'],
    '9_1_' : ['Control','BD3.1'],
    '9_2_' : ['Estadisticas','BD3.2']
    }

anyos = [2019,2020]
vueltas = 0
for anyo in anyos:
    print('Empieza' + str(anyo))
    for numero in datos_nombre:
        if numero != '5_':
            print('\t Empieza '+ datos_nombre[numero][0])
            ## data loading
            print('\t \t Data Loading')
            raw_data = pd.read_csv(directorio + numero + 'vectoresCaracteristicasCluster' + datos_nombre[numero][0] + str(anyo) + '.csv')
            data_pc = pd.read_csv(directorio + '11_vectoresComponentesPrincipalesCluster' + datos_nombre[numero][0] + str(anyo) + '.csv')
            centroides = pd.read_csv(directorio + '11_centroides' + datos_nombre[numero][0] + str(anyo) + '.csv')
            
            datos_sin_abonado = data_pc.drop(columns = ['abonado', 'Cluster'])
            datos_values = datos_sin_abonado.values
            clusters = list(centroides['Cluster'])
            centroides = centroides.drop(columns = ['Cluster'])
            centroid_values = centroides.values
            centroid_values = centroid_values.copy(order = 'C')
            datos_values = datos_values.copy(order = 'c')
            closest, _ = pairwise_distances_argmin_min(centroid_values, datos_values)
            
            usuarios_mas_cercanos_centroides = {'usuario_centroide' + str(i) : data_pc.loc[closest[i]]['abonado'].astype('int') for i in range(len(closest))}
            
            ## users with the most forbiden trips
            print('\t\t Evaluando los usuarios con más viajes prohibidos')
            raw_data['porcentaje medio viajes prohibidos'] = (raw_data['viajes prohibidos mayo'] +
                                                            raw_data['viajes prohibidos junio'] +
                                                            raw_data['viajes prohibidos octubre'] +
                                                            raw_data['viajes prohibidos noviembre'] +
                                                            raw_data['viajes prohibidos diciembre'])/5
            usuarios_mas_viajes_prohibidos = raw_data[raw_data['porcentaje medio viajes prohibidos']>=raw_data['porcentaje medio viajes prohibidos'].describe()['mean']]
            usuarios_mas_viajes_prohibidos = usuarios_mas_viajes_prohibidos.drop(columns = ['Unnamed: 0'])
            
            
            usuarios_cluster = {num_cluster : usuarios_mas_viajes_prohibidos[usuarios_mas_viajes_prohibidos['Cluster'] == num_cluster] for num_cluster in clusters}
            
            ## Pie Chart todos
            print('\t\t Creando el gráfico de tarta para todos')
            labels_pie = [str(num_cluster) for num_cluster in clusters]
            usuarios_cluster_todos = {num_cluster : data_pc[data_pc['Cluster'] == num_cluster] for num_cluster in clusters}
            sizes_pie  = (1/len(usuarios_cluster))*np.array([len(usuarios_cluster_todos[num_cluster]) for num_cluster in clusters])
            explode = [0 for i in clusters]
            
            fig1, ax1 = plt.subplots(figsize = (10,10))
            ax1.pie(sizes_pie, explode=explode, labels=labels_pie, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.legend(title = 'Number of cluster -', loc = 1, fontsize = 22)
            plt.title('Percentage of users per cluster - ' + datos_nombre[numero][1] + str(anyo), fontsize = 22)
            fig1.savefig(graphics_path + 'pieChartTodos' + datos_nombre[numero][0] + str(anyo) + '.png',bbox_inches='tight')
            
            
            
            
            
            ## Pie Chart ilicitos
            print('\t\t Creando el gráfico de tarta para ilicitos')
            labels_pie = [str(num_cluster) for num_cluster in clusters]
            sizes_pie  = (1/len(usuarios_cluster))*np.array([len(usuarios_cluster[num_cluster]) for num_cluster in clusters])
            explode = [0 for i in clusters]
            
            fig1, ax1 = plt.subplots(figsize = (10,10))
            ax1.pie(sizes_pie, explode=explode, labels=labels_pie, autopct='%1.1f%%',
                    shadow=True, startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            plt.legend(title = 'Number of cluster -', loc = 1, fontsize = 14)
            plt.title('Percentage of users with most illicit trips per cluster - ' + datos_nombre[numero][1] + str(anyo), fontsize = 22)
            fig1.savefig(graphics_path + 'pieChartIlicitos' + datos_nombre[numero][0] + str(anyo) + '.png',bbox_inches='tight')
            
            ## Chart of mean value of principal components for travelers in each cluster
            
            usuarios_pc_cluster = {num_cluster : data_pc[data_pc['Cluster'] == num_cluster] for num_cluster in clusters}
            
            valores_medios_pc_cluster = {}
            std_pc_cluster = {}
            #crando diccionario 
            print('\t \t Creando diccionario y gráfico de componentes principales')
            for num_cluster in clusters:
                usuarios_pc_cluster[num_cluster] = usuarios_pc_cluster[num_cluster].drop(columns = ['abonado', 'Cluster'])
                data_description = usuarios_pc_cluster[num_cluster].describe()
                valores_medios_pc_cluster[num_cluster] = data_description.loc['mean']
                std_pc_cluster[num_cluster] = data_description.loc['std']
            
            fig = plt.figure(figsize = (10,10))
            x = [i+1 for i in range(len(valores_medios_pc_cluster[0]))]
            y = [valores_medios_pc_cluster[num_cluster].values for num_cluster in clusters ]
            yerr = [std_pc_cluster[num_cluster].values for num_cluster in clusters ]
            
            [plt.errorbar(x, y[i], yerr=yerr[i], label='Mean values of PC for cluster ' + str(i), linestyle='None', marker='s') for i in clusters]
            plt.title(str(anyo) + ' - ' + datos_nombre[numero][1] + ' - Mean value and standard deviation for each PC by cluster\n for users with the highest average dutring curfew hours', fontsize = 22)
            plt.legend(loc='lower right', fontsize = 15)
            fig.savefig(graphics_path + 'componentesPrincipalesVMySTD' + str(anyo) + datos_nombre[numero][0] +'.png',bbox_inches='tight')


            print('\t\t Creando gráfico centroides')
            fig = plt.figure(figsize = (10,10))
            x = range(1,1+len(centroid_values[0]))
            y = [centroid_values[i] for i in range(len(centroid_values))]
            
            [plt.scatter(x, y[i],marker = 's',label='Centroid ' + str(i)) for i in range(len(y))]
            plt.title(str(anyo)+ ' - ' + datos_nombre[numero][1] + ' - Value of each PC for every centroid', fontsize = 22)
            plt.legend(loc='lower right', fontsize = 15)
            
            fig.savefig(graphics_path + 'componentesPrincipalesCentroides' + str(anyo) + datos_nombre[numero][0] +'.png',bbox_inches='tight')
            
            vueltas +=1
            print('van ' + str(vueltas))
            plt.close('all')
        
        else:
            print('\t Empieza '+ datos_nombre[numero][0])
            ## data loading
            print('\t \t Data Loading')
            raw_data = pd.read_csv(directorio + numero + 'vectoresCaracteristicasCluster' + datos_nombre[numero][0] + str(anyo) + '.csv')
            data_pc = pd.read_csv(directorio + '11_vectoresComponentesPrincipalesCluster' + datos_nombre[numero][0] + str(anyo) + '.csv')
            centroides = pd.read_csv(directorio + '11_centroides' + datos_nombre[numero][0] + str(anyo) + '.csv')
            
            datos_sin_abonado = data_pc.drop(columns = ['abonado', 'Cluster'])
            datos_values = datos_sin_abonado.values
            clusters = list(centroides['Cluster'])
            centroides = centroides.drop(columns = ['Cluster'])
            centroid_values = centroides.values
            centroid_values = centroid_values.copy(order = 'C')
            datos_values = datos_values.copy(order = 'c')
            closest, _ = pairwise_distances_argmin_min(centroid_values, datos_values)
            
            usuarios_mas_cercanos_centroides = {'usuario_centroide' + str(i) : data_pc.loc[closest[i]]['abonado'].astype('int') for i in range(len(closest))}
            ## Chart of mean value of principal components for travelers in each cluster
            
            usuarios_pc_cluster = {num_cluster : data_pc[data_pc['Cluster'] == num_cluster] for num_cluster in clusters}
            
            valores_medios_pc_cluster = {}
            std_pc_cluster = {}

            print('\t\t Creando gráfico centroides')
            fig = plt.figure(figsize = (10,10))
            x = range(1,1+len(centroid_values[0]))
            y = [centroid_values[i] for i in range(len(centroid_values))]
            
            [plt.scatter(x, y[i],marker = 's',label='Centroid ' + str(i)) for i in range(len(y))]
            plt.title(str(anyo) +' - '  + datos_nombre[numero][1] + ' - Value of each PC for every centroid', fontsize = 22)
            plt.legend(loc='lower right', fontsize = 15)
            
            fig.savefig(graphics_path + 'componentesPrincipalesCentroides' + str(anyo) + datos_nombre[numero][0] +'.png',bbox_inches='tight')
            
            vueltas +=1
            print('van ' + str(vueltas))
            plt.close('all')

        
print('############# \n Ya está\n #############')
avisame()
        