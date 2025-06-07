import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

#st.set_page_config(layout="wide")
#st.title("Map Transaction Data - State-wise (India Map)")

path=r"D:/BONEYS/WEB/PYTHON/Project/PhonePe/data/map/transaction/hover/country/india/state"
Map_trans_state_list=os.listdir(path)

#This is to extract the data's to create a dataframe
clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Transaction_count':[], 'Transaction_amount':[]}

for i in Map_trans_state_list:
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
            for z in D['data']['hoverDataList']:
              Name=z['name']
              count=z['metric'][0]['count']
              amount=z['metric'][0]['amount']
              clm['District_name'].append(Name)
              clm['Transaction_count'].append(count)
              clm['Transaction_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Map_trans_state=pd.DataFrame(clm)

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
Map_trans_state['State'] = Map_trans_state['State'].str.strip().str.lower()
Map_trans_state['State'] = Map_trans_state['State'].replace(state_name_map)

top_10_df = (
    Map_trans_state.groupby("State")["Transaction_amount"]
    .sum()
    .reset_index()
    .sort_values(by="Transaction_amount", ascending=False)
    .head(10))
top_10_df = top_10_df.reset_index(drop=True)  # Drop old index
top_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_map_trans_top10"):
    st.subheader("Top 10 States by transaction Amount")
    st.dataframe(top_10_df)
"""
bottom_10_df = (
    Map_trans_state.groupby("State")["Transaction_amount"]
    .sum()
    .reset_index()
    .sort_values(by="Transaction_amount", ascending=True)
    .head(10))
bottom_10_df = bottom_10_df.reset_index(drop=True)  # Drop old index
bottom_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_map_trans_bottom10"):
    st.subheader("Least 10 States by transaction Amount")
    st.dataframe(bottom_10_df)
"""
# Load GeoJSON data from URL
# Plotting Total transaction Amount by State
state_summary = (
    Map_trans_state
    .groupby('State', as_index=False)
    .agg({'Transaction_amount': 'sum'})
)

Map_Trans_fig = px.choropleth(
    state_summary,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Transaction_amount',
    color_continuous_scale='Blues',
    title='Total transaction Amount by State'
)

Map_Trans_fig.update_geos(fitbounds="locations", visible=False)

# Display in Streamlit
#st.plotly_chart(Map_Trans_fig, use_container_width=True)

# Display statewise growth trend
state_yearly = (
    Map_trans_state
    .groupby(['State', 'Year'], as_index=False)
    .agg({'Transaction_amount': 'sum'})
    )
state_yearly['Year'] = state_yearly['Year'].astype(int)

# Line chart
fig_state_trend_total = px.line(
    state_yearly,
    x='Year',
    y='Transaction_amount',
    color='State',
    markers=True,
    title="Transaction Growth Trajectory by State"
)
#st.plotly_chart(fig_state_trend, use_container_width=True)
