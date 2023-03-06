#%%
import geopandas as gpd
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import altair as alt
from matplotlib import pyplot as plt
import numpy as np
from altair import datum


# %%
source1 = './Data/NYPD_Shooting_Incident_Data__Historic.csv'
source2 = './Data/New_York_City_Population.csv'
source3= './Data/NYC Borough Boundaries.geojson'



shooting = pd.read_csv(source1)
boro_pop = pd.read_csv(source2)
boro_boundary = gpd.read_file(source3)

# %%

# dropping unrequired columns
shooting= shooting.drop(['PRECINCT','JURISDICTION_CODE','LOCATION_DESC',
'X_COORD_CD','Y_COORD_CD','Lon_Lat', 'LOCATION_DESC'], axis=1)

# changing all column names to lowercase and renaming the statistical_murder_flag... 
# column for convenience/ personal preference
shooting.columns=shooting.columns.str.lower()
shooting = shooting.rename(columns={'statistical_murder_flag': 'murder_flag'})

# %%

# Next, we will convert the _occur_date_ and _occur_time_ columns to datetime format
shooting['occur_date'] = pd.to_datetime(shooting.occur_date)
shooting['occur_time'] = pd.to_datetime(shooting.occur_time)

# %%

# Extracting only the required columns from the boro_pop dataset
boro_pop = boro_pop[['Borough','2020']]
# %%

# renaming the columns for uniformity and easy understanding. This will be vital for merge operation which 
# will be performed later in this project
boro_pop= boro_pop.rename(columns={'Borough':'boro', '2020':'population'})
# %%

# stripping leading and trailing whitespaces from the records in the boro column. From previous handling of the...
# dataset, it was discovered that there are leading white spaces in the boro column, leading to incorrect...
# result of PD Merge (which will  be performed later in this project)
boro_pop['boro'] = boro_pop['boro'].str.strip()
boro_pop['boro'] = boro_pop['boro'].str.upper()

# %%

# renaming the columns for uniformity and easy understanding and changing the values in that colun to uppercase.
# These steps are vital for the success of the merge operation which will be performed later in this project
 
boro_boundary = boro_boundary.rename(columns={'boro_name': 'boro'})
boro_boundary['boro'] = boro_boundary['boro'].str.upper()

# %%

# Creating 'year' column in the 'shooting' dataset by extracting the year of occurence from occur_date column
shooting['year']= shooting["occur_date"].dt.year
# %%

# Adding a column with the value 'TOTAL' . This will be useful for later visualisations
shooting['total']= 'TOTAL'

# %%

alt.data_transformers.disable_max_rows()

# %%


borough= alt.Chart(shooting).mark_line(tooltip= True).encode(
    x= alt.X('year(occur_date):T', title= 'Year'),
    y= alt.Y('count(incident_key)', title= 'Number of Shootings'),
    color = alt.Color('boro', scale=alt.Scale(scheme= 'category10'), legend= alt.Legend(title= 'Borough')),
    )


total = alt.Chart(shooting).mark_line(strokeDash=[10,1], strokeWidth=3, tooltip= True).encode(
    x= alt.X('year(occur_date):T', axis=alt.Axis(title= 'Year', grid= False)),
    y= alt.Y('count(incident_key)', axis=alt.Axis(title= 'Number of Shootings', grid= False)),
    color= alt.Color('total', scale=alt.Scale(scheme='greys'), legend= alt.Legend(title= ''))
    
)

alt.layer( borough, total).resolve_scale(color='independent').properties(
    title= 'Shootings in New York (2006- 2021)').encode()

#%%

options= [None, 'BRONX','BROOKLYN','STATEN ISLAND','MANHATTAN']

drop_down = alt.binding_select(options= options, name= 'Boroughs ', labels= ['ALL','BRONX','BROOKLYN','STATEN ISLAND','MANHATTAN'])
selection =alt.selection_single(fields=['boro'], bind = drop_down)



alt.Chart(shooting).mark_bar(tooltip= True).encode(
    x= alt.X("year:O"),
    y=alt.Y("count(incident_key)", stack='normalize',  axis= alt.Axis(labels= False, format='.2%')),
    color = alt.Color("murder_flag")
    
).add_selection(selection).transform_filter(selection)

# %%

rect = alt.Chart(shooting[shooting['perp_race'].notnull()]).mark_rect( tooltip= True).encode(
    x= alt.X('perp_race', axis = alt.Axis(title= 'Perpetrator Race', labelAngle=-45)),
    y= alt.Y('vic_race', axis = alt.Axis(title= 'Victim Race'),),
    color = alt.Color('count()', scale= alt.Scale(scheme='reds'))
    ).transform_filter(
        datum.year == 2021
    )


circ = rect.mark_point().encode(
    alt.ColorValue('black'),
    alt.Size('count()',  legend=alt.Legend(title='Crime in Selection'))
    )
