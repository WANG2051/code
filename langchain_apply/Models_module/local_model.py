# -*-coding:utf-8-*-
# todo:基于python第三方库实现ollama的应用
import ollama
messages = []
messages.append({'role': 'user', 'content': '你知道周杰伦吗', })
response = ollama.chat(model='qwen2.5:7b',
                       messages=messages)
# print(response)
# print('*'*80)
print(response['message']['content'])
# # 记录Assistant对话
messages.append({'role': 'assistant', 'content': response['message']['content'], })
messages.append({'role': 'user', 'content': "他有什么好听的歌曲" })
response = ollama.chat(model='qwen2.5:7b',
                       messages=messages)
print('*'*80)
print('222', response['message']['content'])
#todo: 可以远程调用ollama
# import ollama
#
# print(ollama.show('qwen2:1.5b'))
# from ollama import Client as oClient
# # 远程服务器
# # oclient = oClient(host='http://192.168.1.100:11434')
# oclient = oClient(host='http://127.0.0.1:11434')
#
# response = oclient.chat(model='qwen2.5:7b', messages=[
#   {
#     'role': 'user',
#     'content': '为什么天空是蓝色的？',
#   },
# ])
# print(response['message']['content'])
# #
#
# # # todo:基于lanchain框架实现ollama的应用
# from langchain_community.llms import Ollama
# model = Ollama(base_url="http://127.0.0.1:11434", model="qwen2:1.5b", temperature=0)
# print(model)
# print(model.invoke("请给我讲个鬼故事"))
#
#
# ## todo: requests调用ollama
# import requests
# host= "127.0.0.1"
# port= "11434"
# url = f"http://{host}:{port}/api/chat"
# model = "qwen2:1.5b"
# headers = {"Content-Type": "application/json"}
# data = {
#         "model": model, #模型选择
#         "options": {
#             "temperature": 0.  #为0表示不让模型自由发挥，输出结果相对较固定，>0的话，输出的结果会比较放飞自我
#          },
#         "stream": False, #流式输出
#         "messages": [{
#             "role": "system",
#             "content":"你是谁？"
#         }] #对话列表
#     }
# response = requests.post(url, json=data, headers=headers, timeout=60)
# res = response.json()
# print(res["message"]["content"])
#
#



# import ollama
# stream = ollama.chat(
#  model='qwen2.5:7b',
#  messages=[{'role': 'user', 'content': '为什么天空是蓝⾊的？'}],
#  stream=True,
# )
# print(f'stream--》{stream}')
# for chunk in stream:
#     print(chunk['message']['content'], end='', flush=True)
