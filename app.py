import streamlit as st
import os
from bulk_download import check_season_availability, download_episodes_for_season

def main():
    st.title("Bulk Episode Downloader")
    
    # Get the base URL from the user
    base_url = st.text_input("Enter the base URL of the show (e.g., https://www.awafim.tv/titles/212161485483413589-vikings-valhalla):")

    if not base_url:
        st.warning("Please enter the base URL to proceed.")
        return

    # Extract the title name
    title_name = base_url.split("/titles/")[1].split("-", 1)[1].replace("-", " ").title()
    st.write(f"Extracted Series name: {title_name}")
    
    # Get the download path from the user (manual text input)
    download_path = st.text_input("Enter the download folder path (e.g., /path/to/download/folder):")

    if not download_path:
        st.warning("Please provide a download path.")
        return
    
    # Check for available seasons
    st.write("Checking for available seasons...")
    available_seasons = check_season_availability(base_url)
    
    if available_seasons:
        st.write(f"Available seasons: {available_seasons}")
    else:
        st.error("No seasons are available.")
        return
    
    # Ask user which seasons to download
    selected_seasons = st.multiselect("Select seasons to download:", available_seasons)
    
    if selected_seasons:
        for season in selected_seasons:
            season_folder = os.path.join(download_path, f"{title_name} S{season:02d}")
            st.write(f"Downloading Season {season} to {season_folder}")
            
            with st.spinner(f"Downloading Season {season}..."):
                download_episodes_for_season(base_url, season, season_folder)
        
        st.success("Download completed!")
    else:
        st.warning("Please select at least one season to download.")

if __name__ == "__main__":
    main()
