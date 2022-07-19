# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 21:30:13 2022

@author: haffa
"""

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import winsound

def avisame():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)




directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
graphics_path = directorio + 'graphics/'
anyos = [2019,2020]

datos_nombres = {
    '5_'   : 'Lyon',
    '7_'   : 'Generales',
    '9_1_' : 'Control',
    '9_2_' : 'Estadisticas'
    }

for anyo in anyos:
    print('Empieza ' + str(anyo))
    for tipo_dato in datos_nombres:
        data_type = datos_nombres[tipo_dato]
        print('\t Empieza ' + data_type)
        datos = pd.read_csv(directorio + tipo_dato + 'vectoresCaracteristicas' + data_type + str(anyo) + '.csv')
        
        matriz_datos = datos.drop(columns = ['abonado'])
        columnas = list(matriz_datos.keys())
        matriz_datos = matriz_datos.values
        matriz_datos = StandardScaler().fit_transform(matriz_datos)
        ## PCA evaluation
        print('\t Evaluación PCA')
        pca = PCA(n_components = 0.85)
        principalComponents = pca.fit_transform(matriz_datos)
        
        componentes_principales_df = pd.DataFrame(principalComponents,columns = ['PC' + str(i+1) for i in range(len(principalComponents[0]))])
        columna_abonados = datos['abonado']
        componentes_principales_df.insert(0,'abonado',columna_abonados)
        
        #silhouette para las componentes principales
        print('\t Evaluando número de clusters óptimo para kmenas: silhouette')
        scores = []
        for k in range(2,6):
            kmeans = KMeans(n_clusters = k, random_state = 42)
            y_pred = kmeans.fit_predict(principalComponents)
            scores.append(silhouette_score(principalComponents, kmeans.labels_))
        
        print('\t Evaluando k -means')
        number_of_clusters = scores.index(max(scores)) + 2 # index 0 is 2 clusters
        
        kmeans = KMeans(n_clusters = number_of_clusters, random_state = 42)
        y_pred = kmeans.fit_predict(principalComponents)                          # Fitting the input data
        centroids = kmeans.cluster_centers_
        print('\t Formando DataFrames y guardando')
        componentes_principales_df['Cluster'] = y_pred
        componentes_principales_df.to_csv(directorio + '11_vectoresComponentesPrincipalesCluster' + data_type + str(anyo) + '.csv', index = False)
        dic_centroides = {'Centroide clase ' + str(i) : centroids[i] for i in range(number_of_clusters)}
        centroidsDf = pd.DataFrame.from_dict(dic_centroides, orient='index',columns = ['PC' + str(i+1) for i in range(len(centroids[0]))])
        centroidsDf['Cluster'] = [i for i in range(number_of_clusters)]
        centroidsDf.to_csv(directorio + '11_centroides' + data_type + str(anyo) + '.csv', index = False)
        print('------' + tipo_dato + ' HECHO')


print('YA ESTAAAAAA')
avisame()