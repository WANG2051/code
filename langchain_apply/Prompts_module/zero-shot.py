from langchain import PromptTemplate
from langchain_community.llms import Ollama
model = Ollama(model="qwen2.5:7b")
# 定义模板
# template = "我的邻居姓{lastname}，他生了个儿子，给他儿子起个名字"
template = "我的邻居姓{lastname}，他的妻子姓{wname}，他生了个儿子，结合两人的姓氏，给他儿子起个名字"

prompt = PromptTemplate(
    input_variables=["lastname", 'wname'],
    template=template,
)

# prompt_text = prompt.format(lastname="王")
prompt_text = prompt.format(lastname="王", wname="李")
print(f'prompt_text-->{prompt_text}')
# result: 我的邻居姓王，他生了个儿子，给他儿子起个名字


result = model.invoke(prompt_text)
print(result)