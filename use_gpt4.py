import base64
import os
import datetime
from openai import OpenAI
import configparser
import time

properties = configparser.ConfigParser()
properties.read('authentication.ini')
os.environ["OPENAI_API_KEY"] = properties['GPT_AUTH']['api_key']
now = datetime.datetime.now().strftime('%Y-%m-%d')
os.makedirs(os.path.join('gpt_history', now), exist_ok=True)

client = OpenAI()

def send_gpt_message2(input_text, history):
    try:
        message = [
            {"role": "system",
            "content": "당신은 패션 분석 AI 입니다. 주어진 description 을 토대로, 상대의 외모 와 패션 스타일에 대해 분석하세요."},
            {"role" : "user",
            "content" : """
            he individual in the image is wearing a black leather jacket with a high collar and a structured design, featuring visible stitching and a zipper that runs down the front. The jacket appears to be well-fitted, accentuating the silhouette of the wearer. Underneath the jacket, there is a glimpse of a black shirt or top with a buttoned front, which complements the overall dark and edgy aesthetic.

The person's hair is styled in a sleek, straight fashion, falling just above the collar of the jacket. The hair color is a deep, dark shade, which contrasts with the lighter background. The individual's makeup is notable, with a bold red lipstick that stands out against the dark tones of the outfit. The eyes are accentuated with dark eyeliner and a subtle smoky eye makeup, which adds to the dramatic and intense look.

The overall fashion style depicted in the image is a mix of edgy and sophisticated, with a strong emphasis on dark colors and structured, tailored pieces. The combination of the leather jacket, the buttoned shirt, and the bold makeup creates a striking and memorable appearance.
"""},
            {"role" : "assistant",
             "content" : """
             당신은 매우 스타일리시한 락 스타 스타일이군요. 검정색 가죽 자켓을 입고 있는데 자켓은 몸에 딱 맞게 잘 핏되어 있네요. 그 아래에는 검은색 셔츠가 조금 보이는데, 자켓과 잘 어울려 전체적으로 어두운 분위기를 잘 살리고 있네요.
             당신의 헤어스타일도 눈에 띠는데, 깔끔하게 잘 컷된 머릿결이 자켓 칼라 바로 위에 떨어지는군요. 헤어 컬러도 깊고 짙은 색이라서 배경과 대조적이어서 더 돋보이는 것 같아요. 추가적으로 어두운 아이라이너와 스모키 메이크업이 당신의 눈을 강조하고 있어요. 
             그리고 매우 강렬한 레드 립스틱이 전체적인 스타일을 한층 더 돋보이게 만들고 있네요. 결론적으로 말하자면, 당신은 어두운 색상을 좋아하고, 잘 정돈된 아이템을 선호하는 것 같네요. 가죽 자켓, 단추 셔츠, 그리고 강렬한 메이크업의 조합은 그의 존재감을 매우 두드러지게 만들어. 엣지있고 세련된 스타일에 중점을 둔 사람으로 보여요. 
             """
        }]
        if history != []:
            message.extend(history)
        message.append(
            {"role": "user",
             "content": input_text}
        )
        key = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=message
        )
        response = key['choices'][0]['message']['content']
        return response
    except Exception as e:
        print(e)
        return ''

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def send_gpt_message(input_text, history, input_image_path=None):
    try:
        message = []
        if history!=[]:
            message.extend(history)

        if input_image_path != '':
            img = encode_image(input_image_path)
            message.extend([
                {"role": "system",
                 "content": input_text},
                {"role": "user",
                 "content": [
                     {"type": "image_url",
                      "image_url": {
                          "url": f'data:image/png;base64,{img}'
                      }}
                 ]}
            ])
        else:
            message.append(
                {"role" : "user",
                 "content": input_text}
            )
        key = client.chat.completions.create(
            model="gpt-4o",
            messages = message
        )
        response = key.choices[0].message.content
        return response
    except Exception as e:
        print(e)
        return ''

def next_txt_filename(directory):
    txt_files = [f for f in os.listdir(directory) if f.endswith('.md')]
    indices = [int(f.split('.')[0]) for f in txt_files]
    next_index = max(indices) + 1 if indices else 1

    new_txt_filename = str(next_index)+'.md'
    return os.path.join(directory, new_txt_filename)

def write_history(file_name, chat_list):
    with open(file_name, mode='a', encoding='utf-8') as f:
        for chat in chat_list:
            role = chat['role']
            content = chat['content']
            text = f'**{role}** : {content} \n'
            f.write(text)
            f.write('\n')
        f.write('\n---------------------------------------\n')
        f.close()

def txt_to_input(input_message):
    with open(input_message, mode='r', encoding='utf-8') as f:
        message = f.read()
    return message


if __name__ == "__main__":
    end = False
    history = []
    file_name = next_txt_filename(os.path.join('gpt_history', now))
    while not end:
        input_message = input('원하는 걸 입력하시오: ')
        img_message = input('이미지 path를 입력하시오: ')
        if input_message == 'exit':
            end = True
        elif input_message == 'new_session':
            history = []
            file_name = next_txt_filename(os.path.join('gpt_history', now))
        else:
            if input_message.endswith('.txt'):
                input_message = txt_to_input(input_message)
            response = send_gpt_message(input_message, history, img_message)
            print(response)
            user_chat = {"role" : "user",
                        "content" : input_message}
            answer_chat = {"role": "assistant",
                        "content": response}
            write_history(file_name, [user_chat, answer_chat])

            history.extend([user_chat, answer_chat])

