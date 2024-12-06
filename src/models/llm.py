from langchain_aws import ChatBedrock
from langchain_core.language_models import BaseChatModel
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


class LLM:
    def __init__(self, model_name: str, temperature: float):
        self.model = self._initialize_llm(model_name, temperature)

    def _initialize_llm(self, model_name: str, temperature: float) -> BaseChatModel:
        if model_name == "gpt-4o":
            return ChatOpenAI(model="gpt-4o", temperature=temperature)
        elif model_name == "claude-3-5":
            return ChatBedrock(
                model="anthropic.claude-3-5-sonnet-20241022-v2:0",
                temperature=temperature,
                region="us-west-2",
            )
        else:
            raise ValueError(f"Model name {model_name} not supported.")

    def __call__(self, input: LanguageModelInput, structure: BaseModel) -> BaseMessage:
        """structured_outputを持つLLMの呼び出し"""
        try:
            structured_llm = self.model.with_structured_output(structure)
            return structured_llm.invoke(input)
        except Exception as e:
            raise e
