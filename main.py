import json

if __name__ == "__main__":
    serialized_json = '{"type":"item","content":"Under","metadata":{"nodeId":"28fc53d1-22af-4501-ba26-1812149adefb","nodeName":"AI Agent","itemIndex":0,"runIndex":0,"timestamp":1755077011763}}'
    print(f"Length: {len(serialized_json)}")
    obj = json.loads(serialized_json)
    print(obj)
    print(obj['type'])