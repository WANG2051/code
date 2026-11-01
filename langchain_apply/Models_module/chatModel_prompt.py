
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

# 创建原始模板
template_str = """您是一位专业的鲜花店文案撰写员。\n
对于售价为 {price} 元的 {flower_name} ，您能提供一个吸引人的简短描述吗？
# """


# 根据原始模板创建LangChain提示模板
promp_emplate = ChatPromptTemplate.from_template(template_str)
prompt = promp_emplate.format_messages(price='50', flower_name=["玫瑰"], )
print('prompt-->', prompt)
# 实例化模型
model = ChatOllama(model="qwen2:1.5b", temperature=0)

# 打印结果
result = model.invoke(prompt)
print(result.content)