from shiny import App, render, ui
import pandas as pd 
import os
import json
import plotly.express as px
import plotly.graph_objects as go
import altair as alt 

base_path = "/Users/charismalambert/Desktop/"

regressions_path = os.path.join(base_path, "regression_df.csv")
regressions_df = pd.read_csv(regressions_path)

def accidents_by_season(year):
    tracking_by_season = regressions_df[regressions_df["YEAR"] == year].groupby(["SEASON", "CRASH_HOUR"]).size().reset_index(name = "count")

    heatmap = alt.Chart(tracking_by_season).mark_rect().encode(
        x = "CRASH_HOUR:O",
        y = "SEASON:O",
        color = "count:Q", 
    ).properties(
        title=f"Number of Accidents during each Season in {year}",
        width = 600,
        height = 300
    ).configure_title(
        fontSize = 18
    )
    return heatmap 

def variable_relationships(IV, DV, year):
    use_this_df = regressions_df[regressions_df["YEAR"] == year]
    if IV == "AGE":
        fig = px.box(use_this_df, 
            x = DV, 
            y = IV,
            color = DV,
            title = f"{IV} vs {DV} for Traffic Crashes in {year}",
            labels = {IV: IV, DV: DV})
    else: 
        fig = px.histogram(use_this_df,
            x = IV,
            y = DV,
            barmode = 'group',
            title = f"{IV} vs {DV} for Traffic Crashes in 2024",
            labels = {IV: IV, DV: DV})
    fig.update_layout(legend_title_text = DV)
    return fig


app_ui = ui.page_fluid(
    ui.sidebar(
        ui.h3("Crash Trends and Relationships"),
        ui.layout_columns(
            # Output heatmaps side by side
            ui.card(
                ui.input_select("year1", "Select Year for Heatmap 1:", [2021, 2022, 2023, 2024]),
                ui.output_plot("heatmap_1")
            ),
            ui.card(
                ui.input_select("year2", "Select Year for Heatmap 2:", [2021, 2022, 2023, 2024], selected = None),
                ui.output_plot("heatmap_2")
            ) 
        ),
        # Dropdown menu for variable relationships
        ui.input_select("IV", "Select Demographic Variable:", ["AGE", "SEX_R", "PERSON_TYPE_R"]),
        ui.input_select("DV", "Select Crash Outcome:", ["INJURY_CLASSIFICATION_R", "AIRBAG_DEPLOYED_R", "EJECTION_R"]),
        ui.input_select("YEAR", "Select the Year:", [2021, 2022, 2023, 2024]),
        #  Output variable relationship plot based on selected variables
        ui.output_plot("variable_relationships_chart")
    )
)



def server(input, output, session):
    @output()
    def heatmap_1():
        return accidents_by_season(input.year1())
    
    @output()
    def heatmap_2():
        return accidents_by_season(input.year2())
    
    @output()
    def variable_relationships_chart():
        return variable_relationships(input.IV(), input.DV(), input.YEAR())
        
    
app = App(app_ui, server)

if __name__ == "__main__":
    app.run(debug = True)