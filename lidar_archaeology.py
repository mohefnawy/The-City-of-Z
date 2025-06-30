# Python script for LiDAR analysis in archaeology

# This script outlines a general workflow for processing LiDAR data for archaeological purposes.
# It uses common Python libraries for geospatial data handling. 
# You will need to install these libraries if you don't have them:
# pip install laspy numpy matplotlib rasterio

import laspy
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.transform import from_origin

print("LiDAR analysis script for archaeological detection")
print("---------------------------------------------------")

def process_lidar_for_archaeology(lidar_file_path, output_dem_path="output_dem.tif", output_dtm_path="output_dtm.tif"):
    """
    Processes LiDAR data to generate Digital Elevation Models (DEM) and Digital Terrain Models (DTM),
    which are crucial for archaeological prospection.

    Args:
        lidar_file_path (str): Path to the input LiDAR file (e.g., .las, .laz).
        output_dem_path (str): Path to save the output Digital Elevation Model (DEM).
        output_dtm_path (str): Path to save the output Digital Terrain Model (DTM).
    """
    try:
        # 1. Read LiDAR data
        print(f"Reading LiDAR file: {lidar_file_path}")
        with laspy.read(lidar_file_path) as las:
            points = np.vstack((las.x, las.y, las.z)).transpose()
            # Classify ground points (assuming LAS file has classification tags)
            # Common classification for ground is 2
            ground_points = points[las.classification == 2]
            non_ground_points = points[las.classification != 2]

        print(f"Total points: {len(points)}")
        print(f"Ground points: {len(ground_points)}")

        # 2. Create Digital Elevation Model (DEM) - includes all features (vegetation, buildings, ground)
        # For simplicity, we'll use a basic gridding approach. For more advanced DEM creation,
        # consider libraries like `pyntcloud` or `PDAL` for interpolation.
        print("Creating Digital Elevation Model (DEM)...")
        # Determine grid resolution (example: 1 meter resolution)
        resolution = 1.0
        min_x, min_y = np.min(points[:, 0]), np.min(points[:, 1])
        max_x, max_y = np.max(points[:, 0]), np.max(points[:, 1])

        cols = int(np.ceil((max_x - min_x) / resolution))
        rows = int(np.ceil((max_y - min_y) / resolution))

        dem = np.full((rows, cols), np.nan) # Initialize with NaN

        # Simple gridding: assign average Z to each cell
        # This is a very basic approach; for real applications, use interpolation methods.
        for p in points:
            col = int((p[0] - min_x) / resolution)
            row = int((max_y - p[1]) / resolution) # Invert row for top-left origin
            if 0 <= row < rows and 0 <= col < cols:
                if np.isnan(dem[row, col]):
                    dem[row, col] = p[2]
                else:
                    dem[row, col] = (dem[row, col] + p[2]) / 2 # Average if multiple points fall in cell

        # 3. Create Digital Terrain Model (DTM) - ground surface only
        print("Creating Digital Terrain Model (DTM)...")
        dtm = np.full((rows, cols), np.nan)
        for p in ground_points:
            col = int((p[0] - min_x) / resolution)
            row = int((max_y - p[1]) / resolution)
            if 0 <= row < rows and 0 <= col < cols:
                if np.isnan(dtm[row, col]):
                    dtm[row, col] = p[2]
                else:
                    dtm[row, col] = (dtm[row, col] + p[2]) / 2

        # 4. Save DEM and DTM as GeoTIFF files
        transform = from_origin(min_x, max_y, resolution, resolution)

        with rasterio.open(
            output_dem_path,
            'w',
            driver='GTiff',
            height=rows,
            width=cols,
            count=1,
            dtype=dem.dtype,
            crs='+proj=latlong',
            transform=transform,
        ) as dst:
            dst.write(dem, 1)
        print(f"DEM saved to: {output_dem_path}")

        with rasterio.open(
            output_dtm_path,
            'w',
            driver='GTiff',
            height=rows,
            width=cols,
            count=1,
            dtype=dtm.dtype,
            crs='+proj=latlong',
            transform=transform,
        ) as dst:
            dst.write(dtm, 1)
        print(f"DTM saved to: {output_dtm_path}")

        # 5. Optional: Visualization (example using matplotlib)
        print("Generating visualizations...")
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        im1 = axes[0].imshow(dem, cmap='terrain', origin='upper',
                             extent=[min_x, max_x, min_y, max_y])
        axes[0].set_title('Digital Elevation Model (DEM)')
        fig.colorbar(im1, ax=axes[0], label='Elevation (m)')

        im2 = axes[1].imshow(dtm, cmap='terrain', origin='upper',
                             extent=[min_x, max_x, min_y, max_y])
        axes[1].set_title('Digital Terrain Model (DTM)')
        fig.colorbar(im2, ax=axes[1], label='Elevation (m)')

        plt.tight_layout()
        plt.savefig("lidar_dem_dtm_visualization.png")
        print("Visualization saved to: lidar_dem_dtm_visualization.png")

        print("LiDAR processing complete.")

    except FileNotFoundError:
        print(f"Error: LiDAR file not found at {lidar_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- How to use this script ---
# 1. Replace 'path/to/your/lidar_data.las' with the actual path to your LiDAR file.
# 2. Ensure you have the necessary Python libraries installed: laspy, numpy, matplotlib, rasterio.
# 3. Run the script: python lidar_archaeology.py

# Example usage (uncomment and modify with your file path):
# process_lidar_for_archaeology('path/to/your/lidar_data.las')

print("LiDAR script created. This script provides a basic framework. For real-world archaeological applications, you might need more sophisticated interpolation methods, filtering, and analysis techniques (e.g., hillshading, slope analysis, curvature analysis on DTMs to highlight subtle features).")
print("Remember to replace 'path/to/your/lidar_data.las' with your actual LiDAR data file path and install the required libraries.")


