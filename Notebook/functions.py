import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import math
import psycopg2

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

def plotHistoricalShorelines(output, sitename):
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
    plt.savefig(f'Historical Shorelines/{sitename}.jpg')
    
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
    
def shorelinePlotly(output, sitename):
    DF = pd.DataFrame()
    
    for i in range(len(output['shorelines'])):
        DF = pd.concat([DF, pd.DataFrame({'date': output['dates'][i], 'Eastings': output['shorelines'][i][:,0], 'Northings': output['shorelines'][i][:,1]})], ignore_index=True)
    
    DF['date'] = DF['date'].astype(str).apply(lambda x: x[:10])
    
    fig = px.scatter(DF, x="Eastings", y="Northings", color="date", title=f"Shorelines for {sitename[:-3]} with {sitename[-2:]}")
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1
      )
    fig.update_xaxes(
        scaleanchor = "x",
        scaleratio = 1
      )
    fig.write_html(f'Historical Shorelines/{sitename}.html')
    fig.show()
    
def strToDate(dateStr):
    return datetime.strptime(dateStr, '%Y-%m-%d %H:%M:%S+00:00')

# def haversine_distance(lat1, lon1, lat2, lon2):
#     r = 6371
#     phi1 = np.radians(lat1)
#     phi2 = np.radians(lat2)
#     delta_phi = np.radians(lat2 — lat1)
#     delta_lambda = np.radians(lon2 — lon1)
    
#     a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
#     res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 — a)))
    
#     return np.round(res, 2)

def findDistance(north1, east1, north2, east2):
    return math.sqrt(math.pow(east1 - east2, 2) + math.pow(north1 - north2, 2))

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
    """ query data from the vendors table """
    
    conn = psycopg2.connect(url, sslmode='require')
    
    try:
        df = pd.read_sql(command, conn)
        
        if conn is not None:
            conn.close()
        
        return df
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        