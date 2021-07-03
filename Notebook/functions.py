import os
import pickle
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import math
import psycopg2

# CoastSat
from coastsat import SDS_download, SDS_preprocess, SDS_shoreline, SDS_tools, SDS_transects, SDS_islands

def settings(inputs):
    settings = { 
        # general parameters:
        'cloud_thresh': 0.5,        # threshold on maximum cloud cover
        'output_epsg': 3857,        # epsg code of spatial reference system desired for the output   

        # quality control:
        'check_detection': True,    # if True, shows each shoreline detection to the user for validation
        'adjust_detection': True,  # if True, allows user to adjust the postion of each shoreline by changing the threhold
        'save_figure': True,        # if True, saves a figure showing the mapped shoreline for each image

        # [ONLY FOR ADVANCED USERS] shoreline detection parameters:
        'min_beach_area': 4500,     # minimum area (in metres^2) for an object to be labelled as a beach
        'buffer_size': 150,         # radius (in metres) for buffer around sandy pixels considered in the shoreline detection
        'min_length_sl': 200,       # minimum length (in metres) of shoreline perimeter to be valid
        'cloud_mask_issue': False,  # switch this parameter to True if sand pixels are masked (in black) on many images  
        'sand_color': 'default',    # 'default', 'dark' (for grey/black sand beaches) or 'bright' (for white sand beaches)

        # add the inputs defined previously
        'inputs': inputs
        }
    return settings

def switchCoordinates(coordinates):
    for i in coordinates[0]:
        temp = i[0]
        i[0] = i[1]
        i[1] = temp

    return coordinates

def plotHistoricalShorelines(output, sitename, inputSettings):
    fig = plt.figure(figsize=[15,8])

    plt.axis('equal')
    plt.xlabel('Eastings')
    plt.ylabel('Northings')
    plt.grid(linestyle=':', color='0.5')

    for i in range(len(output['shorelines'])):
        sl = output['shorelines'][i]
        date = output['dates'][i]
        plt.plot(sl[:,0], sl[:,1], '.', label=date.strftime('%d-%m-%Y'))
    
    plt.legend();
    plt.show()
    
    filepath = inputSettings['filepath']
    site = inputSettings['sitename']
    
    plt.savefig(f'{filepath}/{site}/{sitename}.jpg')
    
def zoomInShorelines(output):
    fig = plt.figure(figsize=[15,8])

    plt.axis('equal')
    plt.xlabel('Eastings')
    plt.ylabel('Northings')
    plt.grid(linestyle=':', color='0.5')

    for i in range(len(output['shorelines'])):
        sl = output['shorelines'][i]
        date = output['dates'][i]
        plt.margins(x=0, y=-0.25)
        plt.plot(sl[:,0], sl[:,1], '.', label=date.strftime('%d-%m-%Y'))
    
    plt.legend();
    plt.show()
    
def shorelinePlotly(output, sitename, inputSettings):
    DF = pd.DataFrame()
    
    for i in range(len(output['shorelines'])):
        DF = pd.concat([DF, 
                        pd.DataFrame({'dates': output['dates'][i], 'Eastings': output['shorelines'][i][:,0], 'Northings': output['shorelines'][i][:,1]})], 
                       ignore_index=True)
    
    DF['dates'] = DF['dates'].astype(str).apply(lambda x: x[:10])
    
    fig = px.scatter(DF, x="Eastings", y="Northings", color="dates", 
                     text=DF.index,
                     title=f"Shorelines for {sitename[:-3]} with {sitename[-2:]}")
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1
      )
    fig.update_xaxes(
        scaleanchor = "x",
        scaleratio = 1
      )
    
    filepath = inputSettings['filepath']
    site = inputSettings['sitename']
    
    fig.write_html(f'{filepath}/{site}/{sitename}.html')
    fig.show()
    
def strToDate(dateStr):
    return datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S')

def strToDateWithGMT(dateStr):
    return datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S+00:00')

def setUpDB(command, url):
    """ create tables in the PostgreSQL database"""
    
    try:        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(url, sslmode='require')
        cur = conn.cursor()
        
        # create table one by one
        cur.execute(command)
        
        # close communication with the PostgreSQL database server
        cur.close()
        
        # commit the changes
        conn.commit()
        conn.close()
        print('done')
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def getData(command, url):    
    conn = psycopg2.connect(url, sslmode='require')
    
    try:
        df = pd.read_sql(command, conn)
        
        if conn is not None:
            conn.close()
        
        return df
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
def getShorelinesFromSql(data):
    data = data.replace(' ', '')
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.split(',')
    
    mainlist = []

    for i in range(0, len(data), 2):
        mainlist.append([float(data[i]), float(data[i+1])])

    return np.asarray(mainlist, dtype=np.float64)

