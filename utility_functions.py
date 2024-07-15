import requests
from datetime import datetime, timedelta
import xarray as xr
from controller_country import initialize_countryController
import os

class Utility:
    @staticmethod
    def remove_substrings(original_string, substrings):
        for substring in substrings:
            original_string = original_string.replace(substring, "")
        return original_string
    
    @staticmethod
    def add_time(current_time, days=0, hours=0, minutes=0):
        return current_time + timedelta(days=days, hours=hours, minutes=minutes)
    
    @staticmethod
    def update_api(url, data, headers=None):
        try:
            response = requests.put(url, json=data, headers=headers)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()  # Return the response content as JSON
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except Exception as err:
            print(f"An error occurred: {err}")  # Handle other errors
        return None
    
    @staticmethod
    def url_exists(url):
        try:
            response = requests.head(url)
            # You can also use requests.get(url) if you need to access the content of the page
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur
            print(f"An error occurred: {e}")
            return False
        
    @staticmethod
    def download_large_file(url, destination):
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(destination, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            print("File downloaded successfully!")
        except requests.exceptions.RequestException as e:
            print("Error downloading the file:", e)

    @staticmethod
    def time_diff(time1, time2,enabled):
        difference = time1 - time2
        difference_in_minutes = difference.total_seconds() / 60
        print(difference_in_minutes)
        var = False
        if abs(difference_in_minutes) > 0 and abs(difference_in_minutes) < 20:
            var = True
        if not enabled:
            var = False
        
        return var
    
    @staticmethod
    def get_subset(ds):
        subset_region = False
        if ds.subset == True:
            url = f"https://dev-oceanportal.spc.int/v1/api/country/%s" % (ds.subset_region)
            subset_region = initialize_countryController(url)
        return subset_region
    
    @staticmethod
    def subset_netcdf(ds, old_path, new_path):
        dataset = xr.open_dataset(old_path)
        varib = dataset.variables
        subset = dataset[varib.split(",")]

        #CHECK IF SUBSET IS REQUIRED
        if ds.is_subset_auto:
            subset_region = Utility.get_subset(ds)
            subset = ds.sel(lat=slice(subset_region.north_bound_latitude, subset_region.south_bound_latitude),\
                            lon=slice(subset_region.west_bound_longitude, subset_region.east_bound_longitude))
        subset  = xr.decode_cf(subset )
        subset.to_netcdf(path=new_path ,mode='w',format='NETCDF4',  engine='netcdf4')
        return None
    
    @staticmethod
    def remove_file(url):
        if os.path.exists(url):
            os.remove(url)
        else:
            print("The file does not exist") 
