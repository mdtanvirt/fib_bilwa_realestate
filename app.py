import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk 
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

# Hide streamlit default menu and footer from the template
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden}
    footer {visibility: hidden}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

data = pd.read_csv('WestEnd_merged_full new.csv')
#st.dataframe(data)

###########

with st.sidebar:
    st. title("Real estate analyzer")
    nav_menu = option_menu("Main Menu", ["Dashboard", "Map Analyzer"], 
        icons=['clipboard-data', 'map', 'gear'], menu_icon="cast", default_index=0)
    

if nav_menu == 'Dashboard':

    chart_data = data.filter(['Lat', 'Lon', 'Distance to Flood', 'Adjacent Bus Station', 'Street_Name', 'Point_ID', 'Max_Speed'])

    filter_enable = st.checkbox('Enable filtering option')

    if filter_enable:

        options_for_street_name = chart_data['Street_Name'].unique().tolist()
        selected_options_streets = st.multiselect('Select Street Name(You can modify defailt selection)',options_for_street_name, default=options_for_street_name[0:5])

        chart_data = chart_data.query('Street_Name == @selected_options_streets')

        ## card matrix 

        col_total_points, col_max_speed, col_distance_flood, col_bus_stand = st.columns(4)
        
        with col_total_points:
            total_point_count = chart_data['Point_ID'].value_counts().sum().round(2)
            st.metric(label = 'Total real-estate points', value= total_point_count)
        
        with col_max_speed:
            average_speed = chart_data['Max_Speed'].mean().round(2)
            st.metric(label = 'Average speed in Kilo Miter (KM)', value= average_speed)
            
        with col_distance_flood:
            average_dist_flood = chart_data['Distance to Flood'].mean().round(2)
            st.metric(label = 'Average distance to flood in Miter (M)', value= average_dist_flood)
        
        with col_bus_stand:
            max_bus_stand = chart_data['Adjacent Bus Station'].max().round(2)
            st.metric(label = 'Max number of bus station', value= max_bus_stand)

        ## End of card matrix


        midpoint = (np.average(data["Lat"]), np.average(data["Lon"]))

        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=midpoint[0],
                longitude=midpoint[1],
                zoom=12,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                'HexagonLayer',
                data=chart_data,
                get_position='[Lon, Lat]',
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=chart_data,
                    get_position='[Lon, Lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=100,
                ),
            ],
        ))
    
    else:

        ## Card matrix
        col_total_points, col_max_speed, col_distance_flood, col_bus_stand = st.columns(4)
        
        with col_total_points:
            total_point_count = chart_data['Point_ID'].value_counts().sum().round(2)
            st.metric(label = 'Total real-estate points', value= total_point_count)
        
        with col_max_speed:
            average_speed = chart_data['Max_Speed'].mean().round(2)
            st.metric(label = 'Average speed in Kilo Miter (KM)', value= average_speed)
            
        with col_distance_flood:
            average_dist_flood = chart_data['Distance to Flood'].mean().round(2)
            st.metric(label = 'Average distance to flood in Miter (M)', value= average_dist_flood)
        
        with col_bus_stand:
            max_bus_stand = chart_data['Adjacent Bus Station'].max().round(2)
            st.metric(label = 'Max number of bus station', value= max_bus_stand)

        ## End of card matrix

        midpoint = (np.average(data["Lat"]), np.average(data["Lon"]))

        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=midpoint[0],
                longitude=midpoint[1],
                zoom=12,
                pitch=40,
            ),
            layers=[
                pdk.Layer(
                'HexagonLayer',
                data=chart_data,
                get_position='[Lon, Lat]',
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=chart_data,
                    get_position='[Lon, Lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=100,
                ),
            ],
        ))

elif nav_menu == 'Map Analyzer':
    st.write("Map Analyzer")