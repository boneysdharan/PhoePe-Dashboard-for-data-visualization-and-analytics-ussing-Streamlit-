import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

#st.set_page_config(layout="wide")
#st.title("Map User Data - State-wise (India Map)")

path=r"D:/BONEYS/WEB/PYTHON/Project/PhonePe/data/map/user/hover/country/india/state"
Map_user_state_list=os.listdir(path)

#This is to extract the data's to create a dataframe
clm={'State':[], 'Year':[],'Quater':[],'District_name':[], 'Registered_Users_Count':[], 'Apps_Open':[]}

for i in Map_user_state_list:
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
Map_user_state=pd.DataFrame(clm)

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
Map_user_state['State'] = Map_user_state['State'].str.strip().str.lower()
Map_user_state['State'] = Map_user_state['State'].replace(state_name_map)

top_10_df = (
    Map_user_state.groupby("State")["Registered_Users_Count"]
    .sum()
    .reset_index()
    .sort_values(by="Registered_Users_Count", ascending=False)
    .head(10))
top_10_df = top_10_df.reset_index(drop=True)  # Drop old index
top_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_map_user_top10"):
    st.subheader("Top 10 States by Registered User Count")
    st.dataframe(top_10_df)
"""

top_10_apps_open_df = (
    Map_user_state.groupby("State")["Apps_Open"]
    .sum()
    .reset_index()
    .sort_values(by="Apps_Open", ascending=False)
    .head(10))
top_10_apps_open_df = top_10_apps_open_df.reset_index(drop=True)  # Drop old index
top_10_apps_open_df.index += 1

bottom_10_df = (
    Map_user_state.groupby("State")["Registered_Users_Count"]
    .sum()
    .reset_index()
    .sort_values(by="Registered_Users_Count", ascending=True)
    .head(10))
# Show Data Preview
bottom_10_df = bottom_10_df.reset_index(drop=True)  # Drop old index
bottom_10_df.index += 1
"""
if st.checkbox("Show Raw Data", key="raw_data_map_user_bottom10"):
    st.subheader("Least 10 States by Registered User Count")
    st.dataframe(bottom_10_df)
"""

bottom_10_apps_open_df = (
    Map_user_state.groupby("State")["Apps_Open"]
    .sum()
    .reset_index()
    .sort_values(by="Apps_Open", ascending=True)
    .head(10))
bottom_10_apps_open_df = bottom_10_apps_open_df.reset_index(drop=True)  # Drop old index
bottom_10_apps_open_df.index += 1
# Load GeoJSON data from URL
# Plot Total Registered_Users_Count by State
state_register_summary = (
    Map_user_state
    .groupby('State', as_index=False)
    .agg({'Registered_Users_Count': 'sum'})
)

Map_User_Register_fig = px.choropleth(
    state_register_summary,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Registered_Users_Count',
    color_continuous_scale='Greens',
    title='Total Registered_Users_Count by State'
)

Map_User_Register_fig.update_geos(fitbounds="locations", visible=False)

# Display in Streamlit
#st.plotly_chart(Map_User_Register_fig, use_container_width=True)

# Plot Total Apps_Open by State
state_apps_summary = (
    Map_user_state
    .groupby('State', as_index=False)
    .agg({'Apps_Open': 'sum'})
)

Map_User_Apps_fig = px.choropleth(
    state_apps_summary,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Apps_Open',
    color_continuous_scale='Reds',
    title='Total Apps_Open by State'
)

Map_User_Apps_fig.update_geos(fitbounds="locations", visible=False)

# Display in Streamlit
#st.plotly_chart(Map_User_Apps_fig, use_container_width=True)

#Engagement rate, a key metric for assessing content interaction, 
#is calculated as total engagements divided by the relevant base (reach, impressions, followers, or posts)
#In our case, finding engagement ration we get
#engagement ratio = total apps open / total registered users

engagement_df = pd.merge(
    state_register_summary,
    state_apps_summary,
    on='State'
)

engagement_df['Engagement_Ratio'] = engagement_df['Apps_Open'] / engagement_df['Registered_Users_Count']

#top 10 and bottom 10 for engagement ratio 
top_10_engagement_ratio_df = (
    engagement_df.groupby("State")["Engagement_Ratio"]
    .sum()
    .reset_index()
    .sort_values(by="Engagement_Ratio", ascending=False)
    .head(10))
top_10_engagement_ratio_df = top_10_engagement_ratio_df.reset_index(drop=True)  # Drop old index
top_10_engagement_ratio_df.index += 1

bottom_10_engagement_ratio_df = (
    engagement_df.groupby("State")["Engagement_Ratio"]
    .sum()
    .reset_index()
    .sort_values(by="Engagement_Ratio", ascending=True)
    .head(10))
bottom_10_engagement_ratio_df = bottom_10_engagement_ratio_df.reset_index(drop=True)  # Drop old index
bottom_10_engagement_ratio_df.index += 1

#plotting engagement ration on streamlit
Map_User_Engagement_fig = px.choropleth(
    engagement_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Engagement_Ratio',
    color_continuous_scale='Purples',
    title='Engagement Ratio (App Opens per Registered User) by State'
)

Map_User_Engagement_fig.update_geos(fitbounds="locations", visible=False)
#st.plotly_chart(Map_User_Engagement_fig, use_container_width=True)
