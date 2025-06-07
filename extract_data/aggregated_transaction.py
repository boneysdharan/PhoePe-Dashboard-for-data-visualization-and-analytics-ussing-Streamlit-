import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

#st.set_page_config(layout="wide")
#st.title("Aggregated Transaction Data - State-wise (India Map)")

path=r"D:/BONEYS/WEB/PYTHON/Project/PhonePe/data/aggregated/transaction/country/india/state"
Agg_state_list=os.listdir(path)

#This is to extract the data's to create a dataframe
clm={'State':[], 'Year':[],'Quater':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}

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
              clm['Transaction_type'].append(Name)
              clm['Transaction_count'].append(count)
              clm['Transaction_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Trans_state=pd.DataFrame(clm)

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
Agg_Trans_state['State'] = Agg_Trans_state['State'].str.strip().str.lower()
Agg_Trans_state['State'] = Agg_Trans_state['State'].replace(state_name_map)

top_10_df = (
    Agg_Trans_state.groupby("State")["Transaction_count"]
    .sum()
    .reset_index()
    .sort_values(by="Transaction_count", ascending=False)
    .head(10))
top_10_df = top_10_df.reset_index(drop=True)  # Drop old index
top_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_agg_trans_top10"):
    st.subheader("Top 10 States by transaction Count")
    st.dataframe(top_10_df)
"""
bottom_10_df = (
    Agg_Trans_state.groupby("State")["Transaction_count"]
    .sum()
    .reset_index()
    .sort_values(by="Transaction_count", ascending=True)
    .head(10))
bottom_10_df = bottom_10_df.reset_index(drop=True)  # Drop old index
bottom_10_df.index += 1
# Show Data Preview
"""
if st.checkbox("Show Raw Data", key="raw_data_agg_trans_bottom10"):
    st.subheader("Least 10 States by transaction Count")
    st.dataframe(bottom_10_df)
"""
# Load GeoJSON data from URL
#FINDING TRANSACTION COUNT VS STATE
state_summary = (
    Agg_Trans_state
    .groupby('State', as_index=False)
    .agg({'Transaction_count': 'sum'})
)

#Plot data
Agg_Trans_fig = px.choropleth(
    state_summary,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Transaction_count',
    color_continuous_scale='Blues',
    title='Total Transaction Count by State'
)

Agg_Trans_fig.update_geos(fitbounds="locations", visible=False)
# Display in Streamlit
#st.plotly_chart(Agg_Trans_fig, use_container_width=True)

#FINDING TRANSACTION COUNT VS YEAR-QUARTER
# Combine Year and Quarter to create a single time dimension (e.g., 2021-Q1)
Agg_Trans_state['Year_Quarter'] = Agg_Trans_state['Year'].astype(str) + '-Q' + Agg_Trans_state['Quater'].astype(str)

# Group by Year_Quarter and aggregate Transaction_count
quarter_summary = (
    Agg_Trans_state
    .groupby('Year_Quarter', as_index=False)
    .agg({'Transaction_count': 'sum'})
    .sort_values('Year_Quarter')
)

quarter_fig = px.line(
    quarter_summary,
    x='Year_Quarter',
    y='Transaction_count',
    title='Transaction Trends by Quarter',
    markers=True
)

# Display in Streamlit
#st.plotly_chart(quarter_fig, use_container_width=True)

#Finding Category wise transactions based on transaction count
payment_category_count_summary = (
    Agg_Trans_state
    .groupby('Transaction_type', as_index=False)
    .agg({'Transaction_count': 'sum'})
    .sort_values('Transaction_count', ascending=False)
)
payment_category_count_fig = px.bar(
    payment_category_count_summary,
    x='Transaction_type',
    y='Transaction_count',
    color='Transaction_type',
    title='Total Transaction Count by Payment Category'
)

#st.plotly_chart(payment_category_count_fig, use_container_width=True)

#Finding Category wise transactions based on transaction amount
payment_category_amount_summary = (
    Agg_Trans_state
    .groupby('Transaction_type', as_index=False)
    .agg({'Transaction_amount': 'sum'})
    .sort_values('Transaction_amount', ascending=False)
)
payment_category_amount_fig = px.bar(
    payment_category_amount_summary,
    x='Transaction_type',
    y='Transaction_amount',
    color='Transaction_type',
    title='Total Transaction Amount by Payment Category'
)
#st.plotly_chart(payment_category_amount_fig, use_container_width=True)
