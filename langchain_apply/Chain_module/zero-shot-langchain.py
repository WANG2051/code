from langchain import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain

# 定义模板
template = "我的邻居姓{lastname}，他生了个儿子，给他儿子起个名字"

prompt = PromptTemplate(
    input_variables=["lastname"],
    template=template,
)

llm = Ollama(model="qwen2.5:7b")

chain = LLMChain(llm=llm, prompt=prompt)
# chain = prompt | llm
# 执行链
# print(chain.run("王"))
print(chain.invoke("王"))


