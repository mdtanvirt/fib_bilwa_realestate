import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk 
from streamlit_option_menu import option_menu
import math

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
data_rent = pd.read_csv('1_rent_price_cleaned.csv')
data_sold = pd.read_csv('1_sold_price_cleaned.csv')

with st.sidebar:
    st. title("Real estate analyzer")
    nav_menu = option_menu("Main Menu", ["Dashboard", "Map Analyzer"], 
        icons=['clipboard-data', 'map', 'gear'], menu_icon="cast", default_index=0)
    

if nav_menu == 'Dashboard':

    chart_data = data.filter(['Lat', 'Lon', 'Distance to Flood', 'Adjacent Bus Station', 'Street_Name', 'Point_ID', 'Max_Speed'])

    filter_enable = st.checkbox('Enable filtering option')

    if filter_enable:

        options_for_street_name = chart_data['Street_Name'].unique().tolist()
        selected_options_streets = st.multiselect('Select Street Name(You can modify default selection)',options_for_street_name, default=options_for_street_name[0:5])

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
                pitch=10,
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

    enable_rent_ds = st.sidebar.checkbox("Enable filter for RENT dataset")
    
    col_rent, col_sold = st.columns(2)

    with col_rent:

        COLOR_BREWER_BLUE_SCALE = [
            [240, 249, 232],
            [204, 235, 197],
            [168, 221, 181],
            [123, 204, 196],
            [67, 162, 202],
            [8, 104, 172],
        ]

        chart_data = data_rent.filter(['property_ID', 'Lat', 'Lng', 'price', 'kind', 'price_cleaned', 'company'])
        chart_data['company'] = chart_data['company'].fillna('Not a Company')
        chart_data = chart_data.dropna(how='any')

        ## Filtering
        if enable_rent_ds:
            options_for_company = chart_data['company'].unique().tolist()
            selected_options_company = st.sidebar.multiselect('Select Companies(You can modify default selection)',options_for_company, default=options_for_company[0:3])

            chart_data = chart_data.query('company == @selected_options_company')

            ## Card matrix
            col_building_to_rent, col_avg_rent_price = st.columns(2)
            
            with col_building_to_rent:
                total_building_to_rent_count = chart_data['property_ID'].value_counts().sum().round(2)
                st.metric(label = 'Total house to rent', value= total_building_to_rent_count)
            
            with col_avg_rent_price:
                average_rent_price = chart_data['price_cleaned'].mean().round(2)
                st.metric(label = 'Average rent per week ($)', value= average_rent_price)

            ## End of card matrix

            st.write("Most Crowded Area on Map")

            midpoint = (np.average(chart_data["Lat"]), np.average(chart_data["Lng"]))

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=midpoint[0],
                    longitude=midpoint[1],
                    zoom=12.90,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        'HeatmapLayer',
                        data=chart_data,
                        opacity=0.9,
                        get_position='[Lng, Lat]',
                        radius=100,
                        elevation_scale=4,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        get_weight="weight",
                        threshold=1,
                    ),
                    pdk.Layer(
                        'HeatmapLayer',
                        data=chart_data,
                        opacity=0.9,
                        get_position='[Lng, Lat]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=100,
                        pickable=True,
                        #color_range=COLOR_BREWER_BLUE_SCALE,
                        threshold=1,
                    ),
                ],
            ))

        else:
            ## Card matrix
            col_building_to_rent, col_avg_rent_price = st.columns(2)
            
            with col_building_to_rent:
                total_building_to_rent_count = chart_data['property_ID'].value_counts().sum().round(2)
                st.metric(label = 'Total house to rent', value= total_building_to_rent_count)
            
            with col_avg_rent_price:
                average_rent_price = chart_data['price_cleaned'].mean().round(2)
                st.metric(label = 'Average rent per week ($)', value= average_rent_price)

            ## End of card matrix

            st.write("Most Crowded Area on Map")

            midpoint = (np.average(chart_data["Lat"]), np.average(chart_data["Lng"]))

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=midpoint[0],
                    longitude=midpoint[1],
                    zoom=12.90,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        'HeatmapLayer',
                        data=chart_data,
                        opacity=0.9,
                        get_position='[Lng, Lat]',
                        radius=100,
                        elevation_scale=4,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                        get_weight="weight",
                        threshold=1,
                    ),
                    pdk.Layer(
                        'HeatmapLayer',
                        data=chart_data,
                        opacity=0.9,
                        get_position='[Lng, Lat]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=100,
                        pickable=True,
                        #color_range=COLOR_BREWER_BLUE_SCALE,
                        threshold=1,
                    ),
                ],
            ))

    with col_sold:

        enable_sold_ds = st.sidebar.checkbox("Enable filter for SOLD dataset")

        COLOR_BREWER_BLUE_SCALE = [
            [240, 249, 232],
            [204, 235, 197],
            [168, 221, 181],
            [123, 204, 196],
            [67, 162, 202],
            [8, 104, 172],
        ]

        chart_data = data_sold.filter(['property_ID', 'Lat', 'Lng', 'price', 'company'])

        if enable_sold_ds:

            ## Filtering
            options_for_company = chart_data['company'].unique().tolist()
            selected_options_company = st.sidebar.multiselect('Select Companies(You can modify default selection)',options_for_company, default=options_for_company[0:3])

            chart_data = chart_data.query('company == @selected_options_company')

            ## Card matrix
            col_total_sold, col_max_sold , col_max_price= st.columns(3)
            
            with col_total_sold:
                total_sold_count = chart_data['property_ID'].value_counts().sum().round(2)
                st.metric(label = 'Total sold house', value= total_sold_count)
            
            with col_max_sold:
                average_price = (chart_data['price'].mean()/1000000).round(3)
                st.metric(label = 'Average soled price in million ($)', value= average_price)
            
            with col_max_price:
                max_price = (chart_data['price'].max()/1000000).round(3)
                st.metric(label = 'Highest soled price in milion ($)', value= max_price)
                
            ## End of card matrix

            chart_data["radius"] = chart_data["price"].apply(lambda exits_count: math.sqrt(exits_count)/100)

            st.write("Houses by price on Map")

            midpoint = (np.average(data["Lat"]), np.average(data["Lon"]))

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=midpoint[0],
                    longitude=midpoint[1],
                    zoom=12.90,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=chart_data,
                        get_position='[Lng, Lat]',
                        pickable=True,
                        stroked=True,
                        filled=True,
                        radius_scale=6,
                        radius_min_pixels=1,
                        radius_max_pixels=100,
                        line_width_min_pixels=1,
                        get_radius="radius",
                        get_fill_color=[8, 104, 172],
                        get_line_color=[0, 0, 0],
                    ),
                ],
            ))

        else:
            
            ## Card matrix
            col_total_sold, col_max_sold , col_max_price= st.columns(3)
            
            with col_total_sold:
                total_sold_count = chart_data['property_ID'].value_counts().sum().round(2)
                st.metric(label = 'Total sold house', value= total_sold_count)
            
            with col_max_sold:
                average_price = (chart_data['price'].mean()/1000000).round(3)
                st.metric(label = 'Average soled price in million ($)', value= average_price)
            
            with col_max_price:
                max_price = (chart_data['price'].max()/1000000).round(3)
                st.metric(label = 'Highest soled price in milion ($)', value= max_price)
                
            ## End of card matrix

            chart_data["radius"] = chart_data["price"].apply(lambda exits_count: math.sqrt(exits_count)/100)

            st.write("Houses by price on Map")

            midpoint = (np.average(data["Lat"]), np.average(data["Lon"]))

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=midpoint[0],
                    longitude=midpoint[1],
                    zoom=12.90,
                    pitch=0,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=chart_data,
                        get_position='[Lng, Lat]',
                        pickable=True,
                        stroked=True,
                        filled=True,
                        radius_scale=6,
                        radius_min_pixels=1,
                        radius_max_pixels=100,
                        line_width_min_pixels=1,
                        get_radius="radius",
                        get_fill_color=[8, 104, 172],
                        get_line_color=[0, 0, 0],
                    ),
                ],
            ))

        