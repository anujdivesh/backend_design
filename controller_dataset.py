from model_dataset import dataset
import requests
from controller_country import initialize_countryController

class datasetController(dataset):
    def __init__(self, id, short_name, long_name, type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_to_local_dir,local_directory_path,scp,scp_server_path,frequency_type,frequency_minutes,frequency_hours,frequency_days,\
                        check_every_type,check_minutes,check_hours,check_days,variables,subset,subset_region,is_subset_auto):
        super().__init__(id, short_name, long_name, type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_to_local_dir,local_directory_path,scp,scp_server_path,frequency_type,frequency_minutes,frequency_hours,frequency_days,\
                        check_every_type,check_minutes,check_hours,check_days,variables,subset,subset_region,is_subset_auto)

    def dataDownload(self):
        #CHECK WHEATHER TO SUBSET THE DATASET
        subset_region = []
        if self.subset == True:
            url = f"https://dev-oceanportal.spc.int/v1/api/country/%s" % (self.subset_region)
            subset_region.append(initialize_countryController(url))

        
        if self.download_method == "ncss":
            print('downloading with thredds..')

        elif self.download_method == "http":
            print('downloading with http..')
        elif self.download_method == "ncss":
            print('downloading with corpernicus..')
        else:
            print('nothing to download.')
            

def initialize_datasetController(url):
    response = requests.get(url)
    if response.status_code == 200:
        item = response.json()
        dataset = datasetController(item['id'],item['short_name'], item['long_name'],item['type'], item['data_provider'],item['data_source_url'],\
                                item['data_download_url'],item['login_credentials_required'],item['username'],item['password'],\
                                item['API_key'],item['download_method'],item['download_file_prefix'],item['download_file_infix'],\
                                    item['download_file_suffix'],item['download_file_type'],item['download_to_local_dir'],\
                                        item['local_directory_path'],item['scp'],item['scp_server_path'],item['frequency_type'],item['frequency_minutes'],\
                                            item['frequency_hours'],item['frequency_days'],item['check_every_type'],item['check_minutes'],\
                                                item['check_hours'],item['check_days'],item['variables'],\
                                            item['subset'],item['subset_region'],item['is_subset_auto'])
        return dataset
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

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