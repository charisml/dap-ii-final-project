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
        # Simple map without any data
        m = folium.Map(location=[41.882077, -87.627817], zoom_start=12)
        
        # Save map in same directory as app
        map_html_path = os.path.join(www_dir, "map.html")
        m.save(map_html_path)

        if os.path.exists(map_html_path):
            print(f"Map HTML file successfully saved at {map_html_path}")
        else:
            print(f"Map HTML file was not saved successfully!")
        
        return ui.HTML(f'<iframe src="/map.html" width="100%" height="600px"></iframe>')

app = shiny.App(app_ui, server, static_assets=www_dir)