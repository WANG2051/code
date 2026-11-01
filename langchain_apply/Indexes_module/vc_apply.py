from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

# pku.txt内容：<https://www.pku.edu.cn/about.html>
with open('./pku.txt') as f:
    state_of_the_union = f.read()
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_text(state_of_the_union)
print(f'texts-->{texts}')
print(f'len(texts)-->{len(texts)}')
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

docsearch = Chroma.from_texts(texts, embeddings)

query = "1937年北京大学发生了什么？"
docs = docsearch.similarity_search(query, k=1)
print(f'docs==>{docs}')
print(f'len(docs)==>{len(docs)}')