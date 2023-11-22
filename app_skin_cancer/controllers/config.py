import json

def read_config():
    with open("controllers/config.json", "r") as file:
        data = json.load(file)
    return data

settings = read_config()
id2label = {id:label for id, label in enumerate(settings["class_names"])}
label2id = {label:id for id,label in id2label.items()}

#print(settings["list_models"]["vit-L/32"])
#print(settings["class_names"])
#print(id2label)
#print(label2id)
