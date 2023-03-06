#%%
import geopandas as gpd
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import altair as alt
from matplotlib import pyplot as plt
import numpy as np
from altair import datum
import streamlit as st
import datetime


# %%
source1 = './Data/NYPD_Shooting_Incident_Data__Historic.csv'
source2 = './Data/New_York_City_Population.csv'
source3= './Data/NYC Borough Boundaries.geojson'



shooting = pd.read_csv(source1)
boro_pop = pd.read_csv(source2)
boro_boundary = gpd.read_file(source3)

#%%

shooting.head(5)
boro_pop.head(5)
boro_boundary.head(5)

# %%
st.header("Gun Violence in New york City")

# %%

st.markdown("<div><h3>Gun Violence in New york City</h3></div>", unsafe_allow_html = True)

# body {
#     background-color: lightblue;
# }

# h1 {
#     color: white;
#     text-align: center
# }

# p {
#     font-family: verdana;
#     font-size: 20px;
# }

