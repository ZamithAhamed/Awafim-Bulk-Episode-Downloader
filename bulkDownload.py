# bulkDownload.py
import requests
import os
from getDownloadLink import get_final_download_link

def check_season_availability(base_url, max_seasons=100):
    available_seasons = []
    for season in range(1, max_seasons + 1):
        season_url = f"{base_url}/S{season:02d}"
        response = requests.get(season_url)
        if response.status_code == 404:
            print(f"Season {season} is not available.")
            break
        else:
            print(f"Season {season} is available.")
            available_seasons.append(season)
    return available_seasons

def download_episodes_for_season(base_url, season, download_folder):
    season_url = f"{base_url}/S{season:02d}"
    episode_number = 1
    while True:
        episode_url = f"{season_url}/E{episode_number:02d}/download-0-0"
        print(f"Checking availability of Episode {episode_number}...")
        response = requests.get(episode_url)
        if response.status_code == 404:
            print(f"Episode {episode_number} is not available.")
            break
        else:
            print(f"Episode {episode_number} is available.")
            final_download_url = get_final_download_link(episode_url)
            file_extension = os.path.splitext(final_download_url)[1]
            if final_download_url:
                os.makedirs(download_folder, exist_ok=True)
                # Download the episode
                episode_file = os.path.join(download_folder, f"Episode_{episode_number}.{file_extension}")
                with requests.get(final_download_url, stream=True) as r:
                    with open(episode_file, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"Downloaded Episode {episode_number}")
            episode_number += 1

def main():
    base_url = "https://www.awafim.tv/titles/212161485483413589-vikings-valhalla"
    
    # Get the download path from the user
    download_path = input("Please enter the path where you want to download the episodes: ")
    download_path = os.path.abspath(download_path)
    
    print("Checking for available seasons...")
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
        
        # Folder to store the episodes
        season_folder = os.path.join(download_path, f"Season_{season}")
        download_episodes_for_season(base_url, season, season_folder)

if __name__ == "__main__":
    main()
