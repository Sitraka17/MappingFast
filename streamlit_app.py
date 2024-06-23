import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def main():
    st.title("City Map Generator")

    # Input fields
    city_name = st.text_input("Enter the name of the city:", "Bordeaux")
    road_color = st.color_picker("Choose the color of the roads:", "#0000FF")  # Default is blue
    background_color = st.color_picker("Choose the color of the background:", "#FFA500")  # Default is orange
    map_radius = st.slider("Choose the radius of the map (in meters):", 100, 5000, 1000)

    if st.button("Generate Map"):
        with st.spinner("Generating map..."):
            try:
                # Geocode the city to get the central point
                geocode_result = ox.geocode(city_name)
                center_point = (geocode_result[0], geocode_result[1])

                # Fetch graph for the specified city
                G = ox.graph_from_point(center_point, dist=map_radius, retain_all=True, simplify=True, network_type='walk')
                gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)

                # Plot the map
                fig, ax = plt.subplots(figsize=(10, 10))
                gdf_edges.plot(ax=ax, color=road_color, linewidth=2)
                ax.set_facecolor(background_color)
                ax.set_title(f"Map of {city_name}", fontsize=15)
                ax.set_xticks([])
                ax.set_yticks([])
                for spine in ax.spines.values():
                    spine.set_visible(False)
                
                # Show the map in Streamlit
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
