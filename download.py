import os
import requests
import zipfile
import shutil
import getpass

def download_extract_copy(input_folder, mod_name):
    username = getpass.getuser()
    directory_path = f"C:/Users/{username}/AppData/Roaming/AnyAspectRatio/perm/zla"

    # Zip URLs for regionUS.zip and region_common.zip only
    zip_urls = [
        ("https://github.com/fayaz12g/aar-files/raw/main/zla/regionUS.zip", "regionUS.zip"),
        ("https://github.com/fayaz12g/aar-files/raw/main/zla/region_common.zip", "region_common.zip")
    ]

    # Check if the directory exists, create if it doesn't
    os.makedirs(directory_path, exist_ok=True)

    # Define base folder paths for romfs
    romfs_folder = os.path.join(input_folder, mod_name, "romfs")
    region_us_folder = os.path.join(romfs_folder, "regionUS")
    region_common_folder = os.path.join(romfs_folder, "region_common")

    # Ensure destination folders for regionUS and region_common exist
    os.makedirs(region_us_folder, exist_ok=True)
    os.makedirs(region_common_folder, exist_ok=True)

    # Mapping zip files to their respective extract destinations
    extract_folders = {
        "regionUS.zip": region_us_folder,  # Extract to romfs/regionUS
        "region_common.zip": region_common_folder  # Extract to romfs/region_common
    }

    # Download or extract each zip file
    for zip_url, zip_filename in zip_urls:
        zip_file_source = os.path.join(directory_path, zip_filename)

        # Check if the zip file already exists locally
        if os.path.isfile(zip_file_source):
            print(f"{zip_filename} already exists. Skipping download.")
        else:
            print(f"{zip_filename} not found. Downloading, please wait...")
            # Download the ZIP file
            response = requests.get(zip_url)
            response.raise_for_status()
            with open(zip_file_source, "wb") as file:
                file.write(response.content)
            print(f"Finished downloading {zip_filename}.")

        # Extract the zip file to the respective destination
        extract_folder = extract_folders[zip_filename]
        
        # Remove the existing destination folder if it exists (optional, depending on your use case)
        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_file_source, "r") as zip_ref:
            zip_ref.extractall(extract_folder)
            print(f"Extracted {zip_filename} to {extract_folder}.")

    print("All zip files processed and extracted.")

