import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime,timedelta
import calendar

st.set_page_config(
    page_title="MTA Subway Ridership Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main-header {
            font-size:2.5rem;
            color:#1f77b4;
            text-align: center;
            margin-bottom:2rem;
        }
        .metric-card{
            background-color:#f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
        }
        .sidebar-header{
            font-size: 1.2rem;
            font-weight: bold;
            color: #1f77b4;
        }
    </style>
""",unsafe_allow_html=True)

st.markdown('<h1 class="main-header">MTA Subway Ridership Dashboard</h1>',unsafe_allow_html=True)
st.markdown("""
Welcome to the interactive MTA Subway Ridership Dashboard.This dashboard provides comprehensive insights 
into NYC subway ridership patterns, trends, and analytics for 2022 Feb - 2023 Jul
""")

st.sidebar.markdown('<p class="sidebar-header">Dashboard Filters</p>', unsafe_allow_html=True)

@st.cache_data

def load_data():
    """Load MTA DATA"""
    try:
        df=pd.read_parquet('/Users/gga/mta_hourly_2022.parquet')
        return preprocess_data(df)
    except FileNotFoundError:
        st.warning("Original MTA data file not found. Using sample data for demonstration.")
        return create_sample_data()
    
def preprocess_data(df):
    #copy of df
    df=df.copy()

    # map borough abbrv. to full names
    mapping={'BK':'Brooklyn','M':'Manhattan','BX':'Bronx','Q':'Queens'}
    for abbrev,full_name in mapping.items():
        df['borough']=df['borough'].replace(abbrev,full_name)
    # Process timestamp
    if 'transit_timestamp' in df.columns:
        df['transit_timestamp']=df['transit_timestamp'].str.split(pat=' ')
        df['date']=[x[0] for x in df['transit_timestamp']]
        df['time']=[x[1]+ " "+x[2] for x in df['transit_timestamp']]
        df['date']=pd.to_datetime(df['date'], format="%m/%d/%Y")
        df['time']=pd.to_datetime(df['time'], format='%I:%M:%S %p').dt.time
        df['full_datetime']=df['date'].astype(str)+ ' '+df['time'].astype(str)
        df['full_datetime']=pd.to_datetime(df['full_datetime'],errors='coerce')

    if 'date' in df.columns:
        df['month']=df['date'].dt.to_period('M').astype(str)
        df['day_of_week']=df['date'].dt.day_name()

    return df

def create_sample_data():
    np.random.seed(42)

    stations = [
        {'station_complex': 'Times Sq-42 St', 'borough': 'Manhattan', 'latitude': 40.7580, 'longitude': -73.9855},
        {'station_complex': 'Grand Central-42 St', 'borough': 'Manhattan', 'latitude': 40.7527, 'longitude': -73.9772},
        {'station_complex': 'Penn Station', 'borough': 'Manhattan', 'latitude': 40.7505, 'longitude': -73.9934},
        {'station_complex': 'Union Sq-14 St', 'borough': 'Manhattan', 'latitude': 40.7359, 'longitude': -73.9911},
        {'station_complex': 'Atlantic Av-Barclays Ctr', 'borough': 'Brooklyn', 'latitude': 40.6838, 'longitude': -73.9777},
        {'station_complex': 'Jackson Heights-Roosevelt Av', 'borough': 'Queens', 'latitude': 40.7480, 'longitude': -73.9304},
        {'station_complex': 'Fordham Rd', 'borough': 'Bronx', 'latitude': 40.8618, 'longitude': -73.8867},
    ]

    start_date=datetime(2022,1,1)
    end_date=datetime(2023,7,17)
    date_range = pd.date_range(start_date, end_date, freq='D')

    data=[]
    for date in date_range:
        for station in stations:
            day_of_week=date.weekday()
            base_ridership=50000 if station['borough'] == 'Manhattan' else 20000

            if day_of_week>=5:
                base_ridership*=0.7

            ridership=int(base_ridership * (1+np.random.normal(0,0.2)))
            ridership=max(1000,ridership)

            data.append({
                'station_complex':station['station_complex'],
                'borough':station['borough'],
                'latitude':station['latitude'],
                'longitude':station['longitude'],
                'date':date,
                'ridership':ridership,
                'month':date.strftime('%Y-%m'),
                'day_of_week': date.strftime('%A'),
                'time': datetime.now().time()
            })
    
    return pd.DataFrame(data)

df=load_data()

st.sidebar.markdown("Date Range")
min_date=df['date'].min().date()
max_date=df['date'].max().date()

start_date=st.sidebar.date_input(
    "Start Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)

end_date=st.sidebar.date_input(
    "End Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)
st.sidebar.markdown("Borough Selection")
all_boroughs=['All']+list(df['borough'].unique())
selected_borough=st.sidebar.selectbox("Select Borough",all_boroughs)

st.sidebar.markdown(" Station Selection")
if selected_borough == 'All':
    all_stations = ['All'] + list(df['station_complex'].unique())
else:
    borough_stations = df[df['borough'] == selected_borough]['station_complex'].unique()
    all_stations = ['All'] + list(borough_stations)
selected_station = st.sidebar.selectbox("Select Station", all_stations)

filtered_df=df[
    (df['date']>=pd.to_datetime(start_date)) & (df['date']<=pd.to_datetime(end_date))
]

if selected_borough != 'All':
    filtered_df=filtered_df[filtered_df['borough']== selected_borough]

if selected_station != 'All':
    filtered_df=filtered_df[filtered_df['station_complex']==selected_station]

st.markdown("Key Metrics")
col1,col2,col3,col4=st.columns(4)

with col1:
    total_ridership=filtered_df['ridership'].sum()
    st.metric("Total Ridership",f"{total_ridership:,.0f}")

with col2:
    avg_daily_ridership=filtered_df.groupby('date')['ridership'].sum().mean()
    st.metric("Avg Daily Ridership",f"{avg_daily_ridership:,.0f}")

with col3:
    total_stations=filtered_df['station_complex'].nunique()
    st.metric("Active Stations",total_stations)

with col4:
    peak_day=filtered_df.groupby('date')['ridership'].sum().idxmax()
    peak_ridership=filtered_df.groupby('date')['ridership'].sum().max()
    st.metric("Peak Day",f"{peak_ridership:,.0f}")

tab1,tab2,tab3,tab4,tab5=st.tabs(["Trends","Geographic","Borough Analysis","Time Analysis","Top Stations"])

with tab1:
    st.markdown("Ridership Trends Over Time")

    daily_ridership=filtered_df.groupby('date')['ridership'].sum().reset_index()

    fig_trend=px.line(
        daily_ridership,
        x='date',
        y='ridership',
        title='Daily Ridership Trend',
        labels={'ridership':'Total Ridership','date':'Date'}
    )
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, width='stretch')

    monthly_ridership=filtered_df.groupby('month')['ridership'].sum().reset_index()

    fig_monthly=px.bar(
        monthly_ridership,
        x='month',
        y='ridership',
        title='Monthly Ridership Comparison',
        labels={'ridership':'Total Ridership','month':'Month'}
    )
    fig_monthly.update_layout(height=400)
    st.plotly_chart(fig_monthly, width='stretch')

with tab2:
    st.markdown("Geographic Distribution")

    station_ridership = filtered_df.groupby(['station_complex', 'latitude', 'longitude', 'borough'])['ridership'].sum().reset_index()

    fig_map = px.scatter_map(
        station_ridership,
        lat='latitude',
        lon='longitude',
        size='ridership',
        color='borough',
        hover_name='station_complex',
        hover_data=['ridership', 'borough'],
        zoom=10,
        height=600,
        title='Subway Station Ridership Map'
    )

    fig_map.update_layout(map_style='open-street-map')
    st.plotly_chart(fig_map, width='stretch')

    st.markdown("Ridership Heat Map")
    fig_heatmap=px.density_mapbox(
        station_ridership,
        lat='latitude',
        lon='longitude',
        z='ridership',
        hover_name='station_complex',
        radius=20,
        zoom=10,
        mapbox_style='open-street-map',
        height=500,
        title='Ridership Density Heat Map'
    )
    st.plotly_chart(fig_heatmap, width='stretch')

with tab3:
    st.markdown("Borough Analysis")

    borough_ridership=filtered_df.groupby('borough')['ridership'].sum().reset_index()
    borough_ridership=borough_ridership.sort_values('ridership', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig_borough_bar=px.bar(
            borough_ridership,
            x='borough',
            y='ridership',
            title='Total Ridership by Borough',
            labels={'ridership': 'Total Ridership', 'borough': 'Borough'}
        )
        fig_borough_bar.update_layout(height=400)
        st.plotly_chart(fig_borough_bar, width='stretch')

    with col2:
        fig_borough_pie=px.pie(
            borough_ridership,
            values='ridership',
            names='borough',
            title='Ridership Distribution by Borough'
        )
        fig_borough_pie.update_layout(height=400)
        st.plotly_chart(fig_borough_pie, width='stretch')

with tab4:
    st.markdown("Time-Based Analysis")
    
    # Day of week analysis
    day_ridership = filtered_df.groupby('day_of_week')['ridership'].sum().reset_index()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_ridership['day_of_week'] = pd.Categorical(day_ridership['day_of_week'], categories=day_order, ordered=True)
    day_ridership = day_ridership.sort_values('day_of_week')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_day_bar = px.bar(
            day_ridership,
            x='day_of_week',
            y='ridership',
            title='Ridership by Day of Week',
            labels={'ridership': 'Total Ridership', 'day_of_week': 'Day of Week'}
        )
        fig_day_bar.update_layout(height=400)
        st.plotly_chart(fig_day_bar, width='stretch')
    
    with col2:
        
        total_days = (end_date - start_date).days + 1
        day_ridership['avg_ridership'] = day_ridership['ridership'] / max(1, total_days // 7)
        
        fig_day_avg = px.bar(
            day_ridership,
            x='day_of_week',
            y='avg_ridership',
            title='Average Ridership by Day of Week',
            labels={'avg_ridership': 'Average Daily Ridership', 'day_of_week': 'Day of Week'}
        )
        fig_day_avg.update_layout(height=400)
        st.plotly_chart(fig_day_avg, width='stretch')

with tab5:
    st.markdown("Top Performing Stations")
    
    # Top stations by ridership
    top_stations = filtered_df.groupby(['station_complex', 'borough'])['ridership'].sum().reset_index()
    top_stations = top_stations.sort_values('ridership', ascending=False).head(20)
    
    # Table view
    st.markdown("Top 20 Stations by Total Ridership")
    fig_table = go.Figure(data=[go.Table(
        header=dict(values=["Rank", "Station Name", "Borough", "Total Ridership"],
                   fill_color='lightblue',
                   align='left'),
        cells=dict(values=[
            list(range(1, len(top_stations) + 1)),
            top_stations['station_complex'],
            top_stations['borough'],
            [f"{x:,.0f}" for x in top_stations['ridership']]
        ],
        fill_color='lavender',
        align='left'))
    ])
    
    fig_table.update_layout(height=600)
    st.plotly_chart(fig_table, width='stretch')

    st.markdown("Top 10 Stations Visualization")
    top_10 = top_stations.head(10)
    
    fig_top_stations = px.bar(
        top_10,
        x='ridership',
        y='station_complex',
        orientation='h',
        title='Top 10 Stations by Ridership',
        labels={'ridership': 'Total Ridership', 'station_complex': 'Station'},
        color='borough'
    )
    fig_top_stations.update_layout(height=500)
    st.plotly_chart(fig_top_stations, width='stretch')

st.markdown("Key Insights")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
     Trend Analysis
    - **Peak Periods**: Identify high ridership periods
    - **Seasonal Patterns**: Monthly variations in ridership
    - **Growth Trends**: Year-over-year comparisons
    """)

