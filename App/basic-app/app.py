from shiny import App, render, ui
import pandas as pd 
import os
import matplotlib.pyplot as plt 
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
import altair as alt 
import seaborn as sns

base_path = "/Users/charismalambert/Documents/GitHub/dap-ii-final-project/App"

regressions_path = os.path.join(base_path, "regression_df.csv")
regressions_df = pd.read_csv(regressions_path)

def precomputed_by_season(year):
    tracking_by_season = regressions_df[regressions_df["YEAR"] == year].groupby(["SEASON", "CRASH_HOUR"]).size().reset_index(name = "count")
    return tracking_by_season

def accidents_by_season(year):
    tracking_by_season = precomputed_by_season(year)

    heatmap_data = tracking_by_season.pivot("SEASON", "CRASH_HOUR", "count").fillna(0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cax = ax.imshow(heatmap_data, cmap="YlGnBu", aspect="auto")
    ax.set_title(f"Number of Accidents during each Season in {year}")
    ax.set_xlabel('Crash Hour')
    ax.set_ylabel('Season')
    
    # Add color bar for the heatmap
    cbar = fig.colorbar(cax, ax=ax)
    cbar.set_label('Accident Count')
    
    ax.set_xticks(np.arange(len(heatmap_data.columns)))
    ax.set_xticklabels(heatmap_data.columns)
    ax.set_yticks(np.arange(len(heatmap_data.index)))
    ax.set_yticklabels(heatmap_data.index)
    
    # Rotate labels for better readability
    plt.xticks(rotation=45, ha="right")
    
    return fig

def variable_relationships(IV, DV, year):
    use_this_df = regressions_df[(regressions_df["YEAR"] == year) & (regressions_df[IV].notna())]
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if IV == "AGE":
        # Boxplot for demographic variable AGE vs outcome variable DV
        sns.boxplot(data=use_this_df, x=DV, y=IV, ax=ax)
        ax.set_title(f"{IV} vs {DV} for Traffic Crashes in {year}")
        ax.set_xlabel(DV)
        ax.set_ylabel(IV)
    else:
        # Histogram for other demographic variables vs crash outcome DV
        use_this_df.groupby([IV, DV]).size().unstack().plot(kind='bar', stacked=True, ax=ax)
        ax.set_title(f"{IV} vs {DV} for Traffic Crashes in {year}")
        ax.set_xlabel(IV)
        ax.set_ylabel(f"Count of {DV}")
    
    return fig


app_ui = ui.page_fluid(
    ui.h1("Traffic Crash Analysis Project"),
    ui.p("This project explores traffic crash data in the city of Chicago from 2021- 2024. The goal of this project is to uncover trends and patterns of traffic crashes in order to propose solutions for safe commuting in the city. "
        "We explore seasonal patterns of crashes, examine how demographic factors, such as sex and age, relate to crash outcomes, and visualize crash locations on a map of Chicago. "
        "The project is structured in a 'Choose Your Own Adventure' structure that allows the user to select variables of interest to them. "), 
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
    ui.card(
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
        return accidents_by_season(int(input.year1()))
    
    @output()
    def heatmap_2():
        return accidents_by_season(int(input.year2()))
    
    @output()
    def variable_relationships_chart():
        return variable_relationships(input.IV(), input.DV(), input.YEAR())
        
    
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
