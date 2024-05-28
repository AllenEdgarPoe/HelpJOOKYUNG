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

mask_path = r'C:\Users\chsjk\Downloads\photox\mask'
result_path = r'C:\Users\chsjk\Downloads\photox\result'

import os
import datetime
import openai
import configparser

properties = configparser.ConfigParser()
properties.read('authentication.ini')
openai.api_key = properties['GPT_AUTH']['api_key']


# prompt_history = ["a portrait of a woman in fantasy forest, tilt-shift photo, selective focus, blurred background, highly detailed, vibrant, perspective control",
#                   "a realistic photo of a woman in busy street, vibrant city lights, tilt-shift photo, selective focus, blurred background, highly detailed, vibrant, perspective control",
#                   "a woman in dark gloomy garden, red lights, focus, tilt-shift photo, selective focus, blurred background, highly detailed, vibrant, perspective control",
#                   "a girl, bedroom, subtle candle lights, out of focus, tilt-shift photo, selective focus, blurred background, highly detailed, vibrant, perspective control",
#                   "a woman in a tranquil park, soft sunset hues, gentle breeze, tilt-shift photo, selective focus, blurred background, highly detailed, vibrant, perspective control"
#                   ]

prompt_history = [
    "a realistic photo of busy street, vibrant city lights, selective focus",
    "dark gloomy garden, red lights, focus",
    "bedroom, subtle candle lights, out of focus"
]

def send_gpt_message(input_text_file):
    try:
        with open(input_text_file, mode='r', encoding='utf-8') as f:
            input_text = f.read()
            input_text += '\n'.join(prompt_history)
        message = []
        message.append(
            {"role" : "user",
             "content": input_text}
        )
        key = openai.ChatCompletion.create(
            model="gpt-4",
            messages = message
        )
        response = key['choices'][0]['message']['content']

        prompt_history.append(response)
        if len(prompt_history)>10:
            prompt_history.pop(0)
        return response
    except Exception as e:
        print(e)
        return ''

def readImage(path):
    img = cv2.imread(path)
    retval, buffer = cv2.imencode('.png', img)
    b64img = b64encode(buffer).decode("utf-8")
    return b64img

def queue_prompt(prompt):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:
        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
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


def check_file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        raise FileNotFoundError(f'The file {file_path} does not exists. ')

def randomize_seed(prompt, node_id):
    prompt[node_id]['inputs']['seed'] = random.randint(1,4294967294)
    return prompt


def make_prompt(input_message):
    response = send_gpt_message(input_message)
    return response

def transform_image(workflow_path, input_path, save_path):
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            prompt = json.load(f)

        # put input path
        prompt['295']['inputs']['image'] = input_path

        # make prompt
        prompt['290']['inputs']['text_positive'] = make_prompt('input.txt')
        prompt = randomize_seed(prompt, '290')

        # fix the prefix of the save_path
        filename = input_path.split('\\')[-1].split('.')[0]
        prompt['284']['inputs']['filename_prefix'] = filename

        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
        file_name = get_images(ws, prompt)

        return

    except Exception as e:
        print(e)


def backendcache_api(filename, workflow_path, mode):
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            prompt = json.load(f)

        # put input path
        prompt['105']['inputs']['image'] = filename

        model_key = mode
        pos_key = mode + '_pos'
        neg_key = mode + '_neg'
        prompt['101']['inputs']['key'] = model_key
        prompt['102']['inputs']['key'] = pos_key
        prompt['103']['inputs']['key'] = neg_key

        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
        file_name = get_images(ws, prompt)
        return

    except Exception as e:
        print(e)



if __name__ == '__main__':
    path = r'C:\Users\chsjk\Documents\data\real_face\xorbis'
    img = os.path.join(path, '5.jpg')
    for mode in ['harrypotteranime', 'clay', 'lineart']:
        backendcache_api(img,r'C:\Users\chsjk\PycharmProjects\photox\workflow_new\1인portrait\backend_cache_api.json', mode)


