import json
from llm import ask_ai, ask_ai_stream
from memory import (
    get_memory_summary,
    get_relevant_memory,
    add_emotion,
    add_fact
)


# ---------------- MAIN BRAIN (NEW CORE) ----------------
def think(user_input, model="mistral", stream=False):
    """
    This is now the MAIN function your assistant should use.
    """

    # Quick check for simple prompts to skip heavy reasoning
    if is_simple_prompt(user_input):
        return generate_simple_response(user_input, stream)

    memory = get_memory_summary()
    relevant_memory = get_relevant_memory(user_input)

    personality = memory.get("personality_profile", {})
    prefs = memory.get("preferences", {})

    tone = personality.get("tone", "neutral")
    emotion = personality.get("emotion_state", "stable")

    # ---------------- MEMORY CONTEXT BLOCK ----------------
    memory_block = "\n".join(relevant_memory[-8:])

    # ---------------- SYSTEM PROMPT ----------------
    system_prompt = f"""
You are L.U.M.E.N, a personal AI assistant.

You have memory about the user.

PERSONALITY STATE:
- Tone: {tone}
- Emotional understanding: {emotion}

USER PREFERENCES:
{json.dumps(prefs, indent=2)}

RELEVANT MEMORY:
{memory_block}

INSTRUCTIONS:
- Use memory naturally, do NOT repeat it mechanically
- Adapt tone based on emotional state
- Be conversational and helpful
- If user is stressed, be calmer
- If user is excited, match energy
- Keep responses concise and average length unless the user asks for more detail
- Prefer meaningful, compact wording with a complex personality
- Do not mention "memory system"

TOOL USAGE:
- If user asks to create a file: output {"type": "create_file", "path": "full_path", "content": "file_content"}
- If user asks to read a file: output {"type": "read_file", "path": "full_path"}
- If user asks to delete a file: output {"type": "delete_file", "path": "full_path"}
- If user asks to open an app: output {"type": "open_app", "target": "app_name"}
- For chat responses: output normal text

User message:
{user_input}
"""

    if stream:
        raw_stream = ask_ai_stream(system_prompt, model)

        def response_stream():
            full_response = []
            for chunk in raw_stream:
                full_response.append(chunk)
                yield chunk

            reply = "".join(full_response)
            detect_emotion(user_input)
            auto_store_memory(user_input, reply)

        return response_stream()

    response = ask_ai(system_prompt, model)

    # ---------------- AUTO-EMOTION DETECTION ----------------
    detect_emotion(user_input)

    # ---------------- AUTO-MEMORY STORAGE ----------------
    auto_store_memory(user_input, response)

    return response


# ---------------- SIMPLE PROMPT DETECTOR ----------------
def is_simple_prompt(text):
    """Check if prompt is simple enough to skip heavy reasoning"""
    t = text.lower().strip()

    # Short prompts
    if len(t) < 30:
        return True

    # Basic questions
    simple_patterns = [
        "hello", "hi", "how are you", "what's up",
        "good morning", "good evening", "thanks", "thank you",
        "yes", "no", "ok", "okay", "sure", "maybe",
        "what time", "what day", "how's the weather",
        "tell me a joke", "sing a song", "play music"
    ]

    if any(p in t for p in simple_patterns):
        return True

    # No complex words
    complex_words = ["explain", "analyze", "design", "optimize", "compare", "build", "why", "how"]
    if not any(w in t for w in complex_words):
        return True

    return False


# ---------------- SIMPLE RESPONSE GENERATOR ----------------
def generate_simple_response(user_input, stream=False):
    """Generate quick response for simple prompts"""
    simple_prompt = f"You are L.U.M.E.N, a helpful assistant. Respond concisely to: {user_input}"

    if stream:
        raw_stream = ask_ai_stream(simple_prompt, "phi3", simple=True)  # Force fast model and simple mode

        def simple_stream():
            full_response = []
            for chunk in raw_stream:
                full_response.append(chunk)
                yield chunk

            reply = "".join(full_response)
            detect_emotion(user_input)
            auto_store_memory(user_input, reply)

        return simple_stream()

    response = ask_ai(simple_prompt, "phi3")  # Force fast model

    detect_emotion(user_input)
    auto_store_memory(user_input, response)

    return response


# ---------------- EMOTION DETECTION (LIGHTWEIGHT) ----------------
def detect_emotion(text):
    t = text.lower()

    if any(word in t for word in ["angry", "frustrated", "hate", "annoyed"]):
        add_emotion("stress", 2, text)

    elif any(word in t for word in ["happy", "love", "great", "awesome", "excited"]):
        add_emotion("positive", 2, text)

    elif any(word in t for word in ["confused", "don't understand", "lost"]):
        add_emotion("confusion", 2, text)


# ---------------- AUTO MEMORY WRITING ----------------
def auto_store_memory(user_input, ai_response):
    """
    Decides what is worth remembering automatically
    """

    important_keywords = [
        "i am", "my name", "i like", "i love",
        "i hate", "i want", "remember"
    ]

    text = user_input.lower()

    if any(k in text for k in important_keywords):
        add_fact(user_input, importance=2, tags=["user_statement"])

    # store AI helpful responses occasionally
    if len(ai_response) > 200:
        add_fact(ai_response[:200], importance=1, tags=["assistant_insight"])


# ---------------- BACKWARDS COMPATIBILITY ----------------
def ask_model(prompt, model):
    return ask_ai(prompt, model)