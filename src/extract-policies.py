# Script by Max: https://gist.github.com/mhils/c2896cf4d180b7ea3439e1a3e37f7e54

# Usage: mitmdump -s extract-policies.py -n -q -r traffic.mitm
import json

entries = {}

def response(flow):
    try:
        data = json.loads(flow.response.text)
    except ValueError:
        return
    results = data.get("results",{}).values()
    entries.update({
        x["id"]: {
            "name": x.get("name"),
            "url": x.get("url"),
            "policy": x.get("softwareInfo",{}).get("privacyPolicyUrl")
        }
        for x in results
        if x.get("softwareInfo",{}).get("privacyPolicyUrl")
    })

def done():
    with open("policies.json", "w") as f:
        json.dump(entries, f, indent=2)
