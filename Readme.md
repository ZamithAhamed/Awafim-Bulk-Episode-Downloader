# Bulk Episode Downloader for Awafim.tv

This project provides a Python script and a Streamlit interface to bulk download episodes of TV shows from **www.awafim.tv**. It allows users to enter a series URL, select seasons, and download episodes to a specified folder, with download progress displayed.

## Features

- **Bulk Download:** Download multiple episodes from a series based on season selection.
- **Progress Bar:** View download progress, speed, and size in real-time.
- **Customizable Download Folder:** Specify a local folder to store the downloaded episodes.
- **Streamlit Interface:** A simple, interactive web interface for easier use.

## Requirements

Ensure you have the following Python libraries installed:
- `requests` (for handling HTTP requests)
- `tqdm` (for displaying progress bars during downloads)
- `streamlit` (for creating the web interface)

### Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/ZamithAhamed/Awafim-Bulk-Episode-Downloader.git
    cd awafim-bulk-episode-downloader
    ```

2. Create a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use venv\Scripts\activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

### 1. **Run Streamlit App for Bulk Download Interface**

   To run the Streamlit interface, execute the following command:

   ```bash
   streamlit run app.py
   ```
This will open a web interface in your browser where you can:

- Enter the base URL of the show (e.g., https://www.awafim.tv/titles/212161485483413589-vikings-valhalla).
- Specify the download folder.
- Select the seasons you want to download.
- The app will display progress for each episode downloaded.

### 2. **Bulk Download via Command Line**


If you prefer to run the bulk download from the command line without the Streamlit interface, you can directly execute the download function:

   ```bash
   streamlit run app.py
   ```
    

Ensure you update the `base_url` and `download_folder` variables as required.