from typing import Any

def find_project_region_registry_from_parent(parent):
    #projects/ingressdevelopmentenv/locations/us-central1/registries/gargi_python
    if not parent:
        return None

    list = parent.split("/")
    project_region_registry_dict = {}    
    if "projects" in list and len(list) >= 2:
        project_region_registry_dict['project'] = list[1]
    if "locations" in list and len(list) >= 4:
        project_region_registry_dict['location'] = list[3]
    if "registries" in list and len(list) >= 6:
        project_region_registry_dict['registry'] = list[5]

    return project_region_registry_dict

def get_value(json_data, key):
    if key in json_data:
        return json_data[key]
    return None

class SingletonMetaClass(type):

    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwds)
            cls._instances[cls] = instance
        return cls._instances[cls]


