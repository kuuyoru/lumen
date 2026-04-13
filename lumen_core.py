"""
lumen_core.py - Core autonomous processing logic
Handles emotional tracking, memory consolidation, and autonomous reflection
"""
import time
from brain import think
from memory import (
    add_fact,
    add_emotion,
    get_memory_summary,
    build_personality_profile
)

# ============ CORE STATE ============
conversation_buffer = []
BUFFER_LIMIT = 8


# ============ MAIN ENTRY POINT ============
def process_user_input(user_input, stream=False):
    """
    Main autonomous entry point for L.U.M.E.N
    Processes user input through the full AI pipeline
    """

    # Store conversation
    conversation_buffer.append(user_input)

    # Keep buffer small for memory efficiency
    if len(conversation_buffer) > BUFFER_LIMIT:
        conversation_buffer.pop(0)

    # 1. Detect emotional shifts
    emotional_check(user_input)

    # 2. Generate response using brain
    response = think(user_input, stream=stream)

    if hasattr(response, "__iter__") and not isinstance(response, str):
        def stream_wrapper():
            full_response = []
            for chunk in response:
                full_response.append(chunk)
                yield chunk
            autonomous_reflection(user_input, "".join(full_response))

        return stream_wrapper()

    # 3. Autonomous reflection and learning
    autonomous_reflection(user_input, response)

    return response


# ============ EMOTIONAL TRACKING ============
def emotional_check(text):
    """Detect and track emotional keywords in user input"""
    t = text.lower()

    if any(w in t for w in ["angry", "mad", "frustrated", "hate"]):
        add_emotion("stress", 2, text)

    elif any(w in t for w in ["happy", "love", "great", "awesome"]):
        add_emotion("positive", 2, text)

    elif any(w in t for w in ["confused", "don't understand", "lost"]):
        add_emotion("confusion", 2, text)


# ============ AUTONOMOUS REFLECTION ENGINE ============
def autonomous_reflection(user_input, response):
    """
    Analyzes conversations and automatically learns from patterns
    This is where L.U.M.E.N develops personality over time
    """

    summary = get_memory_summary()
    personality = build_personality_profile()

    # Trigger reflection occasionally (every 3rd conversation)
    if len(conversation_buffer) % 3 != 0:
        return

    # ---- Decide importance of conversation ----
    importance_score = evaluate_importance(user_input, response)

    if importance_score >= 2:
        add_fact(
            f"User said: {user_input}",
            importance=importance_score,
            tags=["autonomous_memory"]
        )

    # ---- Personality drift (slow learning) ----
    adapt_personality(personality)


# ============ IMPORTANCE EVALUATION ============
def evaluate_importance(user_input, response):
    """Score how important a conversation is for memory storage"""
    score = 0

    important_words = [
        "my", "i am", "i want", "remember", "important",
        "project", "school", "stress", "help"
    ]

    text = user_input.lower()

    for word in important_words:
        if word in text:
            score += 1

    # Longer responses are usually more important
    if len(response) > 200:
        score += 1

    return score


# ============ PERSONALITY DRIFT SYSTEM ============
def adapt_personality(profile):
    """
    Slowly evolves assistant personality based on user interactions
    Creates a unique AI personality over time
    """

    tone = profile.get("tone", "neutral")

    if tone == "supportive":
        add_fact("User prefers supportive tone", importance=1, tags=["personality"])
    elif tone == "energetic":
        add_fact("User responds well to energy", importance=1, tags=["personality"])


# ============ BACKGROUND THINKING (OPTIONAL) ============
def run_background_thinker():
    """
    Can be called periodically (e.g., every 5 minutes) for autonomous processing
    Triggers memory maintenance, consolidation, and analysis
    Good for when the assistant needs to 'think' between interactions
    """

    summary = get_memory_summary()

    # Lightweight cleanup signal
    if len(summary.get("important_memory", [])) > 10:
        add_fact("Memory system is becoming dense", importance=1, tags=["system"])