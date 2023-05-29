import json
import requests

f = open("/opt/nuclio/common/ip.txt", "r")
ip = f.read()
f.close()
url = 'http://'+ip+':8083'

def init_context(context):
    context.logger.info("Init context...  0%")
    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run traffic sign detector")
    data = event.body
    print(url)
    r = requests.get(url, json=data)
    file_json = r.json()
    answer = []
    for i in range(len(file_json)):
        answer.append({
                    "confidence": str(100),
                    "label": "traffic sign",
                    "points": [file_json[i]["x"], file_json[i]["y"], file_json[i]["x"] + file_json[i]["width"], file_json[i]["y"] + file_json[i]["height"]],
                    "type": "rectangle",
             })
    return context.Response(body=json.dumps(answer), headers={},
        content_type='application/json', status_code=200)
