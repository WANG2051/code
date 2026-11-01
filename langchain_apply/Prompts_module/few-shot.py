from langchain import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms import Ollama
model = Ollama(model="qwen2.5:7b")

examples = [
    {"word": "开心", "antonym": "难过"},
    {"word": "高", "antonym": "矮"},
]

example_template = """
单词: {word}
反义词: {antonym}\\n
"""

example_prompt = PromptTemplate(
    input_variables=["word", "antonym"],
    template=example_template,
)

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="给出每个单词的反义词",
    suffix="单词: {input}\\n反义词:",
    input_variables=["input"],
    example_separator="\\n",
)

prompt_text = few_shot_prompt.format(input="粗")
print(prompt_text)
print('*'*80)
# 给出每个单词的反义词
# 单词: 开心
# 反义词: 难过

# 单词: 高
# 反义词: 矮

# 单词: 粗
# 反义词:

# # 调用模型
print(model.invoke(prompt_text))

# 细