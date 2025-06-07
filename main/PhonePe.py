import streamlit as st
import os
import sys
import plotly.express as px

st.set_page_config(layout="wide", page_title="PhonePe India Data")
st.title("📊 Phone Pe Data Analysis Dashboard")
st.write("""
Welcome to the PhonePe Data Analysis Dashboard.      
This interactive Streamlit app provides insights into PhonePe data insights across Indian states. Select a topic from the dropdown below to explore detailed visualizations and make data-driven observations.
""")

# Add the parent directory (i.e., project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extract_data import aggregated_insurance
from extract_data import aggregated_transaction
from extract_data import aggregated_user
from extract_data import map_insurance
from extract_data import map_transaction
from extract_data import map_user

# Dropdown to select which figure to show
options = [
    "Device Dominance and User Engagement Analysis",
    "Insurance Penetration and Growth Potential Analysis",
    "Decoding Transaction Dynamics on PhonePe",
    "User Engagement and Growth Strategy",
    "Transaction Analysis for Market Expansion",
    "Insurance Engagement Analysis",
]

selected = st.selectbox("Select a Visualization", options)
# ---------- Display Based on Selection ----------

if selected == "Device Dominance and User Engagement Analysis":
    st.plotly_chart(aggregated_user.Agg_User_fig, use_container_width=True)
    st.subheader("Top 10 States by User Count")
    st.dataframe(aggregated_user.top_10_df)
    st.subheader("Least 10 States by User Count")
    st.dataframe(aggregated_user.bottom_10_df)

    # Dropdown to select a state
    selected_state = st.selectbox("Select a State to View Device Brand Usage", aggregated_user.Agg_User_state['State'].unique())

    # Filter data for selected state
    filtered_data = aggregated_user.Agg_User_state[aggregated_user.Agg_User_state['State'] == selected_state]

    # Group by Mobile Brand and sum usage count
    brand_summary = (
        filtered_data
        .groupby('Mobile_Brand_Used', as_index=False)
        .agg({'Usage_count': 'sum'})
    )

    # Bar chart for the selected state
    brand_fig = px.bar(
        brand_summary,
        x="Mobile_Brand_Used",
        y="Usage_count",
        title=f"Device Brand Usage in {selected_state}",
        color="Mobile_Brand_Used"
    )

    st.plotly_chart(brand_fig, use_container_width=True)

    st.subheader("User Preferences Across Different Mobile Device Brands")
    st.plotly_chart(aggregated_user.brand_fig, use_container_width=True)

if selected == "Insurance Penetration and Growth Potential Analysis":
    st.plotly_chart(aggregated_insurance.Agg_Insu_fig, use_container_width=True)
    st.subheader("Top 10 States by Insurance Count")
    st.dataframe(aggregated_insurance.top_10_df)
    st.subheader("Least 10 States by Insurance Count")
    st.dataframe(aggregated_insurance.bottom_10_df)
    st.plotly_chart(map_insurance.Map_Insu_fig, use_container_width=True)
    st.subheader("Top 10 States by Insurance Amount")
    st.dataframe(map_insurance.top_10_df)
    st.subheader("Least 10 States by Insurance Amount")
    st.dataframe(map_insurance.bottom_10_df)

    st.subheader("State-wise Insurance Users Growth Trend")
    # Display statewise users growth trend

    # Dropdown to select a state
    selected_state = st.selectbox("Select a State to View Growth Trend", aggregated_insurance.Agg_Insu_state['State'].unique())

    # Filter data for selected state
    filtered_state_yearly = aggregated_insurance.Agg_Insu_state[aggregated_insurance.Agg_Insu_state['State'] == selected_state]

    state_yearly = (
        filtered_state_yearly
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
        markers=True
    )
    st.plotly_chart(fig_state_trend, use_container_width=True)

    st.subheader("Comparision of Growth Trend in Insurance Count of All States")
    st.plotly_chart(aggregated_insurance.fig_state_trend, use_container_width=True)

if selected == "Decoding Transaction Dynamics on PhonePe":
    st.plotly_chart(aggregated_transaction.Agg_Trans_fig, use_container_width=True)
    st.subheader("Top 10 States by transaction Count")
    st.dataframe(aggregated_transaction.top_10_df)
    st.subheader("Least 10 States by transaction Count")
    st.dataframe(aggregated_transaction.bottom_10_df)
    st.plotly_chart(map_transaction.Map_Trans_fig, use_container_width=True)
    st.subheader("Top 10 States by Total Transaction Amount")
    st.dataframe(map_transaction.top_10_df)
    st.subheader("Least 10 States by Total Transaction Amount")
    st.dataframe(map_transaction.bottom_10_df)
    st.subheader("Year-Quarter vs Transaction_count")
    st.plotly_chart(aggregated_transaction.quarter_fig, use_container_width=True)
    st.plotly_chart(aggregated_transaction.payment_category_count_fig, use_container_width=True)
    st.plotly_chart(aggregated_transaction.payment_category_amount_fig, use_container_width=True)

