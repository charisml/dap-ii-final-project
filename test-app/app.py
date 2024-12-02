from pathlib import Path
import shiny
from shiny import ui, render, reactive
import folium
import os

# Define paths
app_dir = Path(__file__).parent
www_dir = app_dir / "www"
www_dir.mkdir(exist_ok=True)  # Create `www` directory if it doesn't exist

# Define UI
app_ui = ui.page_fluid(
    ui.input_action_button("generate", "Generate Map"),  # Button to trigger map generation
    ui.output_ui("map_ui"),  # Output UI for the map
)

def server(input, output, session):
    @output
    @render.ui
    @reactive.event(input.generate)  # Render only when the button is clicked
    def map_ui():
        # Path for the HTML file
        map_html_path = www_dir / "simple_map.html"

        # Create and save the map
        m = folium.Map(location=[41.882077, -87.627817], zoom_start=12)
        folium.Marker(
            location=[41.882077, -87.627817],
            popup="Test Marker",
            icon=folium.Icon(color="blue"),
        ).add_to(m)
        m.save(map_html_path)

        # Debugging: Print paths and ensure everything is as expected
        print(f"App Directory: {app_dir}")
        print(f"www Directory: {www_dir}")
        print(f"Map HTML Path: {map_html_path}")
        print(f"Does file exist? {os.path.exists(map_html_path)}")

        # Return iframe pointing to the static asset
        return ui.HTML('<iframe src="simple_map.html" width="100%" height="600px"></iframe>')

# Define the app with static_assets pointing to `www_dir`
app = shiny.App(app_ui, server, static_assets=www_dir)
