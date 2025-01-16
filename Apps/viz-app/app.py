from shiny import App, render, ui
import pandas as pd
import plotly.express as px
import altair as alt
import os
from shinywidgets import output_widget, render_widget, render_altair

base_path = r"C:\Users\User\Documents\GitHub\dap-ii-final-project\Data"

regressions_path = os.path.join(base_path, "regression_df.csv")
regression_df = pd.read_csv(regressions_path, low_memory=False)

# Change variable type from object to category for grouping
for col in regression_df.select_dtypes(include="object").columns:
   regression_df[col] = regression_df[col].astype("category")

# Ensure all date variables, except year, are datetime
regression_df["YEAR"] = regression_df["YEAR"].astype(int)
regression_df["CRASH_DATE"] = pd.to_datetime(regression_df["CRASH_DATE"], errors="coerce")
regression_df["CRASH_MONTH"] =regression_df["CRASH_MONTH"].astype(str)
regression_df["CRASH_HOUR"] = regression_df["CRASH_HOUR"].astype(int)

# App UI Layout
app_ui = ui.page_fluid(
   ui.h1("Traffic Crash Analysis Project"),
   ui.p("This project explores traffic crash data in the city of Chicago from 2021-2024. "
        "The goal is to uncover trends and patterns in traffic crashes to propose solutions for safer commuting. "
        "We examine seasonal patterns, demographic factors like sex and age, and visualize crash locations on a map of Chicago. "
        "The project allows users to explore data interactively."),
  
   ui.h3("Demographic Information"),
   ui.layout_columns(
       ui.card(
           ui.h3("Sex Breakdown"),
           output_widget("sex_breakdown")
       ),
       ui.card(
           ui.h3("Age Distribution"),
           output_widget("age_breakdown")
       )
   ),
  
   ui.h3("Crash Trends and Relationships"),
   ui.layout_columns(
       ui.card(
           ui.input_select("year1", "Select Year for Heatmap 1:", [2021, 2022, 2023, 2024]),
           output_widget("heatmap_1")
       ),
       ui.card(
           ui.input_select("year2", "Select Year for Heatmap 2:", [2021, 2022, 2023, 2024]),
           output_widget("heatmap_2")
       )
   ),
  
   ui.card(
       ui.input_select("IV", "Select Demographic Variable:", ["AGE", "SEX", "PERSON_TYPE"]),
       ui.input_select("DV", "Select Crash Outcome:", ["INJURY_CLASSIFICATION", "AIRBAG_DEPLOYED", "EJECTION"]),
       ui.input_select("YEAR", "Select Year:", [2021, 2022, 2023, 2024]),
       output_widget("variable_relationships_chart")
   )
)

# Server logic
def server(input, output, session):
   @output()
   @render_widget
   def sex_breakdown():
       total_sex = len(regression_df["SEX"].dropna())
       sex_percent = regression_df.groupby(["SEX"], observed=False).size().reset_index(name="count")
       sex_percent["PERCENTAGE"] = (sex_percent["count"] / total_sex) * 100
       sex_percent["PERCENTAGE"] = sex_percent["PERCENTAGE"].astype(float)

       fig = px.bar(sex_percent,
                    x="SEX",
                    y="PERCENTAGE",
                    title="Sex Breakdown for Traffic Crashes (Sample Total)",
                    labels={"PERCENTAGE": "Percentage (%)", "SEX": "Sex"})
       fig.update_layout(
           yaxis=dict(title="Percentage (%)"),
           showlegend=False
       )
       return fig
  
   @output()
   @render_widget
   def age_breakdown():
       ages = regression_df["AGE"].dropna()
      
       fig = px.histogram(ages,
                          nbins = 10,
                          title = "Age Distribution for Traffic Crashes (Sample Total)",
                          labels = {"AGE":"Age"},
                          histnorm = "percent")
       fig.update_layout(
           xaxis = dict(title = "Age"),
           yaxis = dict(title= "Percentage (%)"),
           showlegend = False
       )
       return fig
  
   @output()
   @render_altair
   def heatmap_1():
       tracking_by_season = regression_df[regression_df["YEAR"] == int(input.year1())].groupby(["SEASON", "CRASH_HOUR"], observed=False).size().reset_index(name = "count")
       heatmap = alt.Chart(tracking_by_season).mark_rect().encode(
           x = "CRASH_HOUR:O",
           y = "SEASON:O",
           color = "count:Q",
       ).properties(
           title=f"Number of Accidents during each Season in {input.year1()}"
       ).configure_title(
           fontSize = 18
       )
       return heatmap
  
   @output()
   @render_altair
   def heatmap_2():
       tracking_by_season = regression_df[regression_df["YEAR"] == int(input.year2())].groupby(["SEASON", "CRASH_HOUR"],  observed=False).size().reset_index(name = "count")
       heatmap2 = alt.Chart(tracking_by_season).mark_rect().encode(
           x = "CRASH_HOUR:O",
           y = "SEASON:O",
           color = "count:Q",
       ).properties(
           title=f"Number of Accidents during each Season in {input.year2()}"
       ).configure_title(
           fontSize = 18
       )
       return heatmap2
  
   @output()
   @render_widget
   def variable_relationships_chart():
       use_this_df = regression_df[regression_df["YEAR"] == int(input.YEAR())]
       #if input.IV() != "AGE":
           #use_this_df = use_this_df.drop_duplicates(input.DV())
          
       DV_counts = (use_this_df.groupby([input.IV(),input.DV()], observed=False).size().reset_index(name = "count"))
      
       fig = px.bar(DV_counts,
           x = input.IV(),
           y = "count",
           color = input.DV(),
           title = f"{input.IV()} vs {input.DV()} for Traffic Crashes in {input.YEAR()}",
           labels = {input.IV(): input.IV(), "count": f"Number of {input.DV()} occurences", input.DV(): input.DV()})

       fig.update_layout(
           yaxis = dict(title= "Count"),
           legend_title_text =f"{input.DV()} Categories",
           showlegend = True
       )
       return fig
      
  
app = App(app_ui, server)

if __name__ == "__main__":
   app.run()

