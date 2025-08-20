import json

from utils.Requester import Requester

req = Requester("swshadows")

data = req.get_data()

with open("output.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(data, indent=4, ensure_ascii=False))
