import streamlit as st
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from io import BytesIO

def main():
    st.title("City Map Generator")

    # Input fields
    city_name = st.text_input("Enter the name of the city:", "Rotterdam")
    road_color = st.color_picker("Choose the color of the roads:", "#0000FF")  # Default is blue
    background_color = st.color_picker("Choose the color of the background:", "#FFA500")  # Default is orange
    map_radius = st.slider("Choose the radius of the map (in meters):", 100, 5000, 1000)
    export_format = st.selectbox("Select export format:", ["PNG", "JPEG"])

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

                # Export the map
                if st.button("Export Map"):
                    st.markdown("### Exported Map")
                    export_buffer = BytesIO()
                    if export_format == "PNG":
                        fig.savefig(export_buffer, format="png")
                    elif export_format == "JPEG":
                        fig.savefig(export_buffer, format="jpeg")
                    export_buffer.seek(0)
                    st.image(export_buffer, caption=f"Exported map of {city_name}", use_column_width=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
# Donation button in the sidebar
with st.sidebar:
    st.image("SitrakasLogo.png")
    st.write("Hi ! 👋 ")
    st.write("I really liked the famous [PrettyMap App](https://prettymapp.streamlit.app/) ...however it was not exactly what I wanted.")
    st.write("I just wanted to make a really simple interface for user to have those simple design maps. Kind of Scandinavian vibes.")
    st.write("ie. simplicity, minimalism and functionality")
    st.write("So...here it is!")
    st.write(" Enjoy! Njut av!")
    st.markdown(
        """
   <a href='https://ko-fi.com/C0C6YRSIF' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
   """,
        unsafe_allow_html=True,
    )
if __name__ == "__main__":
    main()

