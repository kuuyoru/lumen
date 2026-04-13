"""
llm.py - Unified LLM interface
Breaks circular dependency between brain.py and memory.py
"""
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_TOKEN_LIMIT = 128  # Reduced for faster responses
DEFAULT_TEMPERATURE = 0.5  # Lower for quicker generation
DEFAULT_TIMEOUT = 30  # Shorter timeout for speed  # Shorter timeout for speed


def ask_ai(prompt, model="mistral", timeout=DEFAULT_TIMEOUT):
    """Core LLM interface - centralized here to avoid circular imports"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "max_tokens": DEFAULT_TOKEN_LIMIT,
                "temperature": DEFAULT_TEMPERATURE
            },
            timeout=timeout
        )

        response.raise_for_status()
        return response.json().get("response", "No response received.")

    except requests.exceptions.ConnectionError:
        return "Error: Ollama not running on localhost:11434"

    except Exception as e:
        return f"Error: {str(e)}"


def ask_ai_stream(prompt, model="mistral", timeout=DEFAULT_TIMEOUT, simple=False):
    """Stream LLM output in smaller chunks for progressive typing."""
    token_limit = 128 if simple else DEFAULT_TOKEN_LIMIT  # Even smaller for simple prompts
    temp = 0.4 if simple else DEFAULT_TEMPERATURE  # More deterministic for speed
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": True,
                "max_tokens": DEFAULT_TOKEN_LIMIT,
                "temperature": DEFAULT_TEMPERATURE
            },
            stream=True,
            timeout=timeout
        )

        response.raise_for_status()

        def stream_generator():
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue

                if isinstance(line, bytes):
                    try:
                        text = line.decode("utf-8", errors="ignore").strip()
                    except Exception:
                        text = str(line).strip()
                else:
                    text = str(line).strip()

                if text.startswith("data:"):
                    text = text[5:].strip()
                if not text or text in ("[DONE]", "done"):
                    continue

                try:
                    payload = json.loads(text)
                except json.JSONDecodeError:
                    yield text
                    continue

                if isinstance(payload, dict):
                    partial = payload.get("response") or payload.get("content", "")
                    if not partial and isinstance(payload.get("choices"), list):
                        first_choice = payload["choices"][0]
                        if isinstance(first_choice, dict):
                            partial = first_choice.get("delta", {}).get("content", "")
                            if not partial:
                                partial = first_choice.get("text", "")
                    if partial:
                        yield partial
                else:
                    yield str(payload)

        return stream_generator()

    except Exception as e:
        error_msg = str(e)
        def error_generator():
            yield f"Error: {error_msg}"
        return error_generator()
