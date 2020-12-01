def settings(inputs):
    settings = { 
        # general parameters:
        'cloud_thresh': 0.5,        # threshold on maximum cloud cover
        'output_epsg': 3857,        # epsg code of spatial reference system desired for the output   
        # quality control:
        'check_detection': True,    # if True, shows each shoreline detection to the user for validation
        'save_figure': True,        # if True, saves a figure showing the mapped shoreline for each image
        # add the inputs defined previously
        'inputs': inputs,
        # [ONLY FOR ADVANCED USERS] shoreline detection parameters:
        'min_beach_area': 4500,     # minimum area (in metres^2) for an object to be labelled as a beach
        'buffer_size': 150,         # radius (in metres) of the buffer around sandy pixels considered in the shoreline detection
        'min_length_sl': 200,       # minimum length (in metres) of shoreline perimeter to be valid
        'cloud_mask_issue': False,  # switch this parameter to True if sand pixels are masked (in black) on many images  
        'sand_color': 'default',    # 'default', 'dark' (for grey/black sand beaches) or 'bright' (for white sand beaches)
    }
    return settings

def switchCoordinates(coordinates):
    for i in coordinates[0]:
        temp = i[0]
        i[0] = i[1]
        i[1] = temp

    return coordinates
