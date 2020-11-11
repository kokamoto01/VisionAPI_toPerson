from base64 import b64encode
from sys import argv
import json
import requests

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'

if __name__ == "__main__":
  api_key, *image_filenames = argv[1:]

  img_requests = []
  for imgname in image_filenames:
    with open(imgname, 'rb') as f:
      ctxt = b64encode(f.read()).decode()
      img_requests.append({
          'image': {'content': ctxt},
          'features': [{
              'type': 'OBJECT_LOCALIZATION',
              'maxResults': 50
          }]
      })
  
  response = requests.post(ENDPOINT_URL,
    data=json.dumps({"requests": img_requests}).encode(),
    params={'key': api_key}, 
    headers={'Content-Type': 'application/json'})

  if response.status_code != 200 or response.json().get('error'):
      print(response.text)
  else:
    for idx, resp in enumerate(response.json()['responses']):
      print (json.dumps(resp, indent=2))