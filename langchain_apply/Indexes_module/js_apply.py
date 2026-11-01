from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

loader = TextLoader('./pku.txt')
documents = loader.load()
print(f'documents--》{documents}')
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
print(f'texts--》{texts}')
print(f'len(texts)--》{len(texts)}')

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db = FAISS.from_documents(texts, embeddings)
retriever = db.as_retriever(search_kwargs={'k': 1})
docs = retriever.get_relevant_documents("北京大学什么时候成立的")
print(docs)

#打印结果：
'''
[Document(metadata={'source': './pku.txt'}, page_content='北京大学创办于1898年，是戊戌变法的产物，也是中华民族救亡图存、兴学图强的结果，初名京师大学堂，是中国近现代第一所国立综合性大学，辛亥革命后，于1912年改为现名。')]
'''