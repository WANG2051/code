from langchain_community.llms import Ollama
# model = Ollama(model="qwen2.5:1.5b")
model = Ollama(model="qwen2.5:7b")
result = model.invoke("请给我讲个鬼故事")
print(result)