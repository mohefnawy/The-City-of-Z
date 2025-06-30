# Google Earth Engine Python script for archaeological analysis

import ee

# Initialize the Earth Engine API
# You need to authenticate and initialize the API before running this script.
# Run `earthengine authenticate` in your terminal and follow the instructions.
# ee.Initialize()

# --- User-definable parameters --- 

# Define a region of interest (ROI) for analysis.
# You can define a polygon, a rectangle, or a point with a buffer.
# Example: A rectangle over a potential area in the Amazon (replace with your area of interest)
# Coordinates are [west, south, east, north]
roi = ee.Geometry.Rectangle([-55.0, -10.0, -50.0, -5.0]) 

# You can also define a point and buffer around it:
# point = ee.Geometry.Point(-52.0, -7.0) # Example: Longitude, Latitude
# roi = point.buffer(10000) # 10 km buffer

# Define a date range for satellite imagery
start_date = '2020-01-01'
end_date = '2023-12-31'

# --- Image Collection and Preprocessing --- 

# Load Sentinel-2 surface reflectance data.
# Sentinel-2 is good for archaeological analysis due to its spatial resolution (10m) and spectral bands.
collection = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterBounds(roi) \
    .filterDate(start_date, end_date) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) # Filter out cloudy images

# Select relevant bands for visualization and analysis.
# B4: Red, B3: Green, B2: Blue (for true color composite)
# B8: Near-Infrared (useful for vegetation analysis, which can indicate archaeological features)
image = collection.median().clip(roi) # Take the median composite to reduce noise and clouds

# --- Visualization Parameters --- 

# True color visualization
true_color_vis = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2']
}

# False color infrared (NIR, Red, Green) for vegetation analysis
false_color_vis = {
    'min': 0,
    'max': 3000,
    'bands': ['B8', 'B4', 'B3']
}

# --- Add layers to the map (for use in GEE Code Editor) --- 

# These lines are for use within the Google Earth Engine Code Editor (JavaScript API).
# If you are running this script locally, you would typically export the image or process it further.
# For local visualization, you might use libraries like `folium` or `matplotlib` with `ee.data.getTileUrl`.

# print('Add true color composite to map:')
# ee.mapclient.addToMap(image, true_color_vis, 'True Color Composite')

# print('Add false color infrared composite to map:')
# ee.mapclient.addToMap(image, false_color_vis, 'False Color Infrared')

# --- Example Analysis: NDVI (Normalized Difference Vegetation Index) --- 

# NDVI is often used to highlight differences in vegetation health, which can sometimes indicate buried structures.
ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')

ndvi_vis = {
    'min': -0.2,
    'max': 0.7,
    'palette': ['red', 'yellow', 'green']
}

# print('Add NDVI to map:')
# ee.mapclient.addToMap(ndvi, ndvi_vis, 'NDVI')

# --- Exporting Results (for local script execution) --- 

# To export the image to Google Drive or Google Cloud Storage, uncomment and modify the following:
# export_image_params = {
#     'image': image,
#     'description': 'archaeological_analysis_image',
#     'scale': 10, # Resolution in meters per pixel
#     'region': roi.getInfo()['coordinates'],
#     'maxPixels': 1e10
# }
# task = ee.batch.Export.image.toDrive(**export_image_params)
# task.start()
# print(f'Export task started: {task.id}')

# You can also get a thumbnail URL for quick visualization (requires ee.Initialize() to be uncommented):
# thumbnail_url = image.getThumbUrl(true_color_vis)
# print(f'Thumbnail URL: {thumbnail_url}')

print('Google Earth Engine script created. Remember to install the earthengine-api (`pip install earthengine-api`) and authenticate (`earthengine authenticate`) to run this locally.')
print('The script includes commented-out sections for map visualization (for GEE Code Editor) and export (for local execution).')
print('You will need to uncomment `ee.Initialize()` and the relevant `ee.mapclient.addToMap` or `ee.batch.Export.image.toDrive` lines depending on your use case.')


