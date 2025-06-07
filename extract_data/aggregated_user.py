import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

#st.set_page_config(layout="wide")
#st.title("Map User Data - State-wise (India Map)")

path=r"D:/BONEYS/WEB/PYTHON/Project/PhonePe/data/aggregated/user/country/india/state"
Agg_user_state_list=os.listdir(path)

#This is to extract the data's to create a dataframe
clm={'State':[],'Year':[],'Quater':[],'Mobile_Brand_Used':[],'Usage_count':[],'Percentage':[]}

for i in Agg_user_state_list:
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
            #in this, usersByDevice has null value. So checking them
            users = D.get('data', {}).get('usersByDevice')
            if users is None:
                continue
            else:
                for z in users:
                    Brand=z['brand']
                    count=z['count']
                    perc=z['percentage']
                    clm['Mobile_Brand_Used'].append(Brand)
                    clm['Usage_count'].append(count)
                    clm['Percentage'].append(perc)
                    clm['State'].append(i)
                    clm['Year'].append(j)
                    clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_User_state=pd.DataFrame(clm)

#You need to map your State names to the names used in the GeoJSON file (properties.ST_NM). Otherwise you will get blank figure.
state_name_map = {
    "andaman-&-nicobar-islands": "Andaman & Nicobar Islands",
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
Agg_User_state['State'] = Agg_User_state['State'].str.strip().str.lower()
Agg_User_state['State'] = Agg_User_state['State'].replace(state_name_map)

top_10_df = (
    Agg_User_state.groupby("State")["Usage_count"]
    .sum()
    .reset_index()
    .sort_values(by="Usage_count", ascending=False)
    .head(10))
top_10_df = top_10_df.reset_index(drop=True)  # Drop old index
top_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_agg_user_top10"):
    st.subheader("Top 10 States by Mobile Usage Count")
    st.dataframe(top_10_df)
"""
bottom_10_df = (
    Agg_User_state.groupby("State")["Usage_count"]
    .sum()
    .reset_index()
    .sort_values(by="Usage_count", ascending=True)
    .head(10))
bottom_10_df = bottom_10_df.reset_index(drop=True)  # Drop old index
bottom_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_agg_user_bottom10"):
    st.subheader("Least 10 States by Mobile Usage Count")
    st.dataframe(bottom_10_df)
"""
# Load GeoJSON data from URL
#Plotting total mobile usage with respect to state
state_summary = (
    Agg_User_state
    .groupby('State', as_index=False)
    .agg({'Usage_count': 'sum'})
)

Agg_User_fig = px.choropleth(
    state_summary,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Usage_count',
    color_continuous_scale='Greens',
    title='Total Mobile Usage Count by State'
)

Agg_User_fig.update_geos(fitbounds="locations", visible=False)

# Display in Streamlit
#st.plotly_chart(Agg_User_fig, use_container_width=True)

#finding user preferences across different device brands
brand_summary = (
    Agg_User_state
    .groupby('Mobile_Brand_Used',as_index=False)
    .agg({'Usage_count': 'sum'})
)

brand_fig = px.bar(
    brand_summary, 
    x="Mobile_Brand_Used", 
    y="Usage_count", 
    title="Comparision of Device Brands by Registered Users", 
    color="Mobile_Brand_Used", 
    color_continuous_scale="Blues")

#st.plotly_chart(brand_fig, use_container_width=True)