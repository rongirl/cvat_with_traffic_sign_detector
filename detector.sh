
python3 get_ip.py

nuctl deploy --project-name cvat \
  --path serverless/openvino/omz/public/traffic_sign_detection/nuclio \
  --volume `pwd`/serverless/common:/opt/nuclio/common \
  --platform local

cd detector_dockerfile 
docker build -t server_detector . 
docker run --rm -i --name detector_traffic_signs -p 8083:8083 server_detector
