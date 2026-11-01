from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens
from transformers import AutoTokenizer, AutoModel
from typing import List, Optional


class ChatGLM2(LLM):
    max_token: int = 4096
    temperature: float = 0.8
    top_p = 0.9
    tokenizer: object = None
    model: object = None
    history = []

    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "ChatGLM2"

    # 定义load_model方法，进行模型的加载
    def load_model(self, model_path=None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).float()

    # 实现_call方法，进行模型的推理
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response, _ = self.model.chat(
            self.tokenizer,
            prompt,
            history=self.history,
            max_length=self.max_token,
            temperature=self.temperature,
            top_p=self.top_p)
        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        self.history = self.history + [[None, response]]
        return response


if __name__ == "__main__":
    llm = ChatGLM2()
    llm.load_model("/Users/ligang/PycharmProjects/llm/ChatGLM-6B/model/chatglm-6b-int4")
    print(llm._call("如何读一本书"))

