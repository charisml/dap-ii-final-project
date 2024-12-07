# Transportation and Public Safety
# What is the state of traffic safety in Chicago? What factors influence vehicle crashes?

Data and Programming II Final Project (Fall 2024)

These research questions came out of personal interest as we have either experienced and/or witnessed crashes in Chicago and were curious about the frequency and cause of such occurrences. The Chicago Data Portal contained three different data sets for us to examine: 
- Traffic Crashes - Crashes: Contains data on traffic crashes within city limits of Chicago and the reporting Chicago Police Department jurisdiction. 
- Traffic Crashes - People: Contains data on the people involved in traffic crashes and their level of injury. Involvement is defined as being an occupant in the vehicle at time of crash or the other party in the crash (pedestrian, cyclist, etc.).
- Traffic Crashes - Vehicle: Contains data on the vehicles involved in the accident, which includes motor vehicle and non-motor vehicle modes of transportation. 

After cleaning, our dataset was too large for Github and to be processed by Shiny, so we had to truncate it even more to hold 1,000 random instances per year. The final Shiny app map contains a simple random sampling of 1,000 crash instances per year. For the statistical analysis app, the random sample was stratified to keep the same ratio of data from the original dataset in the sample (ie- if the original dataset had 30% F and 70% M, our sample would have that same ratio). We maintained the original idea to visualize all crashes on a map, and achieved this by generating a simple HTML map of all crashes for a given year. We generated five maps, one for each year 2020-2025, which are available in our Google Drive data folder. 

In our analysis we examined the demographic data as independent variables and crash outcomes as dependent variables. The variables that users can choose from are: Age, Sex, Person_Type,  Injury_Classification, Ejection, and Airbag_Deployed.
From examining these variables, users can understand the following about Chicago crashes: 

- Men are more likely to get into traffic accidents
- Time of day is important factor in crashes, most occuring between the hours of 3-6pm
- The fewest accidents were in Spring 2021, otherwise each year's’ accident frequency is relatively the same
- More accidents occurring earlier in the day Fall and Summer
- Wide range of people involved, mostly 20-60 yo.

  
<img width="511" alt="Screenshot 2024-12-01 at 11 00 41 PM" src="https://github.com/user-attachments/assets/ed7d0b33-54cc-4e8d-a2a6-53c1b3c00092">
<img width="511" alt="Screenshot 2024-12-01 at 11 01 00 PM" src="https://github.com/user-attachments/assets/627c50e4-1181-48eb-b378-a0125ea4be25">
<img width="508" alt="Screenshot 2024-12-01 at 11 00 54 PM" src="https://github.com/user-attachments/assets/e66ae379-3825-4137-8927-2c75ada557c8">
<img width="512" alt="Screenshot 2024-12-01 at 11 00 48 PM" src="https://github.com/user-attachments/assets/e46044a1-41fb-4a3e-bb91-e1d838238b7c">


  
One major policy implication is the need to address the high frequency of crashes during rush hour (3 - 6pm). An intervention to consider is optimizing traffic light timings. Additionally, improving infrastructure like protected bike lanes and pedestrian-friendly designs can enhance safety for vulnerable road users. A city that does this well is Pittsburgh. Pittsburgh’s use of the diagonal street crossings, known as the “Barnes Dance,” optimizes crossing pathways for pedestrians and allows drivers to benefit from longer green lights, leading to less crashes due to the optimization of the traffic flow.  

For future use, download our repository locally by cloning it to your local network. After cloning, ensure your local environment is set up to run our code by navigating to the folder where you’ve cloned. Then change directory (cd) to the Apps folder and cd to crash-map. Finally, run python app.py. Copy the generated url (http://127.0.0.1:8000 ) into your webpage to interact with our application and findings. 
