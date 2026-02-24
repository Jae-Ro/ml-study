import json
import csv


def flatten_dict(
    map: dict,
    delimiter: str = ".", 
) -> dict:
    
    ret = {}
    
    prefix = ""
    stack = [(prefix, map)]

    while stack:
        
        prefix, data = stack.pop()

        if isinstance(data, dict):
            for k, v in reversed(data.items()):
                new_key = f"{prefix}{delimiter}{k}" if prefix else k
                stack.append((new_key, v))
        elif isinstance(data, list):
            for i in range(len(data)-1, -1, -1):
                item = data[i]
                # create an indexed key like "users.0", "users.1", etc.
                new_key = f"{prefix}{delimiter}{i}" if prefix else str(i)
                stack.append((new_key, item))
        else:
            # fallback for root-level primitives
            ret[prefix] = data
    
    return ret

def convert_json_csv(fpath: str) -> str:
    with open(fpath, "r") as f:
        data = json.load(f)

    headers = {}
    records = []
    for dict in data["data"]:
        flat_dict = flatten_dict(dict)
        records.append(flat_dict)
        for k in flat_dict:
            headers[k] = headers.get(k, 0)    
    
    headers = list(headers.keys())
    
    with open("test.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, restval="")
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    convert_json_csv("test.json")