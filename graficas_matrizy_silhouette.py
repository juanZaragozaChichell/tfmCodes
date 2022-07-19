# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 19:36:59 2022

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
        
        if tipo_dato == '5_':
            columnas = ['Commutes May-December', 'Weekly commutes', 'Monday commutes', 'Tuesday commutes', 'Wednesday commutes', 'Thursday commmutes', 'Friday commutes', 'Saturday commutes', 'Sunday commutes', 'May commutes',
                        'June commutes', 'July commutes', 'August commutes', 'September commutes', 'October commutes', 'November commutes', 'December commutes']
        elif tipo_dato == '7_':
            columnas = ['Commutes May-December', 'Weekly commutes', 'Monday commutes', 'Tuesday commutes', 'Wednesday commutes', 'Thursday commmutes', 'Friday commutes', 'Saturday commutes', 'Sunday commutes', 'May commutes',
                        'June commutes', 'July commutes', 'August commutes', 'September commutes', 'October commutes', 'November commutes', 'December commutes',
                        'Postal code', 'Gender', 'Age', 'Language', 'Commutes during curfews May', 'Commutes during curfews June',
                        'Commutes during curfews October','Commutes during curfews November','Commutes during curfews December',
                        'Neighborhood with most departures 1', 'Neighborhood with most departures 2', 'Neighborhood with most arrivals 1', 'Neighborhood with most arrivals 2']
        elif tipo_dato == '9_1_':
            columnas = ['Commutes May-December', 'Weekly commutes', 'Monday commutes', 'Tuesday commutes', 'Wednesday commutes', 'Thursday commmutes', 'Friday commutes', 'Saturday commutes', 'Sunday commutes', 'May commutes',
                        'June commutes', 'July commutes', 'August commutes', 'September commutes', 'October commutes', 'November commutes', 'December commutes',
                        'Postal code', 'Gender', 'Age', 'Language', 'Commutes during curfews May', 'Commutes during curfews June',
                        'Commutes during curfews October','Commutes during curfews November','Commutes during curfews December',
                        'Neighborhood with most departures 1', 'Neighborhood with most departures 2', 'Neighborhood with most arrivals 1', 'Neighborhood with most arrivals 2',
                        'Y1','Y2','Y3','Y4','Y5', 'Y6', 'Y7', 'Y8', 'Mean duration time', 'Std. deviation time', 'Min. duration time', '25% duration time', '50% duration time', '75% duration time', 'Max. duration time']
        elif tipo_dato == '9_2_':
            columnas = ['Commutes May-December', 'Weekly commutes', 'Monday commutes', 'Tuesday commutes', 'Wednesday commutes', 'Thursday commmutes', 'Friday commutes', 'Saturday commutes', 'Sunday commutes', 'May commutes',
                        'June commutes', 'July commutes', 'August commutes', 'September commutes', 'October commutes', 'November commutes', 'December commutes',
                        'Postal code', 'Gender', 'Age', 'Language', 'Commutes during curfews May', 'Commutes during curfews June',
                        'Commutes during curfews October','Commutes during curfews November','Commutes during curfews December',
                        'Neighborhood with most departures 1', 'Neighborhood with most departures 2', 'Neighborhood with most arrivals 1', 'Neighborhood with most arrivals 2',
                        'Mean departure time', 'Std. departure time', 'Min. departure time', '25% duration time', '50% duration time', '75% duration time', 'Max. duration time',
                        'Mean duration time', 'Std. deviation time', 'Min. duration time', '25% duration time', '50% duration time', '75% duration time', 'Max. duration time']
        
        
        data_type = datos_nombres[tipo_dato][0]
        print('\t Empieza ' + data_type)
        datos = pd.read_csv(directorio + tipo_dato + 'vectoresCaracteristicas' + data_type + str(anyo) + '.csv')
        
        matriz_datos = datos.drop(columns = ['abonado'])
        #columnas = list(matriz_datos.keys())
        matriz_datos = matriz_datos.values
        matriz_datos = StandardScaler().fit_transform(matriz_datos)
        ## PCA evaluation
        print('\t Evaluación PCA')
        pca = PCA(n_components = 0.85)
        principalComponents = pca.fit_transform(matriz_datos)
        ## matrix of PC and features
        print('\t Matriz PCA calculandose')
        picture = matrixPCA(pca, anyo ,columnas, datos_nombres[tipo_dato][1])
        picture.savefig(graphics_path + 'matrixPCA'+ str(anyo) + data_type + '.png', bbox_inches='tight')
        
        # #silhouette para las componentes principales
        # print('\t Haciendo silhouette plot componentes principales')
        # scores = []
        # for k in range(2,15):
        #     kmeans = KMeans(n_clusters = k)
        #     y_pred = kmeans.fit_predict(principalComponents)
        #     scores.append(silhouette_score(principalComponents, kmeans.labels_))
        
        # fig = plt.figure()    
        # plt.plot(range(2,15), scores, 'bx-')
        # plt.xlabel('Number of clusters')
        # plt.ylabel('Silhouette score')
        # plt.title('Principal Components \n Silhouete score Vs number of clusters ' +  str(anyo) + '-' + datos_nombres[tipo_dato][1])
        # fig.savefig(graphics_path + 'silhouette'+ str(anyo) + data_type + 'PrincipalComponents.png')
        
        plt.close('all')


print('YA ESTAAAAAA')
avisame()