def enterDataFromJSONtoSql(dataframe, url):
    for index, row in dataframe.iterrows():
        command = (
            '''INSERT INTO shorelineData VALUES ('%s', '%s', '%s', '%s', %f, %f, %d, '%s');''' 
            % (row.location, row.dates, row.shorelines, row.filename, row.cloud_cover, row.geoaccuracy, row.idx, row.satname)
            )

        setUpDB(command, url)

def removeExcessDateStr(url):
    command = (
        '''
        UPDATE shorelineData
        SET dates = LEFT(dates, LENGTH(dates)-6)
        WHERE LENGTH(dates)>19;
        '''
        )

    setUpDB(command, url)
    
def getTransacts(inputs, output, along_dist = 25):        
    matplotlib.use('Qt5Agg')
    transects = SDS_transects.draw_transects(output, settings(inputs))
    
    settingsOfInputs = settings(inputs)
    settingsOfInputs['along_dist'] = along_dist
    
    cross_distance = SDS_transects.compute_intersection(output, transects, settingsOfInputs)
    
    return transects, cross_distance
    
def visualiseTransacts(cross_distance, output, sitename, inputSettings):
    fig = plt.figure(figsize=[15,8], tight_layout=True)
    gs = gridspec.GridSpec(len(cross_distance),1)
    gs.update(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.05)
    
    for i,key in enumerate(cross_distance.keys()):
        
        if np.all(np.isnan(cross_distance[key])):
            continue
            
        ax = fig.add_subplot(gs[i,0])
        ax.grid(linestyle=':', color='0.5')
        ax.set_ylim([-50,50])
        ax.plot(output['dates'], cross_distance[key]- np.nanmedian(cross_distance[key]), '-o', ms=6, mfc='w')
        ax.set_ylabel('distance [m]', fontsize=12)
        ax.text(0.5,0.95, key, bbox=dict(boxstyle="square", ec='k',fc='w'), ha='center',
                va='top', transform=ax.transAxes, fontsize=14)
        
    filepath = inputSettings['filepath']
    site = inputSettings['sitename']
    
    plt.savefig(f'{filepath}/{site}/{sitename} Shoreline Changes.jpg')
        
def plotLabelledTransacts(transects, output, sitename, inputSettings):
    fig = plt.figure(figsize=[15,8], tight_layout=True)
    plt.axis('equal')
    plt.xlabel('Eastings')
    plt.ylabel('Northings')
    plt.grid(linestyle=':', color='0.5')

    for i in range(len(output['shorelines'])):
        sl = output['shorelines'][i]
        date = output['dates'][i]
        plt.plot(sl[:,0], sl[:,1], '.', label=date.strftime('%d-%m-%Y'))

    for i,key in enumerate(list(transects.keys())):
        plt.plot(transects[key][0,0],transects[key][0,1], 'bo', ms=5)
        plt.plot(transects[key][:,0],transects[key][:,1],'k-',lw=1)
        plt.text(transects[key][0,0]-100, transects[key][0,1]+100, key,
                    va='center', ha='right', bbox=dict(boxstyle="square", ec='k',fc='w'))
        
    filepath = inputSettings['filepath']
    site = inputSettings['sitename']
        
    plt.savefig(f'{filepath}/{site}/{sitename} Transacts.jpg')
    
def getDataByLocation(databaseURL, dataframe, locationCounter):
    query = f"SELECT * FROM shorelineData WHERE location = '{dataframe.location.values[locationCounter-1]}' ORDER BY dates;"
    dataframe = getData(query, databaseURL)
    dataframe['dates'] = dataframe['dates'].apply(lambda x: strToDate(x))
    dataframe['shorelines'] = dataframe['shorelines'].apply(lambda x: getShorelinesFromSql(x))

    query = f"SELECT * FROM polygonData WHERE location = '{dataframe.location.values[locationCounter-1]}';"
    polygonData = getData(query, databaseURL)
    polygon = getShorelinesFromSql(polygonData['polygon'][0]).tolist()
    folderName = polygonData['folder_name'][0]
    
    return dataframe, polygon, folderName