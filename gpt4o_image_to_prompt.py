import os
import base64
import openai
from openai import OpenAI
import configparser

properties = configparser.ConfigParser()
properties.read('authentication.ini')
os.environ["OPENAI_API_KEY"] = properties['GPT_AUTH']['api_key']


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

client = OpenAI()

file_path = r'C:\Users\chsjk\Documents\data\미래서울도시관\processed'
suffixes = ('.jpg', '.png')
with open('guide.txt', 'r', encoding='utf-8') as f:
    guide = f.read()

for file in os.listdir(file_path):
    if file.endswith(suffixes):
        path = os.path.join(file_path, file)
        img = encode_image(path)
        messages = [
            {"role": "system",
             "content" : guide},
            {"role" : "user",
             "content" : [
                 {"type": "image_url",
                  "image_url" :{
                      "url": f'data:image/png;base64,{img}'
                  }}
             ]}
        ]
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=messages,
            temperature=0.0
        )

        description = response.choices[0].message.content

        with open(os.path.join(file_path, 'description.txt'), mode='a', encoding='utf-8') as f:
            f.write(f'{file} : {description}\n')
