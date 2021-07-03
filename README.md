# Investigating-Coastal-Changes-Project
A program developed for a school research project, as part of Nanyang Technological University Undergraduate Research Experience on CAmpus (URECA).

## Objective
This research project aims to use remote sensing and satellite technology to obtain satellite images to analyse the shorelines of coastal areas. In this project through the satellite images, studies were conducted on various parts of Asia such as India and Thailand, to analyse the impact of recent natural events and rising sea levels on the shorelines of these areas.

## Implementation
<img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124359852-4e5f4a80-dc59-11eb-9257-13c7a1f6ffff.png> <img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124359884-6afb8280-dc59-11eb-8eee-c6445d7b17fb.png> <img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124359903-81094300-dc59-11eb-8b34-520fceffe6db.png> <img height="250" alt="image" src=https://user-images.githubusercontent.com/48685014/124360021-08ef4d00-dc5a-11eb-8d99-679761c985c3.png>

This program is built using Python programming language, and it builds on the features of [CoastSat](https://www.sciencedirect.com/science/article/pii/S1364815219300490) by Kilian Vos, a tool also built with Python that can obtain the satellite images with Google Earth Engine and perform image segmentation to trace the shorelines based on the extracted images.

* Through this program, the user can enter the location (in latitude, longitude pairs), the period of interest and the selected satellite in order to extract the images.
* After extraction, select good quality images for analysis and use CoastSat's pre-trained image segmentation model to trace the shorelines for each image.
* Shorelines data are stored into a PostgreSQL database for future analysis and reference.
* With available shorelines data, perform analysis of shoreline changes at the locations using CoastSat's transects feature.

**Database:** PostgreSQL on Heroku

## Dependencies
Ensure the program has the CoastSat's dependencies based on the program [repository](https://github.com/kvos/CoastSat).  

> All Python dependencies are in the requirements.txt file.  
`pip install -r requirements.txt`

## Running the Program
Run the following steps to ensure CoastSat dependencies.

1. Go to root directory and download the required environment.  
> Create CoastSat environment  
`conda env create -f environment.yml -n coastsat`

2. Activate and use environment  
> Activate environment  
`conda activate coastsat`

3. Open Jupyter Notebook  
`jupyter notebook`

4. Deactivate environment  
`conda deactivate`

## Potential Error
[Matplotlib Visualisation Error](https://stackoverflow.com/questions/61171307/jupyter-notebook-shows-error-message-for-matplotlib-bad-key-text-kerning-factor)
