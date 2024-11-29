import shiny
from shiny import ui, render, Inputs, Outputs
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
import time
from shapely import wkt
import pandas as pd
import os
from pathlib import Path


# Define paths
app_dir = Path(__file__).parent
www_dir = app_dir / "www"
# Ensure directory exists
www_dir.mkdir(exist_ok=True)  
crashes_gdf = gpd.read_file(r'C:\Users\User\Documents\GitHub\dap-ii-final-project\App\crashes_gdf_2024.csv')

# Ensure geometry is properly set
crashes_gdf['geometry'] = crashes_gdf['LOCATION'].apply(wkt.loads)
crashes_gdf = gpd.GeoDataFrame(crashes_gdf, geometry='geometry')
crashes_gdf.set_crs(epsg=3435, inplace=True)

# Chatgpt's advice to speed up run time: import and process code in chunks
# Define chunk size
chunk_size = 100000

# Track chunks so I know everything is working properly
total_rows = len(crashes_gdf)
num_chunks = (total_rows + chunk_size - 1) // chunk_size  # Calculate total chunks
processed_chunks = []
start_time = time.time()

for i in range(num_chunks):
    start = i * chunk_size
    end = min(start + chunk_size, total_rows)
    chunk = crashes_gdf.iloc[start:end]

    processed_chunks.append(chunk)

    elapsed_time = time.time() - start_time
    print(f"Processed chunk {i + 1}/{num_chunks} - Rows: {start}-{end} (Elapsed time: {elapsed_time:.2f}s)")

# Combine chunks into a single gdf
processed_data = gpd.GeoDataFrame(pd.concat(processed_chunks, ignore_index=True))

# Make more manageable for testing
processed_data = processed_data.head(100)

# Load ward boundaries geojson
ward_boundaries = gpd.read_file(r'C:\Users\User\OneDrive - The University of Chicago\4_DAP-2\Final Project Data\ward_boundaries.geojson')
ward_boundaries = ward_boundaries.to_crs(epsg=3435)

app_ui = ui.page_fluid(
    ui.input_select(
        "year",
        "Select Year",
        choices=["All Years"] + sorted(processed_data['YEAR'].unique().tolist()),
        selected="All Years"
    ),
    ui.output_ui("map_ui")
)

def server(input, output, session):
    @output()
    @render.ui
    def map_ui():
        selected_year = input.year()

        # Filter by year and include option for all years
        if selected_year == "All Years":
            filtered_data = processed_data
        else:
            filtered_data = processed_data[processed_data['YEAR'] == int(selected_year)]
         # Check that data is loaded properly
        print(f"Filtered data: {filtered_data.head()}") 

        # set map starting location at center of Chicago grid - State x Madison
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
        ).add_to(m)

        # Add crash points
        marker_cluster = MarkerCluster().add_to(m)

        # Add popups
        for _, crash in filtered_data.iterrows():
            crash_record_id = crash['CRASH_RECORD_ID']
            lat, lon = crash['geometry'].y, crash['geometry'].x
            most_severe_injury = crash['MOST_SEVERE_INJURY']
            person_types_str = (
                str(crash['PERSON_TYPE']) if pd.notnull(crash['PERSON_TYPE']) else "No data"
            )

             # Asked chatgpt how to make it so crash ID isn't longer than popup (wrap text)
            popup_text = f"""
                <div style="word-wrap: break-word; width: 250px;">
                    <b>Crash Record ID:</b> {crash_record_id}<br>
                    <b>Most Severe Injury:</b> {most_severe_injury}<br>
                    <b>Person Types:</b> {person_types_str}
                </div>
            """
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color='red', icon='info-sign'),
            ).add_to(marker_cluster)

        map_html_path = os.path.join(www_dir, "map.html")
        m.save(map_html_path)

        if os.path.exists(map_html_path):
            print(f"Map HTML file successfully saved at {map_html_path}") 
        else: print(f"Map HTML file was not saved successfully!") 
        # Read the map HTML content 
        with open(map_html_path, 'r', encoding='utf-8') as file: 
            map_content = file.read() 
        return ui.HTML(f'<iframe srcdoc="{map_content}" width="100%" height="600px"></iframe>')

app = shiny.App(app_ui, server, static_assets=www_dir)