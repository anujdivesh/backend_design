from controller_task import initialize_taskController

if __name__ == "__main__":
    url = f"https://dev-oceanportal.spc.int/v1/api/tasks"
    tasks = initialize_taskController(url)
    
    for task in tasks:
        if task.class_id == "download":
            task.dataDownload()
        else:
            print('nothing to do.')