
# 🌍 LiDAR + Satellite Search for Amazon Lost Cities

This project combines LiDAR dataset discovery (via OpenTopography API), satellite imagery (via Sentinel-2), and Google Earth Engine (GEE) tools to explore and analyze potential lost city sites in the Amazon Basin.

---

## 🔧 Requirements

Install the required Python packages:

```bash
pip install geopandas folium requests sentinelsat
```

---

## 📍 Amazon Basin LiDAR Dataset Discovery (OpenTopography)

```python
import requests
import geopandas as gpd
import folium
from shapely.geometry import box

# Define bounding box of Amazon Basin
bbox = {
    "min_lon": -75.0,
    "max_lon": -58.0,
    "min_lat": -15.0,
    "max_lat": 5.0
}

# Build bounding box polygon
bounding_box = box(bbox["min_lon"], bbox["min_lat"], bbox["max_lon"], bbox["max_lat"])
gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[bounding_box])

# Create map
m = folium.Map(location=[-5.0, -67.0], zoom_start=5)
folium.GeoJson(gdf).add_to(m)

# --- OpenTopography API search ---
def search_opentopo_lidar(bbox):
    url = "https://portal.opentopography.org/API/findDatasets"
    params = {
        "south": bbox["min_lat"],
        "north": bbox["max_lat"],
        "west": bbox["min_lon"],
        "east": bbox["max_lon"],
        "outputFormat": "json"
    }
    print("🔍 Searching OpenTopography...")
    response = requests.get(url, params=params)
    data = response.json()
    if 'Datasets' in data:
        for ds in data['Datasets']:
            print(f"🛰️  {ds['name']}")
            print(f"    → {ds['description']}")
            print(f"    📍 Location: {ds['boundingBox']}")
            print(f"    🔗 URL: {ds['url']}
")
    else:
        print("No datasets found.")

# Run the OpenTopography search
search_opentopo_lidar(bbox)

# Save map
m.save("amazon_lidar_map.html")
print("🗺️  Map saved to amazon_lidar_map.html")
```

---

## 🛰️ Sentinel-2 NDVI Overlay Using Python

```python
from sentinelsat import SentinelAPI, geojson_to_wkt
from datetime import date
import json

# Replace with your Copernicus credentials
api = SentinelAPI('user', 'password', 'https://scihub.copernicus.eu/dhus')

# Define GeoJSON AOI from bounding box
aoi_geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [-75.0, -15.0],
                [-75.0, 5.0],
                [-58.0, 5.0],
                [-58.0, -15.0],
                [-75.0, -15.0]
            ]]
        }
    }]
}

# Convert to WKT
footprint = geojson_to_wkt(aoi_geojson)

# Search Sentinel-2 L2A data
products = api.query(footprint,
                     date=('20240101', date.today().strftime('%Y%m%d')),
                     platformname='Sentinel-2',
                     processinglevel='Level-2A',
                     cloudcoverpercentage=(0, 20))

print(f"Found {len(products)} products")
```

---

## 🌳 Google Earth Engine: Canopy Gap and Terrain Analysis (JS Code)

```javascript
// Paste into code.earthengine.google.com

var aoi = ee.Geometry.Rectangle([-75, -15, -58, 5]);

// Load Sentinel-2 imagery
var s2 = ee.ImageCollection('COPERNICUS/S2_SR')
  .filterBounds(aoi)
  .filterDate('2024-01-01', '2024-12-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .median();

// Compute NDVI
var ndvi = s2.normalizedDifference(['B8', 'B4']);
Map.centerObject(aoi, 6);
Map.addLayer(ndvi, {min: 0, max: 1, palette: ['white', 'green']}, 'NDVI');

// Load SRTM terrain
var srtm = ee.Image('USGS/SRTMGL1_003');
var slope = ee.Terrain.slope(srtm);
Map.addLayer(slope, {min: 0, max: 60}, 'Slope');
```

---

## 📁 Outputs

- `amazon_lidar_map.html` – Interactive map showing Amazon LiDAR search region
- NDVI visualizations and Sentinel download search
- GEE script for further terrain/vegetation processing

---

## 💬 Notes

- OpenTopography requires no login for API access.
- SentinelHub (Copernicus) requires a free account.
- Google Earth Engine requires registration but supports powerful cloud-based analysis.

---

## 🧠 Credits

Project inspired by the OpenAI-to-Z Challenge and archaeological interest in El Dorado / City of Z.
