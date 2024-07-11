
from model_task import task
from controller_dataset import initialize_datasetController
from controller_country import initialize_countryController
import requests
from datetime import datetime, timedelta
from utility_functions import Utility

class taskController(task):
    def __init__(self, id, task_name, class_id, dataset_id,status,priority,\
                 duration,task_start_time,next_run_time,last_run_time,next_download_file,last_download_file,enabled,health,fail_count,\
                    success_count,reset_count,attempt_count,predecessor_class,predecessor_class_id,successor_class,successor_class_id,created_by,launched_by,\
                        retain,retention_days):
        super().__init__( id, task_name, class_id, dataset_id,status,priority,\
                 duration,task_start_time,next_run_time,last_run_time,next_download_file,last_download_file,enabled,health,fail_count,\
                    success_count,reset_count,attempt_count,predecessor_class,predecessor_class_id,successor_class,successor_class_id,created_by,launched_by,\
                        retain,retention_days)
    
    #FUNCTION TO GET BOUNDING BOX SUBSETS
    def get_subset(self,ds):
        subset_region = False
        if ds.subset == True:
            url = f"https://dev-oceanportal.spc.int/v1/api/country/%s" % (ds.subset_region)
            subset_region = initialize_countryController(url)
        return subset_region
    

        

    def generate_next_download_filename(self,ds):
        today = datetime.today().strftime('%Y-%m-%d')
        #GET LAST DOWNLOADED FILE
        last_download_file_name = self.last_download_file
        substrings_to_remove = [ds.download_file_prefix, ds.download_file_suffix]
        new_string = self.remove_substrings(last_download_file_name, substrings_to_remove)
        convert_to_datetime = datetime.strptime(new_string, ds.download_file_infix)
        prepare_new_time = convert_to_datetime + timedelta(hours=int(ds.upload_frequency_hours))
        new_file_name = ds.download_file_prefix + "" +prepare_new_time.strftime(ds.download_file_infix) + ds.download_file_suffix
        print(new_file_name)
    
    def download_large_file(self,url, destination):
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(destination, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            print("File downloaded successfully!")
        except requests.exceptions.RequestException as e:
            print("Error downloading the file:", e)

    def url_exists(self,url):
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
    
    def download_ncss(self,ds):
        print('downloading with thredds...')

        #GET URL
        url = ds.data_download_url
        
        #REPLACE WITH FILE TO DOWNLOAD
        url = url.replace('{download_file_name}', self.next_download_file)

        #REPLACE VARIABLES
        url = url.replace('{variables}', ds.variables)

        #CHECK IF SUBSET
        if ds.subset:
            subset_region = self.get_subset(ds)
            url = url.replace('{north}', subset_region.north_bound_latitude)
            url = url.replace('{west}', subset_region.west_bound_longitude)
            url = url.replace('{east}', subset_region.east_bound_longitude)
            url = url.replace('{south}', subset_region.south_bound_latitude)
        
        #TRY TO DOWNLOAD
        output = ds.local_directory_path+"/"+self.next_download_file
        try:
            if self.url_exists(url):
                #DOWNLOAD FILE
                #self.download_large_file(url,output)

                #UPDATE NEXT FILE TO DOWNLOAD
                substrings_to_remove = [ds.download_file_prefix, ds.download_file_suffix]
                new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)
                convert_to_datetime = datetime.strptime(new_string, ds.download_file_infix)
                prepare_new_time = Utility.add_time(convert_to_datetime,ds.frequency_days, ds.frequency_hours,ds.frequency_minutes)
                new_file_name = ds.download_file_prefix + "" +prepare_new_time.strftime(ds.download_file_infix) + ds.download_file_suffix
                new_download_time = Utility.add_time(prepare_new_time,ds.check_days, ds.check_hours,ds.check_minutes)
                print(new_file_name, new_download_time)
                #UPDATE NEXT RUN TIME
            else:
                print('File does not exist')
                #UPDATE ATTEMPT COUNT
                #UPDATE NEXT RUN TIME
        except Exception as e:
            print('Download Failed')

    

    def dataDownload(self):
        #GET DATASET
        dataset_url=f"https://dev-oceanportal.spc.int/v1/api/dataset/%s" % (self.dataset_id)
        ds = initialize_datasetController(dataset_url)

        #CHECK IF FILE EXISTS AND DOWNLOAD
        download_succeed = False
        if ds.download_method == "ncss":
            self.download_ncss(ds)
        elif ds.download_method == "http":
            print('downloading with http..')
        elif ds.download_method == "corpernicus":
            print('downloading with corpernicus..')
        else:
            print('nothing to download.')

        #PUSH IT TO RELEVANT DIRECTORY

        #UPDATE NEXT_DOWNLOAD_FILENAME
        #UPDATE_NEXT_DOWNLOAD_TIME

def initialize_taskController(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        enqueue = []
        for item in data:
            queue = taskController(item['id'],item['task_name'], item['class_id'], item['dataset_id'],item['status'],\
                                 item['priority'],\
                                    item['duration'],item['task_start_time'],item['next_run_time'],\
                                        item['last_run_time'],item['next_download_file'],item['last_download_file'],\
                                        item['enabled'],item['health'],item['fail_count'],item['success_count'],item['reset_count'],\
                                            item['attempt_count'],item['predecessor_class'],item['predecessor_class_id'],item['successor_class'],\
                                            item['successor_class_id'],\
                                                item['created_by'],item['launched_by'],item['retain'],item['retention_days'])
            enqueue.append(queue)
        return enqueue
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
