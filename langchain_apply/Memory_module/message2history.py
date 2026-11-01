from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()
history.add_user_message("在吗？")
history.add_ai_message("有什么事?")

print(history.messages)
