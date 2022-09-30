import py_compile


# test.py_compile
import json

data = {"user":
    {"name":"Thorsten",
    "age":62}
    }

print(data)    

with open ("test.json","w") as file_1:
    json.dump(data,file_1,indent=4)

#json_str= json.dumps(data,indent=2)
json_str= json.dumps(data,separators=(", ",": "))
#print(json_str)

with open ("test.json","r") as file_2:
    data=json.load(file_2)

print(data)      