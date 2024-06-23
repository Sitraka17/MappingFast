import streamlit as st
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import matplotlib.pyplot as plt
import io
import time

# Streamlit app
st.title("City Map Generator using Prettymapp")

# Input for the city name and radius
city_name = st.text_input("Enter the city name or address:", "")
radius = st.slider("Select the radius (meters):", min_value=100, max_value=5000, value=1000)

# Color selection for roads and background
road_color = st.color_picker("Choose the road color:", "#0000FF")  # Default is blue
background_color = st.color_picker("Choose the background color:", "#FFFFFF")  # Default is white

@st.cache_data(show_spinner=False)
def fetch_and_process_data(city_name, radius):
    # Get the area of interest (AOI) with the specified radius
    aoi = get_aoi(address=city_name, radius=radius, rectangular=False)
    
    # Get OSM geometries within the AOI
    df = get_osm_geometries(aoi=aoi)
    
    return aoi, df

if st.button("Make"):
    if city_name:
        start_time = time.time()
        try:
            # Fetch and process data
            aoi, df = fetch_and_process_data(city_name, radius)
            
            # Define custom style
            custom_style = {
                "background": {"color": background_color},
                "perimeter": {"color": "#000000"},
                "water": {"color": "#a0c8f0"},
                "park": {"color": "#c8e6a0"},
                "industrial": {"color": "#e6e6e6"},
                "highway": {"color": road_color},
                "street": {"color": road_color},
                "path": {"color": road_color},
            }
            
            # Plot the map using the custom style
            fig = Plot(
                df=df,
                aoi_bounds=aoi.bounds,
                draw_settings=custom_style
            ).plot_all()
            
            # Display the map
            st.pyplot(fig)
            
            # Save the map to an in-memory file
            buf = io.BytesIO()
            fig.savefig(buf, format='jpg')
            buf.seek(0)
            
            # Provide a download button for the map
            st.download_button(
                label="Download Map",
                data=buf,
                file_name=f"{city_name}_map.jpg",
                mime="image/jpeg"
            )
            
            end_time = time.time()
            st.write(f"Map generated in {end_time - start_time:.2f} seconds.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a city name or address.")
