import streamlit as st
import osmnx as ox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Streamlit app
st.title("City Map Generator using OSMnx")

# Input for the city name
city_name = st.text_input("Enter the city name:", "")

if st.button("Make"):
    if city_name:
        try:
            place = [city_name]
            gdf_nodes = gdf_edges = None

            for place in place:
                G = ox.graph_from_place(place, retain_all=True, simplify=True, network_type='walk')
                n_, e_ = ox.graph_to_gdfs(G)
                n_["place"] = place
                e_["place"] = place
                if gdf_nodes is None:
                    gdf_nodes = n_
                    gdf_edges = e_
                else:
                    gdf_nodes = pd.concat([gdf_nodes, n_])
                    gdf_edges = pd.concat([gdf_edges, e_])

            # Plot it
            colors = {city_name: 'blue'}
            fig, ax = plt.subplots(figsize=(10, 10))
            gdf_edges.plot(ax=ax, column="place", cmap=ListedColormap([colors[k] for k in sorted(colors.keys())]), alpha=1, linewidth=2, edgecolor='blue', facecolor='orange')

            plt.title(city_name)
            plt.xticks([])
            plt.yticks([])
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)

            st.pyplot(fig)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a city name.")

