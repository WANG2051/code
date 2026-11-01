# coding:utf-8
# 导入必备的工具包
import time
from local_db import *
from langchain import PromptTemplate
from langchain_community.llms import Ollama


# 加载FAISS向量库
embeddings = OllamaEmbeddings(model="mxbai-embed-large", temperature=0)
db = FAISS.load_local("faiss/wuliu", embeddings, allow_dangerous_deserialization=True)
# db = FAISS.load_local("faiss/wuliu", embeddings)

start_time = time.time()


def get_related_content(related_docs):
    # print(f'related_docs--》{related_docs}')
    related_content = []
    for doc in related_docs:
        # print(f'doc.page_content--》{doc.page_content}')
        related_content.append(doc.page_content.replace("\n\n", "\n"))
    # print(f'related_content列表状态--》{related_content}')

    return "\n".join(related_content)


def define_prompt():
    question = '我的快递出发地是哪？预计几天的时间到达？'
    docs = db.similarity_search(question, k=2)

    related_content = get_related_content(docs)
    # print('*' * 80)
    # print(f'related_content字符串状态-->{related_content}')
    # print('*'*80)
    PROMPT_TEMPLATE = """
        基于以下已知信息，简洁和专业的来回答用户的问题。不允许在答案中添加编造成分。
        已知内容:
        {context}
        问题:
        {question}"""

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE,)

    my_pmt = prompt.format(context=related_content,
                           question=question)

    return my_pmt


def qa():
    model = Ollama(model="qwen2.5:7b")
    # print(f'model-->{model}')
    my_pmt = define_prompt()
    print(f'my_pmt--》{my_pmt}')
    # result = model.invoke(my_pmt)
    # return result



if __name__ == '__main__':
    result = qa()
    print(result)
    end_time = time.time()
    print(end_time-start_time)