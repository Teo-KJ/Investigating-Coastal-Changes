# Investigating-Coastal-Changes
A program developed for a school research project, as part of Nanyang Technological University's Undergraduate Research Experience on Campus (URECA).

## Objective
This research project aims to use remote sensing and satellite technology to obtain satellite images to analyse the shorelines of coastal areas. In this project through the satellite images, studies were conducted on various parts of Asia such as India and Thailand, to analyse the impact of recent natural events and rising sea levels on the shorelines of these areas.

## Implementation
<img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124359852-4e5f4a80-dc59-11eb-9257-13c7a1f6ffff.png> <img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124359884-6afb8280-dc59-11eb-8eee-c6445d7b17fb.png> <img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124359903-81094300-dc59-11eb-8b34-520fceffe6db.png> <img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124360021-08ef4d00-dc5a-11eb-8d99-679761c985c3.png>

This program is built using the Python programming language, and it builds on the features of [CoastSat](https://www.sciencedirect.com/science/article/pii/S1364815219300490), a tool also developed using Python. CoastSat is able to obtain the satellite images with Google Earth Engine and perform image segmentation to trace the shorelines based on the extracted images.

* Through this program, the user can enter the location (in latitude, longitude pairs), the period of interest (start and end date) and the selected satellite (e.g. Landsat 5, Sentinel-2 and etc.) in order to extract the images.
* After extraction, the user can manually select good quality images for analysis and use CoastSat's pre-trained image segmentation model to trace the shorelines for each image.
* Shorelines data are then stored into a PostgreSQL database for future analysis and reference.
* With available shorelines data, perform analysis of shoreline changes at the locations using CoastSat's transects feature.

**Database:** PostgreSQL on Heroku

## Dependencies
Ensure the program has the CoastSat's dependencies based on the original [repository](https://github.com/kvos/CoastSat).  

> All Python dependencies are in the requirements.txt file.  
`pip install -r requirements.txt`

## Running the Program
Run the following steps to ensure CoastSat dependencies.

1. Go to root directory and download the required environment.  
> Create CoastSat environment  
`conda env create -f environment.yml -n coastsat`

2. When environment is available, activate and use environment  
> Activate environment  
`conda activate coastsat`

3. Open Jupyter Notebook  
`jupyter notebook`

4. Deactivate environment  
`conda deactivate`

## Potential Error
[Matplotlib Visualisation Error](https://stackoverflow.com/questions/61171307/jupyter-notebook-shows-error-message-for-matplotlib-bad-key-text-kerning-factor)
