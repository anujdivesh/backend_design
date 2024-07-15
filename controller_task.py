
from model_task import task
from controller_dataset import initialize_datasetController
from controller_country import initialize_countryController
import requests
from datetime import datetime, timedelta
from utility_functions import Utility
from controller_server_path import PathManager

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
    
    #GENERATE NEXT DOWNLOAD FILENAME AND NEXT DOWNLOAD TIME
    def generate_next_download_filename(self,ds):
        substrings_to_remove = [ds.download_file_prefix, ds.download_file_suffix]
        new_string = Utility.remove_substrings(self.next_download_file, substrings_to_remove)
        convert_to_datetime = datetime.strptime(new_string, ds.download_file_infix)
        prepare_new_time = Utility.add_time(convert_to_datetime,ds.frequency_days, ds.frequency_hours,ds.frequency_minutes)
        new_file_name = ds.download_file_prefix + "" +prepare_new_time.strftime(ds.download_file_infix) + ds.download_file_suffix
        new_download_time = Utility.add_time(prepare_new_time,ds.check_days, ds.check_hours,ds.check_minutes)
        return new_file_name,new_download_time
    
    def download_http(self,ds):
        print('downloading with thredds...')
        try:
            #GET URL
            url = ds.data_download_url
            
            #REPLACE WITH FILE TO DOWNLOAD
            url = url.replace('{download_file_name}', self.next_download_file)

            download_complete = False
            is_error = False
            if Utility.url_exists(url):
                #DOWNLOAD THE FILE
                Utility.download_large_file(url,PathManager.get_url('tmp',self.next_download_file))

                #SUBSET AND GET VARIBLES AND MOVE FILE
                output_file = "%s/%s" % (ds.local_directory_path, self.next_download_file)
                if ds.download_to_local_dir:
                    Utility.subset_netcdf(ds, PathManager.get_url('tmp',self.next_download_file), output_file)

                #CLEANUP
                Utility.remove_file(PathManager.get_url('tmp',self.next_download_file))
                download_complete = True
            else:
                download_complete = False
        
        except Exception as e:
            print(e)
            is_error = True
        return download_complete, is_error

    

    def dataDownload(self):
        #GET DATASET
        dataset_url=f"https://dev-oceanportal.spc.int/v1/api/dataset/%s" % (self.dataset_id)
        ds = initialize_datasetController(dataset_url)

        #CHECK IF FILE EXISTS AND DOWNLOAD
        download_succeed, is_error = False, False
        
        if ds.download_method == "http":
            download_succeed, is_error = self.download_http(ds)
        elif ds.download_method == "corpernicus":
            print('downloading with corpernicus..')
        else:
            print('nothing to download.')
        """
        #COMPULSORY THINGS TO DO
        if download_succeed:
            new_file_name,new_download_time = self.generate_next_download_filename(ds)
            #UPDATE API NEW FILENAME AND NEWDOWNLOAD_TIME
            data = {
                "next_run_time":new_download_time.strftime("%Y-%m-%d %H:%M:%S"),
                "last_run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "next_download_file":new_file_name,
                "last_download_file":self.next_download_file,
                "success_count":self.success_count + 1
            }
            Utility.update_api(PathManager.get_url('ocean-api','task',str(self.id)), data)
            print('File download successful!')
        else:
            print('File does not exist, try again later')
            update_time = Utility.add_time(datetime.strptime(self.next_run_time,"%Y-%m-%dT%H:%M:%S.000Z"),ds.check_days, ds.check_hours,ds.check_minutes).strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "next_run_time":update_time,
                "last_run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "attempt_count":self.attempt_count + 1
            }
            Utility.update_api(PathManager.get_url('ocean-api','task',str(self.id)), data)

        if is_error:
            update_time = Utility.add_time(datetime.strptime(self.next_run_time,"%Y-%m-%dT%H:%M:%S.000Z"),ds.check_days, ds.check_hours,ds.check_minutes).strftime("%Y-%m-%d %H:%M:%S")
            data = {
                    "next_run_time":update_time,
                    "last_run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "fail_count":self.fail_count + 1
            }
            Utility.update_api(PathManager.get_url('ocean-api','task',str(self.id)), data)
            print('Download Failed')
        """
        #SCP FILE
        #SEND FILE TO RELEVANT SERVERS

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
