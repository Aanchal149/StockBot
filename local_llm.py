from langchain_community.llms import Ollama

def get_local_llm():
    return Ollama(
        model="tinyllama",
        temperature=0.3,
        num_ctx=1024,
        timeout=120
    )

