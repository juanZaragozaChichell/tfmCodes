import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import winsound


def avisame():
    duration = 2000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)


directorio = 'D:/Desktop/Estudios/UNIVERSIDAD/Investmat/TFM/codigos_final_2/'
graphics_path = directorio + 'graphics_clusters_pc_new/'

anyos = [2019, 2020]

datos_nombre = {
    '7_'   : ['Generales','BD2'],
    '9_1_' : ['Control','BD3.1'],
    '9_2_' : ['Estadisticas','BD3.2']
    }

for year in anyos:
    for num_dato in datos_nombre:
        print('Empieza ' + datos_nombre[num_dato][1] + ': ' + str(year))

        raw_data = pd.read_csv(directorio + num_dato + 'vectoresCaracteristicasCluster' 
                                                    + datos_nombre[num_dato][0] + str(year) +'.csv')
        raw_data['porcentaje medio viajes prohibidos'] = (raw_data['viajes prohibidos mayo'] +
                                                          raw_data['viajes prohibidos junio'] +
                                                          raw_data['viajes prohibidos octubre'] +
                                                          raw_data['viajes prohibidos noviembre'] +
                                                          raw_data['viajes prohibidos diciembre'])/5
        usuarios_mas_viajes_prohibidos = raw_data[raw_data['porcentaje medio viajes prohibidos']>=
                                                raw_data['porcentaje medio viajes prohibidos'].describe()['mean']]

        fig, ax = plt.subplots(figsize = (10,10))

        size = 0.3
        claves = raw_data['Cluster'].value_counts().keys().sort_values()
        vals1 = [raw_data['Cluster'].value_counts().loc[i] for i in claves]
        vals2 = [usuarios_mas_viajes_prohibidos['Cluster'].value_counts().loc[i] for i in claves]
        cmap = plt.colormaps["tab20c"]
        outer_colors = cmap(np.arange(3)*4)
        inner_colors = cmap([1, 2, 5, 6, 9, 10])

        ax.pie(vals1, radius=1, colors=outer_colors,
            autopct="%.1f%%",pctdistance=1-0.15, 
            labeldistance=1,textprops={'fontsize': 12},
            wedgeprops=dict(width=size, edgecolor='w'))

        ax.pie(vals2, radius=1-0.33, colors=outer_colors,
            autopct="%.1f%%",pctdistance=1-0.3, 
            labeldistance=1-0.33,textprops={'fontsize': 12},
            wedgeprops=dict(width=size, edgecolor='w'))
        plt.legend(title = 'Number of cluster -', loc = 1)
        ax.legend(claves)
        ax.set(aspect="equal", 
            title= 'Proportion of elements belonging to each cluster\n' + datos_nombre[num_dato][1] + '\t' + str(year))
        fig.savefig(graphics_path + 'donutPorcentajeClusters' + datos_nombre[num_dato][1] + str(year) + '.png',bbox_inches='tight')
        plt.close()
        print('\t Terminado ' + datos_nombre[num_dato][1] + ': ' + str(year))

avisame()