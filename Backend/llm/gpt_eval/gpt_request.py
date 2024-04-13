import datetime
import openai
import os

os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

openai.api_base = 'https://api.ngapi.top/v1'
my_api_key = 'sk-ViH9iKkSZBW4zSsyB3238dA47d8044EeA608866630Cb0359'


def send_request_to_openai(model, my_api_key, messages):
    # 设置 OpenAI 的 API 密钥
    openai.api_key = my_api_key

    # 发送请求到 OpenAI
    response = openai.ChatCompletion.create(model=model, messages=messages,temperature=0.8)

    # 返回 OpenAI 的响应
    return response


def send_request(prompts):
    response = send_request_to_openai('gpt-3.5-turbo', my_api_key, [{'role': 'user', 'content': prompts}])
    return response.choices[0].message['content']
