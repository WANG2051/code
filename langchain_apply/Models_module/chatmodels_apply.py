from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.chat_models import ChatOllama
model = ChatOllama(model="qwen2.5:7b")
messages = [
        SystemMessage(content="现在你是一个著名的诗人"),
        HumanMessage(content="给我写一首唐诗")
]
res = model.invoke(messages)
print(res)
print(res.content)

# 加入AIMessage
messages = [
        SystemMessage(content="现在你是一个著名的诗人"),
        HumanMessage(content="给我写一首唐诗"),
        AIMessage(content='清风明月夜，独坐思故人。\n江水东流去，孤舟何处人？\n花落知多少，柳暗闭重门。\n唯有心中意，常随鹤归云。'),
        HumanMessage(content="给我写一首宋词"),
]
res = model.invoke(messages)
print(res)
print(res.content)


