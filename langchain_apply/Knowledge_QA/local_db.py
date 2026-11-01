from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS # 向量数据库


def get_vector():
    # 第一步：加载文档
    loader = PyMuPDFLoader("物流信息.pdf")
    # 将文本转成 Document 对象
    data = loader.load()
    print(f'data-->{data}')
    print(f'len(data):{len(data)}')

    # # 第二步：切分文本
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=20)
    # # 切割加载的 document
    split_docs = text_splitter.split_documents(data)
    print("split_docs size:", len(split_docs))
    print(split_docs)
    #
    # # 第三步：初始化 hugginFace 的 embeddings 对象
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    #
    #
    # # 第四步：将 document通过embeddings对象计算得到向量信息并永久存入FAISS向量数据库，用于后续匹配查询
    db = FAISS.from_documents(split_docs, embeddings)
    db.save_local("./faiss/wuliu")

if __name__ == '__main__':
    result = get_vector()