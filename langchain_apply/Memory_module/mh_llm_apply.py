from langchain import ConversationChain
from langchain_community.llms import Ollama

#  实例化大模型
llm = Ollama(model="qwen2.5:7b")
conversation = ConversationChain(llm=llm)
resut1 = conversation.predict(input="小明有1只猫")
print(resut1)
print('*'*80)
resut2 = conversation.predict(input="小刚有2只狗")
print(resut2)
print('*'*80)
resut3 = conversation.predict(input="小明和小刚一共有几只宠物?")
print(resut3)
print('*'*80)