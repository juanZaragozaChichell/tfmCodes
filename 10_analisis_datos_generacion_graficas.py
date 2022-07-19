# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 21:45:03 2022

@author: haffa
"""

import pandas as pd
from myusefulgraphics import plotExplainedVariance, matrixPCA, plotclustersKmeans, plotKMeans3D, plotSOMclusters
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import winsound

def avisame():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)




directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
graphics_path = directorio + 'graphics_new/'
anyos = [2019,2020]

datos_nombres = {
    '5_'   : ['Lyon','BD1'],
    '7_'   : ['Generales','BD2'],
    '9_1_' : ['Control','BD3.1'],
    '9_2_' : ['Estadisticas','BD3.2']
    }


for anyo in anyos:
    print('Empieza ' + str(anyo))
    for tipo_dato in datos_nombres:
        data_type = datos_nombres[tipo_dato][0]
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
        picture = plotExplainedVariance(pca, anyo, datos_nombres[tipo_dato][1])
        picture.savefig(graphics_path + 'explainedVariance'+ str(anyo) + data_type + '.png')

        ## matrix of PC and features
        print('\t Matriz PCA calculandose')
        picture = matrixPCA(pca, anyo ,columnas, datos_nombres[tipo_dato][1])
        picture.savefig(graphics_path + 'matrixPCA'+ str(anyo) + data_type + '.png',bbox_inches='tight')
        
        
        
        #silhouette para las propias features de la matriz normalizadas, como hacen los de lyon
        # print('\t Haciendo silhouette plot datos raw')
        # scores = []
        # for k in range(2,15):
        #     kmeans = KMeans(n_clusters = k)
        #     y_pred = kmeans.fit_predict(matriz_datos)
        #     scores.append(silhouette_score(matriz_datos, kmeans.labels_))
        
        # fig = plt.figure()    
        # plt.plot(range(2,15), scores, 'bx-')
        # plt.xlabel('Number of clusters')
        # plt.ylabel('Silhouette score')
        # plt.title('Raw data - Silhouete score Vs number of clusters ' +  str(anyo) + '-' + 'Lyon')
        # fig.savefig(graphics_path + 'silhouette'+ str(anyo) + data_type + 'Raw.png')
        
        
        #silhouette para las componentes principales
        print('\t Haciendo silhouette plot componentes principales')
        scores = []
        for k in range(2,15):
            kmeans = KMeans(n_clusters = k, random_state = 42)
            y_pred = kmeans.fit_predict(principalComponents)
            scores.append(silhouette_score(principalComponents, kmeans.labels_))
        
        fig = plt.figure()    
        plt.plot(range(2,15), scores, 'bx-')
        plt.xlabel('Number of clusters')
        plt.ylabel('Silhouette score')
        plt.title('Silhouete score Vs number of clusters ' +  str(anyo) + '-' + datos_nombres[tipo_dato][1])
        fig.savefig(graphics_path + 'silhouette'+ str(anyo) + data_type + 'PrincipalComponents.png')
        
        print('\t Evaluando k -means')
        number_of_clusters = scores.index(max(scores)) + 2 # index 0 is 2 clusters
        
        kmeans = KMeans(n_clusters = number_of_clusters, random_state = 42)
        y_pred = kmeans.fit_predict(principalComponents)                          # Fitting the input data
        centroids = kmeans.cluster_centers_
        print('\t Formando DataFrames y guardando')
        datos['Cluster'] = y_pred
        datos.to_csv(directorio + tipo_dato + 'vectoresCaracteristicasCluster' + data_type + str(anyo) + '.csv')
        dic_centroides = {'Centroide clase ' + str(i) : centroids[i] for i in range(number_of_clusters)}
        centroidsDf = pd.DataFrame.from_dict(dic_centroides, orient='index',columns = ['PC' + str(i+1) for i in range(len(centroids[0]))])
        centroidsDf.to_csv(directorio + '10_centroides' + data_type + str(anyo) + '.csv')
        
        print('\t Gráfica Kmeans')
        picture = plotclustersKmeans(principalComponents, number_of_clusters ,anyo, datos_nombres[tipo_dato][1])
        picture.savefig(graphics_path + 'kmeans'+ str(anyo) + data_type + '.png',bbox_inches='tight')
        
        print('\t Gráfica Kmeans 3D')
        image = plotKMeans3D(principalComponents, number_of_clusters, datos_nombres[tipo_dato][1])
        image.write_image(graphics_path + 'kmeans3D'+ str(anyo) + data_type + '.png')
        image.data = []
        image.layout = {}
        
        # print('\t Gráfica SOM')
        # picture = plotSOMclusters(principalComponents,number_of_clusters, anyo, data_type)
        # picture.savefig(graphics_path + 'SOM'+ str(anyo) + data_type + '.png')
        
        print('------' + tipo_dato + ' HECHO')
        plt.close('all')


print('YA ESTAAAAAA')
avisame()
