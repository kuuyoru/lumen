import json
import os
from memory import get_memory_summary

# ----------------------------
# MODEL MAP
# ----------------------------
MODELS = {
    "fast": "phi3",
    "balanced": "mistral"
}

DEFAULT_MODEL = MODELS["fast"]

# ----------------------------
# LEARNING FILE (persistent memory)
# ----------------------------
LEARNING_FILE = "router_learning.json"


# ----------------------------
# LOAD LEARNING DATA
# ----------------------------
def load_learning():
    if not os.path.exists(LEARNING_FILE):
        return {"history": []}

    try:
        with open(LEARNING_FILE, "r") as f:
            return json.load(f)
    except:
        return {"history": []}


# ----------------------------
# SAVE LEARNING DATA
# ----------------------------
def save_learning(data):
    try:
        with open(LEARNING_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass


# ----------------------------
# USER OVERRIDE DETECTION
# ----------------------------
def detect_user_override(text):
    t = text.lower()

    if any(x in t for x in [
        "light mode", "fast mode", "quick mode",
        "use light", "use fast", "phi3 only"
    ]):
        return MODELS["fast"]

    if any(x in t for x in [
        "deep mode", "best model",
        "strongest", "use strongest",
        "think thoroughly", "analyze deeply", "full capacity", "deep analysis"
    ]):
        return MODELS["balanced"]

    if any(x in t for x in [
        "balanced mode", "normal mode", "default mode"
    ]):
        return MODELS["balanced"]

    return None


# ----------------------------
# COMPLEXITY ENGINE
# ----------------------------
def estimate_complexity(text, memory):
    score = 0
    t = text.lower()

    if len(text) > 200:
        score += 2
    elif len(text) > 80:
        score += 1

    deep_words = [
        "explain", "why", "how", "analyze",
        "design", "optimize", "compare", "build"
    ]

    if any(w in t for w in deep_words):
        score += 2

    tool_words = [
        "file", "encrypt", "decrypt",
        "schedule", "delete", "create"
    ]

    if any(w in t for w in tool_words):
        score += 1

    if len(memory.get("important_memory", [])) > 6:
        score += 1

    return score


# ----------------------------
# CORE LEARNING SYSTEM
# ----------------------------
def update_learning(user_input, selected_model, final_model_used):
    """
    Stores routing decision outcomes for learning
    """

    data = load_learning()

    data["history"].append({
        "input": user_input,
        "chosen": selected_model,
        "final": final_model_used
    })

    # keep file small (last 200 entries)
    data["history"] = data["history"][-200:]

    save_learning(data)


# ----------------------------
# MODEL SCORE ADJUSTER
# ----------------------------
def learn_best_model(user_input, complexity):
    """
    Learns from past usage patterns
    """

    data = load_learning()
    history = data.get("history", [])

    # simple frequency-based learning
    fast_score = 0
    balanced_score = 0

    for h in history[-50:]:
        if h["final"] == MODELS["fast"]:
            fast_score += 1
        elif h["final"] == MODELS["balanced"]:
            balanced_score += 1

    # bias adjustment - prefer fast by default
    if complexity >= 4:
        balanced_score += 3
    else:
        fast_score += 3

    if balanced_score >= fast_score:
        return MODELS["balanced"]

    return MODELS["fast"]


# ----------------------------
# MAIN ROUTER
# ----------------------------
def choose_model(user_input):
    """
    Self-learning adaptive router
    """

    memory = get_memory_summary()

    # 1. user override wins
    override = detect_user_override(user_input)
    if override:
        return override

    # 2. estimate complexity
    complexity = estimate_complexity(user_input, memory)

    # 3. self-learning decision
    model = learn_best_model(user_input, complexity)

    return model


# ----------------------------
# FEEDBACK FUNCTION (IMPORTANT)
# ----------------------------
def feedback(user_input, selected_model, final_model_used=None):
    """
    Call this after response if model changed or user corrected system.
    Records learning data for future model selection.
    """
    if final_model_used is None:
        final_model_used = selected_model
    
    update_learning(user_input, selected_model, final_model_used)


# ----------------------------
# SAFETY WRAPPER
# ----------------------------
def safe_model(model_name):
    if model_name not in MODELS.values():
        return DEFAULT_MODEL
    return model_name