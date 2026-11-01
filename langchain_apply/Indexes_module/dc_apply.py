from langchain_community.document_loaders import TextLoader
loader = TextLoader('衣服属性.txt', encoding='utf8')
docs = loader.load()
print(docs)
print(len(docs))
a = docs[0].page_content[:4]
print(a)
#
# print('*'*80)
# from langchain_community.document_loaders import UnstructuredFileLoader
# loader = UnstructuredFileLoader('衣服属性.txt', encoding='utf8')
# docs = loader.load()
# print(docs)
# print(len(docs))
# a = docs[0].page_content[:4]
# print(a)