if selected == "User Engagement and Growth Strategy":
    st.plotly_chart(map_user.Map_User_Register_fig, use_container_width=True)
    st.subheader("Top 10 States by Registered User Count")
    st.dataframe(map_user.top_10_df)
    st.subheader("Least 10 States by Registered User Count")
    st.dataframe(map_user.bottom_10_df)
    st.plotly_chart(map_user.Map_User_Apps_fig, use_container_width=True)
    st.subheader("Top 10 States by Apps Opened")
    st.dataframe(map_user.top_10_apps_open_df)
    st.subheader("Least 10 States by Apps Opened")
    st.dataframe(map_user.bottom_10_apps_open_df)
    st.plotly_chart(map_user.Map_User_Engagement_fig, use_container_width=True)
    st.subheader("Top 10 States by Engagement Ratio")
    st.dataframe(map_user.top_10_engagement_ratio_df)
    st.subheader("Least 10 States by Engagement Ratio")
    st.dataframe(map_user.bottom_10_engagement_ratio_df)

if selected == "Insurance Engagement Analysis":
    st.plotly_chart(aggregated_insurance.Agg_Insu_fig, use_container_width=True)
    st.subheader("Top 10 States by Insurance Count")
    st.dataframe(aggregated_insurance.top_10_df)
    st.subheader("Least 10 States by Insurance Count")
    st.dataframe(aggregated_insurance.bottom_10_df)
    st.plotly_chart(map_insurance.Map_Insu_fig, use_container_width=True)
    st.subheader("Top 10 States by Insurance Amount")
    st.dataframe(map_insurance.top_10_df)
    st.subheader("Least 10 States by Insurance Amount")
    st.dataframe(map_insurance.bottom_10_df)

    st.subheader("State-wise Insurance Users Growth Trend")
    # Display statewise users growth trend

    # Dropdown to select a state
    selected_state = st.selectbox("Select a State to View Growth Trend", aggregated_insurance.Agg_Insu_state['State'].unique())

    # Filter data for selected state
    filtered_state_yearly = aggregated_insurance.Agg_Insu_state[aggregated_insurance.Agg_Insu_state['State'] == selected_state]

    state_yearly = (
        filtered_state_yearly
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
        markers=True
    )
    st.plotly_chart(fig_state_trend, use_container_width=True)

    st.subheader("Comparision of Growth Trend in Insurance Count of All States")
    st.plotly_chart(aggregated_insurance.fig_state_trend, use_container_width=True)
    st.plotly_chart(map_insurance.engagement_insurance_fig, use_container_width=True)

if selected == "Transaction Analysis for Market Expansion":
    st.plotly_chart(aggregated_transaction.Agg_Trans_fig, use_container_width=True)
    st.subheader("Top 10 States by transaction Count")
    st.dataframe(aggregated_transaction.top_10_df)
    st.subheader("Least 10 States by transaction Count")
    st.dataframe(aggregated_transaction.bottom_10_df)
    st.plotly_chart(map_transaction.Map_Trans_fig, use_container_width=True)
    st.subheader("Top 10 States by Total Transaction Amount")
    st.dataframe(map_transaction.top_10_df)
    st.subheader("Least 10 States by Total Transaction Amount")
    st.dataframe(map_transaction.bottom_10_df)

    st.subheader("State-wise Transaction Amount Growth Trend")
    # Display statewise growth trend

    # Dropdown to select a state
    selected_state = st.selectbox("Select a State to View Growth Trend", map_transaction.Map_trans_state['State'].unique())

    # Filter data for selected state
    filtered_state_yearly = map_transaction.Map_trans_state[map_transaction.Map_trans_state['State'] == selected_state]

    state_yearly = (
        filtered_state_yearly
        .groupby(['State', 'Year'], as_index=False)
        .agg({'Transaction_amount': 'sum'})
        )
    state_yearly['Year'] = state_yearly['Year'].astype(int)

    # Line chart
    fig_state_trend = px.line(
        state_yearly,
        x='Year',
        y='Transaction_amount',
        color='State',
        markers=True
    )
    st.plotly_chart(fig_state_trend, use_container_width=True)

    st.subheader("Comparision of Growth Trend in Transaction Amount of All States")
    st.plotly_chart(map_transaction.fig_state_trend_total, use_container_width=True)
