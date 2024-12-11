import os
import shutil
import tempfile
import zipfile
import requests

STATIC_PACKAGE_URL = "https://github.com/zdhxiong/mdui/releases/download/v1.0.2/mdui-v1.0.2.zip"
TARGET_DIR = os.path.join("app", "static")

def install_mdui(download_url=STATIC_PACKAGE_URL, target_dir=TARGET_DIR):
    
    with tempfile.TemporaryDirectory() as temp_dir:

        print(f"Downloading {download_url}...")
        response = requests.get(download_url, stream=True)
        if response.status_code != 200:
            raise Exception(f"Failed to download file: {response.status_code}")

        zip_path = os.path.join(temp_dir, "mdui.zip")
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        extracted_dir = os.path.join(temp_dir, "mdui")
        print(f"Extracting to {target_dir}...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extracted_dir)

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.move(extracted_dir, target_dir)
        with open(os.path.join(target_dir, ".gitkeep"), "w") as f:
            pass

    print(f"Successfully extracted to {target_dir}")

if __name__ == "__main__":
    install_mdui()
