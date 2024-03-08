import os
import datetime
import openai
import configparser

properties = configparser.ConfigParser()
properties.read('authentication.ini')
openai.api_key = properties['GPT_AUTH']['api_key']
now = datetime.datetime.now().strftime('%Y-%m-%d')
os.makedirs(os.path.join('gpt_history', now), exist_ok=True)

def send_gpt_message(input_text, history):
    try:
        message = []
        if history!=[]:
            message.extend(history)
        message.append(
            {"role" : "user",
             "content": input_text}
        )
        key = openai.ChatCompletion.create(
            model="gpt-4",
            messages = message
        )
        response = key['choices'][0]['message']['content']
        return response
    except Exception as e:
        print(e)
        return ''

def next_txt_filename(directory):
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    indices = [int(f.split('.')[0]) for f in txt_files]
    next_index = max(indices) + 1 if indices else 1
    new_txt_filename = str(next_index)+'.txt'
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

if __name__ == "__main__":
    end = False
    history = []
    file_name = next_txt_filename(os.path.join('gpt_history', now))
    while not end:
        input_message = input('원하는 걸 입력하시오: ')
        if input_message == 'exit':
            end = True
        elif input_message == 'new_session':
            history = []
            file_name = next_txt_filename(os.path.join('gpt_history', now))
        else:
            response = send_gpt_message(input_message, history)
            print(response)
            user_chat = {"role" : "user",
                        "content" : input_message}
            answer_chat = {"role": "assistant",
                        "content": response}
            write_history(file_name, [user_chat, answer_chat])

            history.extend([user_chat, answer_chat])

