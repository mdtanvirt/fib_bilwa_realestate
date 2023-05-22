import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk 

st.set_page_config(layout="wide")

# Hide streamlit default menu and footer from the template
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden}
    footer {visibility: hidden}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title('Project realestate')

data = pd.read_csv('WestEnd_merged_full new.csv')
st.dataframe(data)

###########


chart_data = data.filter(['Lat', 'Lon', 'Distance to Flood', 'Adjacent Bus Station', 'Street_Name'])
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
