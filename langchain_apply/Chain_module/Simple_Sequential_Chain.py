from langchain import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import LLMChain, SimpleSequentialChain

# 创建第一条链
template = "我的邻居姓{lastname}，他生了个儿子，给他儿子起个名字"

first_prompt = PromptTemplate(
    input_variables=["lastname"],
    template=template,
)
llm = Ollama(model="qwen2.5:7b")


first_chain = LLMChain(llm=llm, prompt=first_prompt)

# 创建第二条链
second_prompt = PromptTemplate(
    input_variables=["child_name"],
    template="邻居的儿子名字叫{child_name}，给他起一个小名",
)

second_chain = LLMChain(llm=llm, prompt=second_prompt)


# 链接两条链
overall_chain = SimpleSequentialChain(chains=[first_chain, second_chain], verbose=False)

print(overall_chain)
print('*'*80)
# 执行链，只需要传入第一个参数
catchphrase = overall_chain.run("王")
print(catchphrase)