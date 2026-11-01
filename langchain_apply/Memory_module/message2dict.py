from langchain.memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_to_dict
from langchain_community.llms import Ollama

#  实例化大模型
llm = Ollama(model="qwen2.5:7b")

history = ChatMessageHistory()
history.add_user_message("hi!")
history.add_ai_message("whats up?")

dicts = messages_to_dict(history.messages)

print(dicts)
# [{'type': 'human', 'data': {'content': 'hi!', 'additional_kwargs': {}}},
# {'type': 'ai', 'data': {'content': 'whats up?', 'additional_kwargs': {}}}]
# 读取历史消息
new_messages = messages_from_dict(dicts)

print(new_messages)
