from huggingface_hub import InferenceClient
import base64
import requests
import io

client = InferenceClient("http://127.0.0.1:8080")

# read image from local file
image_path = r"C:\Users\chsjk\Documents\data\real_face\hard\4.png"
with open(image_path, "rb") as f:
    image = base64.b64encode(f.read()).decode("utf-8")

image = f"data:image/png;base64,{image}"
prompt = f"![]({image})Describe the character's appearance in detail\n\n"


for token in client.text_generation(prompt, max_new_tokens=50, stream=True):
    print(token)

# This is a picture of an anthropomorphic rabbit in a space suit.