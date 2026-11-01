from local_qa import *
# ConversationalRetrievalChain作用：自动保存历史对话信息
from langchain.chains import ConversationalRetrievalChain
import streamlit as st

# 设置标题
st.set_page_config(page_title="物流行业信息咨询系统")
st.title("物流行业信息咨询RAG系统")

# 初始化全局变量
chat_history = []


# 定义检索链函数
def new_retrival():
    """
    创建基于 ConversationalRetrievalChain 的问答链。
    """
    chain = ConversationalRetrievalChain.from_llm(
        llm=Ollama(model="qwen2.5:7b"),  # 使用本地大模型
        retriever=db.as_retriever()        # 基于本地数据库的检索器
    )
    return chain

# 主逻辑
def main():
    """
    Streamlit 主页面的交互逻辑。
    """
    # print(f'st.session_state-->{st.session_state}')
    # 初始化会话状态
    if "messages" not in st.session_state:
        st.session_state.messages = []  # 用于保存聊天记录
    # print(f'st.session_state-->{st.session_state}')
    # 展示历史聊天记录
    for message in st.session_state.messages:
        # print(f'message["role"]-->{message["role"]}')
        with st.chat_message(message["role"]):
            st.markdown(message["content"])  # 显示消息内容

    # 接受用户输入
    # prompt = st.chat_input("请输入你的问题:")
    if prompt := st.chat_input("请输入你的问题:"):
        # 保存用户消息到会话状态
        print(f'prompt--》{prompt}')
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 显示用户输入
        with st.chat_message("user"):
            st.markdown(prompt)

        # 调用模型获取回答
        with st.chat_message("assistant"):
            # 占位符用于显示逐字生成的回答
            message_placeholder = st.empty()
            full_response = ""

            # 调用检索链获取答案
            chain = new_retrival()
            result = chain.invoke({"question": prompt, "chat_history": chat_history})
            print(f'result--->{result}')
            chat_history.append((prompt, result["answer"]))  # 更新聊天历史
            assistant_response = result["answer"]
            message_placeholder.markdown(assistant_response)

            # 保存回答到会话状态
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# 运行主逻辑
if __name__ == "__main__":
    main()
