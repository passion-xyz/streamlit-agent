from langchain.memory import (
    ChatMessageHistory,
    ConversationSummaryMemory
)
from llm import llm_non_stream

messages_history = ChatMessageHistory()
summaries = []
summarizer = ConversationSummaryMemory(
    llm=llm_non_stream, return_messages=False)
