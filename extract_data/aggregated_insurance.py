import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

#st.set_page_config(layout="wide")
#st.title("Aggregated Insurance Data - State-wise (India Map)")

path=r"D:/BONEYS/WEB/PYTHON/Project/PhonePe/data/aggregated/insurance/country/india/state"
Agg_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#This is to extract the data's to create a dataframe
clm={'State':[], 'Year':[],'Quater':[],'Insurance':[], 'Insurance_count':[], 'Insurance_amount':[]}

for i in Agg_state_list:
    p_i=path+"/"+i
    Agg_yr=os.listdir(p_i)
    #delhi
    for j in Agg_yr:
        p_j=p_i+"/"+j
        #2018
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+"/"+k 
            #1.json
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Insurance'].append(Name)
              clm['Insurance_count'].append(count)
              clm['Insurance_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Creating dataframe
Agg_Insu_state=pd.DataFrame(clm)

#You need to map your State names to the names used in the GeoJSON file (properties.ST_NM). Otherwise you will get blank figure.
state_name_map = {
    'andaman-&-nicobar-islands': 'Andaman & Nicobar Islands',
    'andhra-pradesh': 'Andhra Pradesh',
    'arunachal-pradesh': 'Arunachal Pradesh',
    'assam': 'Assam',
    'bihar': 'Bihar',
    'chandigarh': 'Chandigarh',
    'chhattisgarh': 'Chhattisgarh',
    'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli',
    'delhi': 'NCT of Delhi',
    'goa': 'Goa',
    'gujarat': 'Gujarat',
    'haryana': 'Haryana',
    'himachal-pradesh': 'Himachal Pradesh',
    'jammu-&-kashmir': 'Jammu & Kashmir',
    'jharkhand': 'Jharkhand',
    'karnataka': 'Karnataka',
    'kerala': 'Kerala',
    'ladakh': 'Ladakh',
    'lakshadweep': 'Lakshadweep',
    'madhya-pradesh': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra',
    'manipur': 'Manipur',
    'meghalaya': 'Meghalaya',
    'mizoram': 'Mizoram',
    'nagaland': 'Nagaland',
    'odisha': 'Odisha',
    'puducherry': 'Puducherry',
    'punjab': 'Punjab',
    'rajasthan': 'Rajasthan',
    'sikkim': 'Sikkim',
    'tamil-nadu': 'Tamil Nadu',
    'telangana': 'Telangana',
    'tripura': 'Tripura',
    'uttar-pradesh': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand',
    'west-bengal': 'West Bengal'
}
Agg_Insu_state['State'] = Agg_Insu_state['State'].str.strip().str.lower()
Agg_Insu_state['State'] = Agg_Insu_state['State'].replace(state_name_map)

top_10_df = (
    Agg_Insu_state.groupby("State")["Insurance_count"]
    .sum()
    .reset_index()
    .sort_values(by="Insurance_count", ascending=False)
    .head(10))
top_10_df = top_10_df.reset_index(drop=True)  # Drop old index
top_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_agg_insu_top10"):
    st.subheader("Top 10 States by Insurance Count")
    st.dataframe(top_10_df)
"""
bottom_10_df = (
    Agg_Insu_state.groupby("State")["Insurance_count"]
    .sum()
    .reset_index()
    .sort_values(by="Insurance_count", ascending=True)
    .head(10))
bottom_10_df = bottom_10_df.reset_index(drop=True)  # Drop old index
bottom_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_agg_insu_bottom10"):
    st.subheader("Least 10 States by Insurance Count")
    st.dataframe(bottom_10_df)
"""
# Load GeoJSON data from URL
state_summary = (
    Agg_Insu_state
    .groupby('State', as_index=False)
    .agg({'Insurance_count': 'sum'})
)

# Plotting total insurance count by state
Agg_Insu_fig = px.choropleth(
    state_summary,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Insurance_count',
    color_continuous_scale='Reds',
    title='Total Insurance Count by State'
)

Agg_Insu_fig.update_geos(fitbounds="locations", visible=False)

# Display in Streamlit
#st.plotly_chart(Agg_Insu_fig, use_container_width=True)

# Display statewise growth trend
state_yearly = (
    Agg_Insu_state
    .groupby(['State', 'Year'], as_index=False)
    .agg({'Insurance_count': 'sum'})
    )
state_yearly['Year'] = state_yearly['Year'].astype(int)

# Line chart
fig_state_trend = px.line(
    state_yearly,
    x='Year',
    y='Insurance_count',
    color='State',
    markers=True,
    title="Insurance Growth Trajectory by State"
)
#st.plotly_chart(fig_state_trend, use_container_width=True)
