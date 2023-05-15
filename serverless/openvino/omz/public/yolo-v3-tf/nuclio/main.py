import json
import base64
from PIL import Image
import io
from model_handler import ModelHandler
import yaml
import requests
from io import BytesIO

def init_context(context):
    context.logger.info("Init context...  0%")

    # Read labels
    with open("/opt/nuclio/function.yaml", 'rb') as function_file:
        functionconfig = yaml.safe_load(function_file)

    labels_spec = functionconfig['metadata']['annotations']['spec']
    labels = {item['id']: item['name'] for item in json.loads(labels_spec)}

    # Read the DL model
    model = ModelHandler(labels)
    context.user_data.model = model

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run yolo-v3-tf model")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"]))
    threshold = float(data.get("threshold", 0.5))
    image = Image.open(buf)
    url = "http://192.168.0.104:8083"
    r = requests.get(url, json=data)
    file_json = r.json()
    print(type(file_json))
    print(file_json)
   # for i in range(len(file_json)):
   #     for key, value in file_json[i].items():
    #        f.write(f'{key}, {value}\n')
    #f.close()
    answer = []
    for i in range(len(file_json)):
        answer.append({
                    "confidence": str(100),
                    "label": "traffic sign",
                    "points": [file_json[i]["x"], file_json[i]["y"], file_json[i]["x"] + file_json[i]["width"], file_json[i]["y"] + file_json[i]["height"]],
                    "type": "rectangle",
             })
    results = context.user_data.model.infer(image, threshold)
    print(results)

    return context.Response(body=json.dumps(results), headers={},
        content_type='application/json', status_code=200)
