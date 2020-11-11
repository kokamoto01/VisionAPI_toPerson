# 絶対使うライブラリ
from base64 import b64encode
from sys import argv
from os import makedirs
from datetime import datetime
import json
import requests

# 後で使うかも
  # imgname = image_filenames[idx]
  # jpath = join(RESULTS_DIR, basename(imgname) + '.json')
  # for idx, result in enumerate(response.json()['responses']): 

ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'

def make_image_data(image_filenames): # img_requests(画像データ+VisionAPIの処理を入れる配列)を作る関数
  img_requests = [] # リクエスト用の配列
  for imgname in image_filenames:
    with open(imgname, 'rb') as f:
      ctxt = b64encode(f.read()).decode() # 画像をBASE64でエンコード
      img_requests.append({
              'image': {'content': ctxt},
              'features': [{
                  'type': 'OBJECT_LOCALIZATION',
                  'maxResults': 50
              }]
      })
  return img_requests

def conversion_image_data(image_filenames): # リクエスト内容をjson形式に変換する関数
  imgdict = make_image_data(image_filenames)
  return json.dumps({"requests": imgdict })

def request_api(api_key, image_filenames): # VisionAPIを呼び出す関数
  response = requests.post(ENDPOINT_URL,
                          data=conversion_image_data(image_filenames),
                          params={'key': api_key},
                          headers={'Content-Type': 'application/json'})
  return response

# def inlcuded_person(result): # VisionAPIから得られた結果から人数を抜き取る

#   return numbers

def output_json(result): # VisionAPIから得られた結果をファイルとして出力する
  makedirs('jsons', exist_ok=True)
  now = datetime.now()
  file_name = './jsons/' + 'log_' + now.strftime('%Y%m%d_%H%M') + '.json' # ファイル命名規則(./jsons/log_yyyydddd_hhmm.json)
  with open(file_name, 'w') as f:
    json.dump(result, f, indent=2)

if __name__ == '__main__':
  api_key, *image_filenames = argv[1:]
  if not api_key or not image_filenames: # 正常な引数を設定していない時
    print("""\
    適切なAPIキーと画像ファイルを指定してください。
    $ python test01.py APIキー 画像ファイル""")
  else: # 引数が正常に設定できている
    response = request_api(api_key, image_filenames)
    if response.status_code != 200 or response.json().get('error'): # エラーメッセージ
      print(response.text)
    else: # 正常なら画面出力
      result = response.json()['responses'][0]['localizedObjectAnnotations'] # 大量の入れ子構造になっているので、要対応
      print(json.dumps(result, indent=2))
      output_json(result)