"""
src/core/llm_provider.py
Centralized deterministic LLM provider for the agentic firewall pipeline.
"""
from langchain_ollama import ChatOllama


def get_llm(
    model_name: str = "llama3.1:8b",
    temperature: float = 0.0,
    base_url: str = "http://localhost:11434"
) -> ChatOllama:
    """
    Returns a configured ChatOllama instance.
    Temperature is strictly fixed at 0.0 to guarantee reproducible security benchmarks.
    """
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        num_predict=512,
        base_url=base_url
    )


if __name__ == "__main__":
    print("[*] Initializing Ollama provider test...")
    llm = get_llm()
    try:
        response = llm.invoke("Respond with: PROVIDER READY")
        print(f"[✓] Connection successful: {response.content.strip()}")
    except Exception as e:
        print(f"[✗] Failed to connect to Ollama: {e}")