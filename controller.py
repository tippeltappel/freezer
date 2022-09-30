# controller.py
import json

# filepathes
units_file = "data/units.json"

# test data
units = [{"name":"ml","rank":88},{"name":"gr","rank":88}]

def units_obj_save(file_name):
    with open (file_name,"w") as f:
    json.dump(obj,f,indent=4)

def units_obj_load(obj,file_name)
    with open (file_name,"r") as f:
        return json.load(f)