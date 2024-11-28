import os
import requests
from ruamel.yaml import YAML

def get_latest_grid_driver():
    # URL of the JSON file containing driver information
    url = "https://raw.githubusercontent.com/ganeshkumarashok/azhpc-extensions/refs/heads/master/NvidiaGPU/Nvidia-GPU-Linux-Resources.json"
    response = requests.get(url)
    data = response.json()
    
    # Extract the latest GRID driver information
    grid_versions = data['Latest']['Category']
    grid_info = next((item for item in grid_versions if item["Name"] == "GRID"), None)
    
    if grid_info:
        latest_version_info = grid_info['Versions'][0]
        latest_version = latest_version_info['DriverVersion']
        latest_url = latest_version_info['Driver'][0]['DirLink']
        return latest_version, latest_url
    
    raise Exception("Could not find latest GRID driver version")

def update_driver_config():
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    
    with open("driver_config.yml", "r") as f:
        config = yaml.load(f)
    
    # Get latest version and URL
    latest_version, latest_url = get_latest_grid_driver()
    print(latest_version, latest_url)
    
    # Update the grid section while preserving order
    config['grid']['version'] = latest_version
    config['grid']['url'] = latest_url
    
    # Write back to file
    with open("driver_config.yml", "w") as f:
        yaml.dump(config, f)

if __name__ == "__main__":
    update_driver_config()