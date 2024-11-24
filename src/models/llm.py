from langchain_google_genai import ChatGoogleGenerativeAI


def initialize_llm(model_name: str, temperature: float) -> ChatGoogleGenerativeAI:
    if model_name == "gemini":
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature)
    else:
        raise ValueError(f"Model name {model_name} not supported.")
