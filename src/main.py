import json 


file_path = "tests/data/"

def load_json_file(file_path, n):
    file_name = f"{file_path}example_{n}.json"
    with open(file_name, "r") as f:
        data = json.load(f)
    return data

data_dict = load_json_file(file_path,1)
output = []
assert isinstance(data_dict,dict) == True
for item in data_dict["context_sources"]:
    meta_data = item.get("metadata", {})
    output.append(
        {
            "context": item['context'],
            "source_doc": meta_data.get("document_id", None),
            "method": item["source"],
            "reason":meta_data.get("query", None)

     }
     )

print(output)