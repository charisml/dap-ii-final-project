import folium
from folium.plugins import MarkerCluster
import geopandas as gpd
import pandas as pd
from shapely import wkt
import os

# Load crash data
crashes_gdf = gpd.read_file(r'C:\Users\User\Documents\GitHub\dap-ii-final-project\Data\crashes_gdf.csv')

# Ensure geometry is properly set
crashes_gdf['geometry'] = crashes_gdf['LOCATION'].apply(wkt.loads)
crashes_gdf = gpd.GeoDataFrame(crashes_gdf, geometry='geometry')
crashes_gdf.set_crs(epsg=3435, inplace=True)

# Process data in chunks to improve run time
chunk_size = 100000
total_rows = len(crashes_gdf)
num_chunks = (total_rows + chunk_size - 1) // chunk_size
processed_chunks = []

for i in range(num_chunks):
    start = i * chunk_size
    end = min(start + chunk_size, total_rows)
    chunk = crashes_gdf.iloc[start:end]
    processed_chunks.append(chunk)

# Combine chunks into a single GeoDataFrame
processed_data = gpd.GeoDataFrame(pd.concat(processed_chunks, ignore_index=True))

# Load ward boundaries geojson
ward_boundaries = gpd.read_file(r'C:\Users\User\OneDrive - The University of Chicago\4_DAP-2\Final Project Data\ward_boundaries.geojson')
ward_boundaries = ward_boundaries.to_crs(epsg=3435)

# Ensure processed_data['YEAR'] is a string for filtering
processed_data['YEAR'] = processed_data['YEAR'].astype(str)

# Define the output directory for maps
output_dir = os.path.join(os.getcwd(), "maps")
os.makedirs(output_dir, exist_ok=True)

# Generate maps for each year from 2020 to 2024
years = ['2020', '2021', '2022', '2023', '2024']
for year in years:
    filtered_data = processed_data[processed_data['YEAR'] == year]
    
    # Create the map
    m = folium.Map(location=[41.882077, -87.627817], zoom_start=12)

    # Add ward boundaries to the map
    folium.GeoJson(
        ward_boundaries,
        name="Ward Boundaries",
        style_function=lambda x: {
            "fillColor": "blue",
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.1,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['ward'],
            aliases=['Ward: '],
            localize=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 2px;
            """,
        )
    ).add_to(m)

    # Add MarkerCluster for crashes
    marker_cluster = MarkerCluster().add_to(m)

    # Add crash points with popups
    for _, crash in filtered_data.iterrows():
        lat, lon = crash['geometry'].y, crash['geometry'].x
        crash_date = crash['CRASH_DATE']
        most_severe_injury = crash['MOST_SEVERE_INJURY']
        person_types_str = str(crash['PERSON_TYPE']) if pd.notnull(crash['PERSON_TYPE']) else "No data"
        prim_cause_str = str(crash['PRIM_CONTRIBUTORY_CAUSE']) if pd.notnull(crash['PRIM_CONTRIBUTORY_CAUSE']) else "No data"
        crash_type_str = str(crash['FIRST_CRASH_TYPE']) if pd.notnull(crash['FIRST_CRASH_TYPE']) else "No data"
        weather_str = str(crash['WEATHER_CONDITION']) if pd.notnull(crash['WEATHER_CONDITION']) else "No data"
        lighting_str = str(crash['LIGHTING_CONDITION']) if pd.notnull(crash['LIGHTING_CONDITION']) else "No data"
        trafficway_type_str = str(crash['TRAFFICWAY_TYPE']) if pd.notnull(crash['TRAFFICWAY_TYPE']) else "No data"
        address_str = str(crash['ADDRESS']) if pd.notnull(crash['ADDRESS']) else "No data"

        # Popup text
        popup_text = f"""
            <div style="word-wrap: break-word; width: 250px;">
                <b>Date of Crash:</b> {crash_date}<br>
                <b>Address:</b> {address_str}<br>
                <b>Most Severe Injury:</b> {most_severe_injury}<br>
                <b>Person Types:</b> {person_types_str}<br>
                <b>Primary Cause:</b> {prim_cause_str}<br>
                <b>Crash Type:</b> {crash_type_str}<br>
                <b>Weather Condition:</b> {weather_str}<br>
                <b>Lighting Condition:</b> {lighting_str}<br>
                <b>Trafficway Type:</b> {trafficway_type_str}
            </div>
        """
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color='red', icon='info-sign'),
        ).add_to(marker_cluster)

    # Save the map as an HTML file
    map_html_path = os.path.join(output_dir, f"crash_map_{year}.html")
    m.save(map_html_path)
    print(f"Map for year {year} saved successfully at {map_html_path}")

print("All maps generated and saved successfully.")
