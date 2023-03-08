# Please follow this nbviewer link to view the project code and interactive charts: 
https://nbviewer.org/github/damilare-osunleke/NYC_Shooting/blob/main/main.ipynb


# Shootings: Gun Violence in New York City

####                                    Project Description   
####

##### Goal:
This project seeks to understand gun voilence in the city of New York, and obtain insights that can potentially help to reduce the spate of shootings in the city. To achieve this, the following questions are explored in this project:

1   What has been the overall trend in shootings across the five boroughs of the city over the last 15 years?   
2   What proportion of shootings resulted in deaths?   
3   What are the dominan profiles of the perpetrators and victims of shootings: race, age group?    
4   During what time of the day do most shootings occur?     
5   Which boroughs of New York City have the worst shootings problem?   



#### Motivation   

In the last decade, a lot has been reported in the bedia about the epidemic of gun violence in the United States of America, particularly mass shootings. Although mass shootings recieve extensive coverage in the media, they account for only a small fraction of gun-related violence and death in the country.

In 2018, the Centers for Disease Control and Prevention's (CDC) National Center for Health Statistics reports 38,390 deaths by firearm, bringing the rate of firearm death to about 12 per 100,000. [[1]](https://www.cdc.gov/injury/wisqars/pdf/leading_causes_of_injury_deaths_highlighting_violence_2018-508.pdf), [[2]](https://www.kff.org/other/state-indicator/firearms-death-rate-per-100000/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D)

New York City is the most populated and most densely-populated city in the United States, with its fair share of gun voilence. Many of the cases of shootings reported in the media happended in New York city. Although the city has made progress in the reduction of crime in general, and gun violence in particular, gun violence remains a serious concern. For instance, compared to London (a city with similar population), NYC had double the number of gun violence in 2021. [[3]](https://www.statista.com/statistics/865565/gun-crime-in-london/)

I was motivated to carry out this project in order to better understand the dynamics of gun violence in one of the world's most popular cities.


#### Data

Three datasets were used for this project. All are publicly available of the open data platform of the City of New York and can be accessed via the links below:

1) Historic records of all shootings in New York City (2006 to 2021): [NYPD Shooting Incident Data (Historic)](https://data.cityofnewyork.us/Public-Safety/NYPD-Shooting-Incident-Data-Historic-/833y-fsy8). Data provided by Police Department (NYPD)
2) Historic and projected population of New York City by Borough: [New York City Population by Borough, 1950 - 2040](https://data.cityofnewyork.us/City-Government/New-York-City-Population-by-Borough-1950-2040/xywu-7bv9). Data provided by Department of City Planning (DCP)
3) A map of the administrative boundaries of the the 5 boroughs of New York City: [Borough Boundaries](https://data.cityofnewyork.us/browse?q=map%20borough&sortBy=relevance). Data provided by Department of City Planning (DCP)


Since the datasets is published by reputable government agencies, they are considered very reliable.


##### Data Description
Below are the features from each dataset that was used for this projects

**Shooting Dataset:**   
a) **incident_key** : Randomly generated persistent and unique ID for each incident    
b) **occur_date** : Exact date of the shooting incident   
c) **occur_time** : Exact time of the shooting incident      
d) **boro** : Borough where the shooting incident occurred   
e) **statistical_murder_flag** : whether or not the shooting resulted in the victim’s death   
f) **perp_age_group** : Perpetrator’s age category      
g) **perp_sex** : Perpetrator’s sex description      
h) **perp_race** : Perpetrator’s race description   
f) **vic_age_group** : Victim’s age within a category   
i) **vic_sex** : Victim’s sex description   
j) **vic_race** : Victim’s race description   
i) **longitude** : longitudinal coordinate of the shooting location   
j) **latitude** : latitudinal  coordinate of the shooting location   


**Borough population dataset:**   
a) **Borough** : New York City borough name   
b) **2020** : Population of the borough as at the year 2020  


**Borough Boundaries dataset:**   
a) **boro_code** : Unique Borough code   
b) **boro_name** : Borough name 
b) **geometry** : Polygon representing the geometry of the borough 


