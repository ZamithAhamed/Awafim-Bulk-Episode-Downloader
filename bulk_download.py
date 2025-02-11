import os
import requests
from urllib.parse import unquote
from tqdm import tqdm
import time
from getDownloadLink import get_final_download_link
import streamlit as st


def check_season_availability(base_url):
    season_number = 1
    available_seasons = []
    
    # Checking availability of seasons
    while True:
        season_url = f"{base_url}/S{season_number:02d}"
        response = requests.get(season_url)
        
        if response.status_code == 404:
            break
        else:
            available_seasons.append(season_number)
        
        season_number += 1
    
    return available_seasons

def get_episodes_for_season(base_url, season):
    season_url = f"{base_url}/S{season:02d}"
    episode_number = 1
    episodes = []

    while True:
        episode_url = f"{season_url}/E{episode_number:02d}/download-0-0"
        
        # Check if episode is available (status code 404 means not found)
        response = requests.get(episode_url)
        
        if response.status_code == 404:
            break
        
        final_download_url = get_final_download_link(episode_url)
        if final_download_url:
            filename = final_download_url.split("/")[-1]
            filename = unquote(filename)
            filename = filename.replace("_", " ")
            episodes.append((episode_url, filename))
        
        episode_number += 1
    
    return episodes

def download_episode(episode_url, download_folder, episode_name, progress_bar):
    final_download_url = get_final_download_link(episode_url)
    if final_download_url:
        response = requests.head(final_download_url)
        file_size = int(response.headers.get('Content-Length', 0))
        
        episode_path = os.path.join(download_folder, episode_name)

        # This will be used to clear the previous display output and replace with new data
        status_placeholder = st.empty()

        with requests.get(final_download_url, stream=True) as r:
            r.raise_for_status()
            total_downloaded = 0
            start_time = time.time()

            with open(episode_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    total_downloaded += len(chunk)

                    # Calculate download speed
                    elapsed_time = time.time() - start_time
                    download_speed = (total_downloaded / elapsed_time) / 1024  # KB/s

                    # Update progress bar with percentage
                    progress_bar.progress(total_downloaded / file_size)

                    # Update download speed and size information in the placeholder
                    status_placeholder.text(
                        f"Speed: {download_speed:.2f} KB/s | "
                        f"Size: {total_downloaded / (1024 * 1024):.2f} MB"
                    )


def download_episodes_for_season(base_url, season, download_folder):

    season_url = f"{base_url}/S{season:02d}"
    episode_number = 1

    while True:
        episode_url = f"{season_url}/E{episode_number:02d}/download-0-0"
        
        # Check if episode is available (status code 404 means not found)
        response = requests.get(episode_url)
        
        if response.status_code == 404:
            break
        
        final_download_url = get_final_download_link(episode_url)
        if final_download_url:
            filename = final_download_url.split("/")[-1]
            filename = unquote(filename)
            filename = filename.replace("_", " ")
            with st.spinner(f"Downloading {filename}..."):
                progress_bar = st.progress(0)
                download_episode(episode_url, download_folder, filename, progress_bar)
        
        episode_number += 1
    
