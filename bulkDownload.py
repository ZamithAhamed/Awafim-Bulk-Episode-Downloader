# bulkDownload.py
import requests
import os
from getDownloadLink import get_final_download_link
import time
from tqdm import tqdm  # Import tqdm for progress bar
from urllib.parse import unquote

def check_season_availability(base_url, max_seasons=100):
    available_seasons = []
    for season in range(1, max_seasons + 1):
        season_url = f"{base_url}/S{season:02d}"
        response = requests.get(season_url)
        if response.status_code == 404:
            # print(f"Season {season} is not available.")
            break
        else:
            # print(f"Season {season} is available.")
            available_seasons.append(season)
    return available_seasons

def download_episodes_for_season(base_url, season, download_folder):
    season_url = f"{base_url}/S{season:02d}"
    episode_number = 1
    while True:
        episode_url = f"{season_url}/E{episode_number:02d}/download-0-0"
        # print(f"Checking availability of Episode {episode_number}...")
        response = requests.get(episode_url)
        if response.status_code == 404:
            break
        else:
            # print(f"Episode {episode_number} is available.")
            final_download_url = get_final_download_link(episode_url)
            if final_download_url:
                os.makedirs(download_folder, exist_ok=True)
                
                # Extract filename from the final download URL
                filename = final_download_url.split("/")[-1]  # Get the part after the last "/"
                filename = unquote(filename)  # Decode URL encoding
                filename = filename.replace("_", " ")  # Replace underscores with spaces
                
                # Download the episode
                episode_file = os.path.join(download_folder, filename)
                with requests.get(final_download_url, stream=True) as r:
                    total_size = int(r.headers.get('content-length', 0))
                    # Using tqdm to show the progress bar with speed
                    with open(episode_file, 'wb') as f, tqdm(
                        desc=f"Downloading Episode {episode_number}",
                        total=total_size, 
                        unit='B', 
                        unit_scale=True,
                        ncols=100,  # Set the width of the progress bar (optional)
                        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]"
                    ) as bar:
                        start_time = time.time()
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                            bar.update(len(chunk))
                            elapsed_time = time.time() - start_time
                            # Calculate the download speed
                            download_speed = len(chunk) / elapsed_time if elapsed_time > 0 else 0
                            # Update tqdm with the download speed
                            bar.set_postfix(speed=f"{download_speed / 1024:.2f} KB/s")
                            start_time = time.time()
                # print(f"Downloaded Episode {episode_number}")
            episode_number += 1

def main():
    base_url = "https://www.awafim.tv/titles/212161485483413589-vikings-valhalla"
    
    # Get the download path from the user
    download_path = input("Please enter the path where you want to download the episodes: ")
    download_path = os.path.abspath(download_path)
    
    title_name = base_url.split("/titles/")[1].split("-", 1)[1].replace("-", " ").title()

    print(f"Checking for available seasons of {title_name}...")
    available_seasons = check_season_availability(base_url)

    if not available_seasons:
        print("No seasons are available.")
        return
    
    print("\nAvailable seasons:", available_seasons)
    
    # Ask user for which seasons to download
    selected_seasons = input("Enter season numbers to download (comma separated): ").split(',')
    selected_seasons = [int(season.strip()) for season in selected_seasons if season.strip().isdigit()]
    
    for season in selected_seasons:
        if season not in available_seasons:
            print(f"Season {season} is not available, skipping...")
            continue
        
        # Folder to store the episodes (e.g., "Vikings Valhalla S01")
        season_folder = os.path.join(download_path, f"{title_name} S{season:02d}")
        download_episodes_for_season(base_url, season, season_folder)

if __name__ == "__main__":
    main()
