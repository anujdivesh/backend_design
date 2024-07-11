
class dataset:
    def __init__(self, id, short_name, long_name, type,data_provider,data_source_url,data_download_url,login_credentials_required,username,\
                 password,API_key,download_method,download_file_prefix,download_file_infix,download_file_suffix,download_file_type,\
                    download_to_local_dir,local_directory_path,scp,scp_server_path,frequency_type,frequency_minutes,frequency_hours,frequency_days,\
                        check_every_type,check_minutes,check_hours,check_days,variables,subset,subset_region,is_subset_auto):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.type = type
        self.data_provider = data_provider
        self.data_source_url = data_source_url
        self.data_download_url = data_download_url
        self.login_credentials_required = login_credentials_required
        self.username = username
        self.password = password
        self.API_key = API_key
        self.download_method = download_method
        self.download_file_prefix = download_file_prefix
        self.download_file_infix = download_file_infix
        self.download_file_suffix = download_file_suffix
        self.download_file_type = download_file_type
        self.download_to_local_dir = download_to_local_dir
        self.local_directory_path = local_directory_path
        self.scp = scp
        self.scp_server_path = scp_server_path
        self.frequency_type = frequency_type
        self.frequency_minutes = frequency_minutes
        self.frequency_hours = frequency_hours
        self.frequency_days = frequency_days
        self.check_every_type = check_every_type
        self.check_minutes = check_minutes
        self.check_hours = check_hours
        self.check_days = check_days
        self.variables = variables
        self.subset = subset
        self.subset_region = subset_region
        self.is_subset_auto = is_subset_auto