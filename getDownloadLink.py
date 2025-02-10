# getDownloadLink.py
import requests
import time

def get_final_download_link(initial_url, max_retries=3, retry_delay=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.awafim.tv/",
    }

    for attempt in range(max_retries):
        response = requests.get(initial_url, headers=headers, allow_redirects=False)
        if 'Location' not in response.headers:
            print(f"Attempt {attempt + 1}: Failed to get the redirected URL")
            return None

        redirected_url = response.headers['Location']
        print(f"Step 1 - Redirected URL (Attempt {attempt + 1}):", redirected_url)

        if redirected_url != initial_url:
            break
        else:
            print("Redirected URL is the same as the initial URL. Retrying...")
            time.sleep(retry_delay)

    if redirected_url == initial_url:
        print("Failed to get a different redirection URL after retries.")
        return None

    response = requests.post(redirected_url, headers=headers, allow_redirects=False)
    if 'Location' not in response.headers:
        print("Failed to get the final file download URL")
        return None

    final_download_url = response.headers['Location']
    print("Step 2 - Final Download Link:", final_download_url)

    return final_download_url
