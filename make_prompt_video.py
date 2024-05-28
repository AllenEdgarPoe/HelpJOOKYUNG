import random
import os
import cv2
import numpy as np
from base64 import b64encode
import websocket #NOTE: websocket-client (https://github.com/websocket-client/websocket-client)
import uuid
import json
import urllib.request
import urllib.parse
import configparser
import logging
import sys
from PIL import Image
sys.path.append('.')
config_file = os.getcwd()

setting = configparser.ConfigParser()
# setting.read('config.ini')
# server_address = setting['COMFYUI']['address']
server_address = '127.0.0.1:8189'
client_id = str(uuid.uuid4())

path = r'C:\Users\chsjk\Documents\data\AI서울 참고이미지\processed'
with open(os.path.join(path, 'description.json'), 'r', encoding='utf-8') as f:
    description = json.load(f)
key_list = list(description.keys())
for key in key_list:
    if not os.path.exists(os.path.join(path, key)):
        key_list.remove(key)


def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data
    return

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())

def make_prompt_video(landmarks):
    prompt = f'"0":"{description[landmarks[0]]}",\n' \
             f'"25":"{description[landmarks[1]]}",\n' \
             f'"50":"{description[landmarks[2]]}",\n' \
             f'"75":"{description[landmarks[3]]}",\n' \
             f'"100":"{description[landmarks[0]]}",\n'
    return prompt

def randomize_seed(prompt, node_id):
    prompt[node_id]['inputs']['seed'] = random.randint(1,4294967294)
    return prompt

def transform_image(workflow_path):
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            prompt = json.load(f)

        landmarks = random.sample(key_list, 4)
        prompt_txt = make_prompt_video(landmarks)
        img1 = os.path.join(path, landmarks[0])
        img2 = os.path.join(path, landmarks[1])
        img3 = os.path.join(path, landmarks[2])
        img4 = os.path.join(path, landmarks[3])

        # put input path
        prompt['133']['inputs']['image'] = img1
        prompt['134']['inputs']['image'] = img2
        prompt['135']['inputs']['image'] = img3
        prompt['136']['inputs']['image'] = img4
        prompt['140']['inputs']['image'] = img1

        # make prompt
        prompt['119']['inputs']['text'] = prompt_txt

        randomize_seed(prompt, '69')

        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
        file_name = get_images(ws, prompt)
        return

    except Exception as e:
        print(e)


if __name__ == '__main__':
    workflow_path = r'C:\Users\chsjk\PycharmProjects\ComfyUI_windows_portable\ComfyUI\work__flow\symphony\10sec_video_api.json'
    for _ in range(10):
        transform_image(workflow_path)

