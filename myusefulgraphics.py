# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:56:09 2022

@author: haffa
"""


import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn_som.som import SOM
from sklearn.cluster import KMeans
import pandas as pd
import plotly.express as px

#%% auxiliar functions

def elbowKmeans(pc, year, datatype):
    sum_of_squared_distances = []
    for k in range(1,15):
        kmeans = KMeans(n_clusters = k)
        kmeans.fit(pc)
        sum_of_squared_distances.append(kmeans.inertia_)
    fig = plt.figure()    
    plt.plot(range(1,15), sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k - ' +  str(year) + '-' + datatype)
    return fig

def matrixPCA(pca, year,columnas, datatype):
    
    fig = plt.figure(figsize = (20,20))
    ax = sns.heatmap(pca.components_,annot = False,
                     cmap = sns.color_palette("vlag", as_cmap=True),
                     yticklabels = [ "PCA"+str(x) for x in range(1,pca.n_components_+1)],
                     xticklabels = columnas, cbar=True,cbar_kws={"shrink": .4}
                     #cbar_kws={"orientation": "horizontal"}
                     )
    ax.set_xticklabels(ax.get_xticklabels(), fontsize = 15)
    ax.set_yticklabels(ax.get_yticklabels(),rotation = 0, fontsize = 15)
    ax.set_aspect("equal")
    plt.title('Matrix PC VS Characteristics - ' + str(year)+ '-' + datatype, fontsize = 22)

    return fig

def plotclustersKmeans(pc,nK, year, datatype):
    kmeans = KMeans(n_clusters = nK)
    kmeans.fit(pc)
    y_kmeans = kmeans.predict(pc)
    fig = plt.figure(figsize = (5,4))
    ax = fig.add_subplot(1,1,1)
    points = ax.scatter(pc[:, 0], pc[:, 1], c=y_kmeans, s=10, cmap='Accent')
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title(str(year) + ' scatter plot of K-means and centroids \n k = ' + str(nK)+ '-' + datatype)
    fig.colorbar(points)
    plt.show()
    return fig

def plotSOMclusters(principalComponents,nK, year, datatype):
    datos_som = SOM(m=nK, n=1, dim=len(principalComponents[0]))
    datos_som.fit(principalComponents)
    predicciones = datos_som.predict(principalComponents)
    fig = plt.figure(figsize = (10,8))
    ax = fig.add_subplot(1,1,1) 
    x = principalComponents[:,0]
    y = principalComponents[:,1]

    points = ax.scatter(x, y, c=predicciones, cmap = 'Accent', s = 10)

    plt.xlabel('PC1')
    plt.ylabel('PC2')
    plt.title(str(year) + ' scatter plot of SOM predictions - '+str(nK) +'clusters' + '-' + datatype)
    fig.colorbar(points)
    plt.show()
    return fig

def plotExplainedVariance(pca, year, datatype):
    
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Number of principal components', fontsize = 15)
    ax.set_ylabel('Explained Variance', fontsize = 15)
    ax.set_title('Explained variance VS Principal Components ' + str(year) + '\n' + datatype, fontsize = 20)
    plt.bar(x = range(1,1+ pca.n_components_), height=pca.explained_variance_ratio_)
    return fig

def plotKMeans3D(principalComponents, nK, datatype):

    kmeans = KMeans(n_clusters = nK)
    y_pred = kmeans.fit_predict(principalComponents)                          # Fitting the input data
    principalDf = pd.DataFrame(data = principalComponents,
                                columns = ['PC' + str(i) for i in range(len(principalComponents[0]))])
    principalDf['Cluster'] = y_pred
    finalDf = principalDf ## just for convenience
    
    finalDf['PC4'] = finalDf['PC4'] - min(finalDf['PC4'])
    finalDf['PC4'] = finalDf['PC4']**2
    finalDf['Cluster'] = finalDf['Cluster'].astype(str)
    #para poder usar la cuarta componente principal como color, le restamos el mínimo de dicha columna; eso nos lo llevará a no negativos y ya podremos usar el color
    
    fig = px.scatter_3d(
        finalDf, x='PC1', y='PC2', z='PC3', color='Cluster',
        size = 'PC4'
    )
    return fig

def plotDonut(edad_umvp,idiomas_umvp,sexo_umvp,edad_labels, idioma_labels, sexo_labels, anyo, nombre_datos):
    fig, ax = plt.subplots(figsize = (15,15))
    size = 0.3
    wedges1, texts1 = ax.pie(edad_umvp.values,
        radius=1,
        #colors=cmap(np.arange(len(edad_umvp))*6),
        wedgeprops=dict(width=size, edgecolor='w'))

    wedges2, texts2 = ax.pie(idiomas_umvp.values,
        radius=1-0.33,
        #colors=cmap(np.arange(len(idiomas_umvp))*0.5),
        wedgeprops=dict(width=size, edgecolor='w'))

    wedges3, texts3 = ax.pie(sexo_umvp.values, 
        radius=1-0.66, 
        #colors=cmap(np.arange(len(sexo_umvp))*4),
        wedgeprops=dict(width=size, edgecolor='w'))

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props, zorder=1, va="center")


    for i, p in enumerate(wedges1):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(edad_labels[i], xy=((1-0.1)*x, (1-0.1)*y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw,fontsize = 15)
        
    for i, p in enumerate(wedges2):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(idioma_labels[i], xy=((1-0.4)*x, (1-0.4)*y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw,fontsize = 15)
        
    for i, p in enumerate(wedges3):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(sexo_labels[i], xy=((1-0.7)*x, (1-0.7)*y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw, fontsize = 15)

    ax.set_aspect('equal')
    ax.set_title('Description of users ' + str(anyo) + ' ' + nombre_datos, fontsize = 22)
    return fig

