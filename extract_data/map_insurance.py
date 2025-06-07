import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

#st.set_page_config(layout="wide")
#st.title("Mapped Insurance Data - State-wise (India Map)")

path=r"D:/BONEYS/WEB/PYTHON/Project/PhonePe/data/map/insurance/hover/country/india/state"
Map_Insu_Hover_state_list=os.listdir(path)

#This is to extract the data's to create a dataframe
clm={'State':[], 'Year':[],'Quater':[],'Insurance':[], 'Insurance_count':[], 'Insurance_amount':[]}

for i in Map_Insu_Hover_state_list:
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
              clm['Insurance'].append(Name)
              clm['Insurance_count'].append(count)
              clm['Insurance_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Map_Insu_state=pd.DataFrame(clm)

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
Map_Insu_state['State'] = Map_Insu_state['State'].str.strip().str.lower()
Map_Insu_state['State'] = Map_Insu_state['State'].replace(state_name_map)

top_10_df = (
    Map_Insu_state.groupby("State")["Insurance_amount"]
    .sum()
    .reset_index()
    .sort_values(by="Insurance_amount", ascending=False)
    .head(10))
top_10_df = top_10_df.reset_index(drop=True)  # Drop old index
top_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_map_insu_top10"):
    st.subheader("Top 10 States by Insurance Count")
    st.dataframe(top_10_df)
"""
bottom_10_df = (
    Map_Insu_state.groupby("State")["Insurance_amount"]
    .sum()
    .reset_index()
    .sort_values(by="Insurance_amount", ascending=True)
    .head(10))
bottom_10_df = bottom_10_df.reset_index(drop=True)  # Drop old index
bottom_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_map_insu_bottom10"):
    st.subheader("Least 10 States by Insurance Count")
    st.dataframe(bottom_10_df)
"""
# Load GeoJSON data from URL
# Plotting Total Insurance Amount by State
state_summary = (
    Map_Insu_state
    .groupby('State', as_index=False)
    .agg({'Insurance_amount': 'sum'})
)

Map_Insu_fig = px.choropleth(
    state_summary,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Insurance_amount',
    color_continuous_scale='Reds',
    title='Total Insurance Amount by State'
)

Map_Insu_fig.update_geos(fitbounds="locations", visible=False)

# Display in Streamlit
#st.plotly_chart(Map_Insu_fig, use_container_width=True)

#FINDING INSURANCE ENGAGEMENT ANALYSIS BASED ON USERS

path2=r"D:/BONEYS/WEB/PYTHON/Project/PhonePe/data/map/user/hover/country/india/state"
Map_user_state_list=os.listdir(path2)

clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Registered_Users_Count':[], 'Apps_Open':[]}

for i in Map_user_state_list:
    p_i=path2+"/"+i
    Agg_yr=os.listdir(p_i)
    #delhi
    for j in Agg_yr:
        p_j=p_i+"/"+j
        #2018
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+"/"+k 
            #1.json
            Data = open(p_k,'r')
            D=json.load(Data)
            for district, values in D['data']['hoverData'].items():
                Name = district
                count = values['registeredUsers']
                open_app = values['appOpens']
                clm['District_name'].append(Name)
                clm['Registered_Users_Count'].append(count)
                clm['Apps_Open'].append(open_app)
                clm['State'].append(i)
                clm['Year'].append(j)
                clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
map_user =pd.DataFrame(clm)

map_user['State'] = map_user['State'].str.strip().str.lower()
map_user['State'] = map_user['State'].replace(state_name_map)

user_df = map_user.groupby('State', as_index=False).agg({'Registered_Users_Count': 'sum'})
df_insurance = Map_Insu_state.groupby('State', as_index=False).agg({'Insurance_count': 'sum'})
#We can do like this too df_insurance = Map_Insu_state.groupby('State', as_index=False)['Insurance_count'].sum()

engagement_insurance = pd.merge(user_df, df_insurance, on="State", how="inner")
engagement_insurance['Insurance_Engagement_%'] = (engagement_insurance['Insurance_count'] / engagement_insurance['Registered_Users_Count']) * 100
engagement_insurance = engagement_insurance.sort_values(by='Insurance_Engagement_%', ascending=False)

engagement_insurance_fig = px.bar(
    engagement_insurance.sort_values(by="Insurance_Engagement_%", ascending=False),
    x="State", 
    y="Insurance_Engagement_%", 
    title="Percentage of PhonePe Users Engaging in Insurance",
    labels={"Insurance_Engagement_%": "% Engaged"}
)
#st.plotly_chart(engagement_insurance_fig, use_container_width=True)