# add chart of total population

alt.layer(rect,circ).properties( title= 'Perpetrators and Victims of New York City Shootings by Race in 2021',
    width=400,
    height=400
)

# %%

rect = alt.Chart(shooting[(shooting['perp_age_group'].notnull()) & (shooting['perp_age_group'] != 'UNKNOWN') & (shooting['vic_age_group'] != 'UNKNOWN')]).mark_rect(tooltip= True).encode(
    x= alt.X('perp_age_group', sort=['<18','18-24','25-44','45-64','65+'], axis = alt.Axis(title= 'Perpetrator Age')),
    y= alt.Y('vic_age_group', sort=['<18','18-24','25-44','45-64','65+'], axis = alt.Axis(title= 'Victim Age')),
    color = alt.Color('count()', scale= alt.Scale(scheme='reds'))
    ).transform_filter(
        datum.year == 2021
    )


circ = rect.mark_point().encode(
    alt.ColorValue('black'),
    alt.Size('count()', legend=alt.Legend(title='Crime in Selection'))
    )
# add chart of total population

alt.layer(rect,circ).properties( title= 'Perpetrators and Victims of New York City Shootings by Age in 2021',
    width=400,
    height=400
)
#%%

conditions= [
    (shooting['occur_time'] >= pd.to_datetime('0:00')) &  (shooting['occur_time'] < pd.to_datetime('6:00')),
    (shooting['occur_time']>= pd.to_datetime('6:00')) &  (shooting['occur_time'] < pd.to_datetime('12:00')),
    (shooting['occur_time'] >= pd.to_datetime('12:00')) &  (shooting['occur_time'] < pd.to_datetime('18:00')),
    (shooting['occur_time'] >= pd.to_datetime('18:00')) &  (shooting['occur_time'] <= pd.to_datetime('23:59')),
    
]

choices = ['Midnight','Morning','Afternoon','Night']
shooting['time_of_day'] = np.select(conditions, choices, default=np.nan)

# %%

base = alt.Chart(shooting[shooting.year == 2021]).transform_joinaggregate(
    Total1='count(incident_key)',
    groupby= ['time_of_day']
).transform_joinaggregate(
    Total2='count(incident_key)'    
).encode(
    theta = alt.Theta('percentage:Q', stack="normalize"),    
    order= alt.Order('count():Q', sort= 'ascending'),
    tooltip= ['time_of_day', alt.Tooltip('percentage:Q', format=".0%")]).properties(
        title= 'Shootings in New york City by Time of Day in 2021 (%) '            
).transform_calculate( 
            percentage = (datum.Total1/ datum.Total2)
)


pie = base.mark_arc(outerRadius=120).encode(color= 'time_of_day:N')

text = base.mark_text(radius=100).encode(text= alt.Text("percentage:Q", format=".0%"))

pie + text

#%%

# group total number of shootings by borough, and keep only required columns 
boro_shooting = shooting[shooting['year']==2021][['boro','incident_key']].groupby('boro').count(
).reset_index().rename(columns= {'incident_key':'number_of_shootings'})
# %%

# merge the boro_shooting, boro_boundary and boro_pop datasets into a single dataset 'shooting_combined'
shooting_combined = pd.merge(left=boro_boundary, right= pd.merge(left= boro_shooting, right= boro_pop, on= 'boro', how= 'left'), on= 'boro', how= 'left')
shooting_combined['shootings_per_million'] = round((shooting_combined['number_of_shootings']/shooting_combined['population'])*1000000)


# %%

# Two geomaps comparing the total shootings against shootings_per_million across the 5 boroughs of New york City

chart_a= alt.Chart(shooting_combined).mark_geoshape(stroke='black').encode(
    alt.Color("number_of_shootings", scale=alt.Scale(scheme='reds'), legend=alt.Legend(
        orient='none',
        legendX= 20, legendY=20,
        direction='horizontal',
        titleAnchor='middle')),
    alt.Tooltip(["boro_code","boro", 'number_of_shootings', 'population'])
).properties( title= 'Number of Shootings by New York City Borough in 2021').project("naturalEarth1")


chart_b= alt.Chart(shooting_combined).mark_geoshape(stroke='black').encode(
    alt.Color("shootings_per_million", scale=alt.Scale(scheme='reds'), legend=alt.Legend(
        orient='none',
        legendX= 20, legendY=20,
        direction='horizontal',
        titleAnchor='middle')),
    alt.Tooltip(["boro_code","boro", 'shootings_per_million', 'population'])
).properties( title= 'Shootings per Million by New York City Borough in 2021').project("naturalEarth1")



alt.hconcat(
   chart_a, chart_b 
).resolve_scale(
    color='independent'
).configure(background='#DDEEFF')
# %%
