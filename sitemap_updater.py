import requests
import os
import sys

# --- Configuration ---
SITEMAP_URL = "https://docs.warpstream.com/warpstream/sitemap-pages.xml"
OUTPUT_FILENAME = "docs-zendesk-sitemap.xml"
TEMP_OUTPUT_PATH = os.path.join(os.getcwd(), OUTPUT_FILENAME)

def download_and_clean_sitemap():
    """
    Downloads the sitemap, removes lines containing <priority> and <lastmod>,
    and saves the cleaned content to the output file.
    """
    print(f"1. Downloading sitemap from: {SITEMAP_URL}")
    try:
        # 1. Download the content
        response = requests.get(SITEMAP_URL, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        raw_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the sitemap: {e}", file=sys.stderr)
        sys.exit(1)

    print("2. Cleaning content by removing <priority> and <lastmod> lines...")
    
    # 2. Process the content line by line
    cleaned_lines = []
    
    # Split the content into lines and strip leading/trailing whitespace
    for line in raw_content.splitlines():
        
        # Check if the line contains either tag (case-insensitive check added for robustness)
        lower_line = line.lower()
        if "<priority>" in lower_line or "<lastmod>" in lower_line:
            # Skip this line
            continue
        
        # Keep the line (strip extra whitespace from the line for cleanliness)
        cleaned_lines.append(line.strip())

    cleaned_content = '\n'.join(cleaned_lines)
    
    # 3. Write the cleaned content to the local file
    print(f"3. Writing cleaned content to {TEMP_OUTPUT_PATH}")
    try:
        # Use 'utf-8' encoding for XML files
        with open(TEMP_OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print(f"Success! {OUTPUT_FILENAME} has been updated locally.")
    except IOError as e:
        print(f"Error writing the file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    # Ensure the required 'requests' library is installed if running locally
    try:
        import requests
    except ImportError:
        print("The 'requests' library is required. Install with: pip install requests")
        sys.exit(1)

    download_and_clean_sitemap()
