def filter_taks_by_name(list_of_tasks, task_name):
    """
    Filter tasks by name
    """
    return [task for task in list_of_tasks if task["name"].lower().startswith(task_name.lower())]
