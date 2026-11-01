from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_community.agent_toolkits.load_tools import load_tools

#  实例化大模型
llm = Ollama(model="qwen2.5:7b")

#  设置工具
# "serpapi"实时联网搜素工具、"math": 数学计算的工具
# tools = load_tools(["serpapi", "llm-math"], llm=llm)
tools = load_tools(["llm-math"], llm=llm)

# 实例化代理Agent:返回 AgentExecutor 类型的实例
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

print('agent', agent)
print('*'*80)
# 准备提示词
prompt_template = """解以下方程：3x + 4(x + 2) - 84 = y; 其中x为3，请问y是多少？"""
prompt = PromptTemplate.from_template(prompt_template)
# print('prompt-->', prompt)
print('*'*80)
# # 代理Agent工作
result = agent.run(prompt_template)
print(f'result-->{result}')