with col2:
    st.markdown("""
    Operational Insights
    - **Busiest Stations**: High-traffic locations
    - **Borough Distribution**: Geographic ridership patterns
    - **Optimal Timing**: Peak usage hours and days
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>MTA Subway Ridership Dashboard | Data Analysis & Visualization</p>
    <p>For optimal performance, ensure your MTA data file is in the same directory as this script.</p>
</div>
""", unsafe_allow_html=True)

# Instructions for data loading
with st.expander("Data Loading Instructions"):
    st.markdown("""
    ### How to load your actual MTA data:
    
    1. **Place your CSV file** in the same directory as this script
    2. **Rename the file** to `MTA_Subway_HourlyBeginning_February_2022.csv`
    3. **Restart the app** to load the real data
    
    ### Expected CSV columns:
    - `transit_timestamp`: Timestamp data
    - `station_complex`: Station name
    - `borough`: Borough abbreviation (BK, M, BX, Q)
    - `latitude`: Station latitude
    - `longitude`: Station longitude
    - `ridership`: Number of riders
    
    ### Data Processing:
    The dashboard automatically:
    - Converts borough abbreviations to full names
    - Processes timestamps and creates date/time columns
    - Adds derived columns (month, day_of_week)
    - Handles missing values and data cleaning
    """)
