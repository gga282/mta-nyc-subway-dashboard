# MTA Subway Ridership Dashboard

An interactive Streamlit dashboard for analyzing NYC subway ridership patterns and trends.

## Features

### Key Metrics
- Total ridership across selected time period
- Average daily ridership
- Number of active stations
- Peak day ridership

### Interactive Visualizations
1. **Trends Tab**: Daily and monthly ridership trends
2. **Geographic Tab**: Interactive maps and heat maps
3. **Borough Analysis**: Comparative analysis by borough
4. **Time Analysis**: Day-of-week patterns
5. **Top Stations**: Ranking of busiest stations

### Interactive Filters
- **Date Range**: Select custom time periods
- **Borough Selection**: Filter by specific boroughs
- **Station Selection**: Drill down to individual stations

## Quick Start

### 1. Install Dependencies
```bash
pip install streamlit plotly pandas numpy
```

### 2. Run the Dashboard
```bash
streamlit run mta_dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Data Setup

### Using Sample Data
The dashboard includes sample MTA-like data for immediate demonstration. It will automatically use this data if your actual MTA file is not found.

### Loading Your MTA Data
To use your actual MTA subway data:

1. **Place your CSV file** in the same directory as `mta_dashboard.py`
2. **Rename the file** to: `MTA_Subway_HourlyBeginning_February_2022.csv`
3. **Restart the dashboard** to load the real data

### Expected CSV Structure
Your CSV file should contain these columns:
- `transit_timestamp`: Timestamp data (e.g., "02/01/2022 12:00:00 AM")
- `station_complex`: Station name
- `borough`: Borough abbreviation (BK, M, BX, Q)
- `latitude`: Station latitude
- `longitude`: Station longitude
- `ridership`: Number of riders

## Dashboard Sections

### Key Metrics (Top)
Real-time metrics that update based on your filter selections:
- Total ridership for selected period
- Average daily ridership
- Number of active stations
- Peak day and ridership

### Trends Tab
- **Daily Trend Line**: Shows ridership patterns over time
- **Monthly Bar Chart**: Compares ridership across months

### Geographic Tab
- **Interactive Map**: Scatter plot showing station locations and ridership
- **Heat Map**: Density visualization of ridership patterns

### Borough Analysis Tab
- **Bar Chart**: Total ridership by borough
- **Pie Chart**: Percentage distribution across boroughs

### Time Analysis Tab
- **Day of Week**: Total ridership by weekday
- **Average Daily**: Mean ridership patterns

### Top Stations Tab
- **Ranking Table**: Top 20 stations by ridership
- **Bar Chart**: Visual representation of top 10 stations

## Technical Details

### Data Processing
The dashboard automatically:
- Converts borough abbreviations to full names (BK→Brooklyn, M→Manhattan, etc.)
- Processes timestamps and creates date/time columns
- Adds derived columns (month, day_of_week)
- Handles missing values and data cleaning

### Performance Features
- **Caching**: Data is cached for faster performance
- **Responsive Design**: Works on desktop and mobile
- **Interactive Filters**: Real-time data updates

## Customization

### Styling
The dashboard uses custom CSS for a professional appearance:
- Clean, modern interface
- Consistent color scheme
- Responsive layout

### Adding New Features
You can extend the dashboard by:
- Adding new visualization tabs
- Including additional filters
- Adding more metrics
- Integrating external data sources

## Troubleshooting

### Common Issues

1. **Data Not Loading**
   - Ensure CSV file is in the correct directory
   - Check file name matches exactly
   - Verify CSV has required columns

2. **Map Not Displaying**
   - Check internet connection for map tiles
   - Verify latitude/longitude data is valid

3. **Performance Issues**
   - Try reducing date range
   - Install watchdog for better file watching: `pip install watchdog`

### Getting Help
- Check the "Data Loading Instructions" expander in the dashboard
- Review the console output for error messages
- Ensure all dependencies are installed

## License

This dashboard is created for educational and demonstration purposes. Feel free to modify and adapt it for your specific needs.

## Contributing

To contribute improvements:
1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This dashboard was created based on MTA subway ridership analysis patterns. It's designed to work with the specific data structure from the original analysis notebook.
