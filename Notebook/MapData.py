import os
from functions import *

class MapData:
    
    def __init__(self, name, coordinates, period, satellite):
        self.name = name
        self.coordinates = coordinates
        self.period = period
        self.satellite = satellite

    def getData(self):
        # swtich the coordinates placement
        polygon = switchCoordinates(self.coordinates)
        
        # satellite missions
        sat_list = [self.satellite]
        
        # name of the site
        sitename = f'{self.name}' + ' ' + str(sat_list[0])
        
        # directory where the data will be stored
        filepath = os.path.join(os.getcwd(), 'extracted data')
        
        # put all the inputs into a dictionnary
        inputs = {'polygon': polygon, 'dates': self.period, 'sat_list': sat_list, 'sitename': sitename, 'filepath':filepath}
        
        return inputs
