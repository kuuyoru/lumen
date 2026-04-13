import json
import os
import time
import requests
from llm import ask_ai

# ---------------- FIREBASE CONFIG ----------------
FIREBASE_PROJECT_ID = "lumen-fe055"
FIREBASE_API_KEY = "AIzaSyABv1chnRzEuOrj1LBWl2t3tJpPfBl2g94"
FIREBASE_URL = f"https://{FIREBASE_PROJECT_ID}-default-rtdb.firebaseio.com"

# ---------------- LOCAL CACHE ----------------
LOCAL_CACHE_SIZE = 25

local_cache = {
    "facts": [],
    "preferences": {},
    "emotions": [],
    "identity": {},
    "skills": {},
    "last_sync": 0
}

# ---------------- FIREBASE CORE ----------------
def firebase_get(path=""):
    try:
        url = f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_API_KEY}"
        r = requests.get(url, timeout=5)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def firebase_put(path, data):
    try:
        url = f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_API_KEY}"
        r = requests.put(url, json=data, timeout=5)
        return r.status_code == 200
    except:
        return False

def firebase_patch(path, data):
    try:
        url = f"{FIREBASE_URL}/{path}.json?auth={FIREBASE_API_KEY}"
        r = requests.patch(url, json=data, timeout=5)
        return r.status_code == 200
    except:
        return False


# ---------------- CACHE SYSTEM ----------------
def load_from_cache():
    global local_cache
    file = "memory_cache.json"

    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                local_cache.update(json.load(f))
        except:
            pass

    local_cache.setdefault("facts", [])
    local_cache.setdefault("preferences", {})
    local_cache.setdefault("emotions", [])
    local_cache.setdefault("identity", {})
    local_cache.setdefault("skills", {})

def save_to_cache():
    try:
        with open("memory_cache.json", "w", encoding="utf-8") as f:
            json.dump(local_cache, f, indent=2)
    except:
        pass


# ---------------- SYNC ----------------
def sync_to_cloud():
    now = time.time()

    if now - local_cache.get("last_sync", 0) < 30:
        return

    key = "lumen_memory"

    firebase_put(f"{key}/preferences", local_cache["preferences"])
    firebase_put(f"{key}/emotions", local_cache["emotions"][-20:])
    firebase_put(f"{key}/facts", local_cache["facts"][-15:])

    local_cache["last_sync"] = now
    save_to_cache()


def load_from_cloud():
    key = "lumen_memory"
    cloud = firebase_get(key)

    if cloud:
        local_cache["preferences"] = cloud.get("preferences", {})
        local_cache["emotions"] = cloud.get("emotions", [])
        local_cache["facts"] = cloud.get("facts", []) + local_cache.get("facts", [])

        # remove duplicates
        seen = set()
        cleaned = []

        for f in reversed(local_cache["facts"]):
            t = f.get("text", "")
            if t not in seen:
                seen.add(t)
                cleaned.append(f)

        local_cache["facts"] = cleaned[-LOCAL_CACHE_SIZE:]

    return local_cache


# ---------------- EMOTIONS ----------------
def add_emotion(event_type, intensity=1, context=""):
    local_cache["emotions"].append({
        "type": event_type,
        "intensity": intensity,
        "context": context,
        "time": time.time()
    })

    local_cache["emotions"] = local_cache["emotions"][-50:]
    save_to_cache()


# ---------------- FACT STORAGE (UPGRADED) ----------------
def add_fact(text, importance=1, tags=None):
    if not local_cache.get("facts"):
        load_from_cache()

    entry = {
        "text": text,
        "time": time.time(),
        "importance": importance,
        "tags": tags or [],
        "relevance_score": importance
    }

    local_cache["facts"].append(entry)

    # prioritize important memories
    local_cache["facts"].sort(
        key=lambda x: x.get("relevance_score", 1),
        reverse=True
    )

    local_cache["facts"] = local_cache["facts"][:LOCAL_CACHE_SIZE]

    if len(local_cache["facts"]) % 5 == 0:
        apply_memory_decay()

    if len(local_cache["facts"]) >= LOCAL_CACHE_SIZE:
        consolidate_memories()

    # Don't sync on every add_fact - sync periodically instead
    # This reduces API calls dramatically (from thousands to ~2 per minute)
    save_to_cache()


# ---------------- MEMORY DECAY (SMART) ----------------
def apply_memory_decay():
    now = time.time()

    for f in local_cache.get("facts", []):
        age = (now - f.get("time", 0)) / 86400

        # only weak memories fade
        if f.get("importance", 1) == 1 and age > 3:
            f["relevance_score"] = max(0, f.get("relevance_score", 1) - 0.3)

    save_to_cache()


# ---------------- CONSOLIDATION ----------------
def consolidate_memories():
    if len(local_cache["facts"]) < 5:
        return

    recent = local_cache["facts"][-10:]
    text_blob = "\n".join([f"- {f['text']}" for f in recent])

    prompt = f"""
Summarize these memories into 2 clean insights:

{text_blob}
"""

    try:
        response = ask_ai(prompt, "mistral")

        lines = [l.strip("- ").strip() for l in response.split("\n") if l.strip()]

        new_facts = []
        for l in lines[:2]:
            new_facts.append({
                "text": l,
                "time": time.time(),
                "importance": 2,
                "relevance_score": 3
            })

        local_cache["facts"] = local_cache["facts"][:-10] + new_facts
        local_cache["facts"] = local_cache["facts"][-LOCAL_CACHE_SIZE:]

        save_to_cache()

    except:
        pass


# ---------------- RELEVANCE SCORING ----------------
def score_memory_relevance(fact, query):
    score = fact.get("importance", 1)

    text = fact.get("text", "").lower()
    query = query.lower()

    for word in query.split():
        if word in text:
            score += 2

    age = time.time() - fact.get("time", 0)

    if age < 86400:
        score += 2
    elif age < 604800:
        score += 1

    return score


def get_relevant_memory(query, limit=10):
    load_from_cloud()

    scored = []
    for f in local_cache.get("facts", []):
        scored.append((score_memory_relevance(f, query), f))

    scored.sort(reverse=True, key=lambda x: x[0])

    return [f["text"] for _, f in scored[:limit]]


# ---------------- PERSONALITY FUSION ENGINE ----------------
def build_personality_profile():
    profile = {
        "tone": "neutral",
        "emotion_state": "stable",
        "topics": [],
        "user_state": "normal"
    }

    emotions = local_cache.get("emotions", [])
    facts = local_cache.get("facts", [])

    # emotion analysis
    if emotions:
        recent = emotions[-10:]
        stress = sum(1 for e in recent if e["type"] == "stress")
        joy = sum(1 for e in recent if e["type"] == "positive")

        if stress > joy:
            profile["tone"] = "supportive"
            profile["emotion_state"] = "stressed"
        elif joy > stress:
            profile["tone"] = "energetic"
            profile["emotion_state"] = "positive"

    # topic detection
    topics = {}

    for f in facts[-30:]:
        t = f.get("text", "").lower()

        if "code" in t:
            topics["coding"] = topics.get("coding", 0) + 1
        if "school" in t:
            topics["school"] = topics.get("school", 0) + 1
        if "ai" in t:
            topics["ai"] = topics.get("ai", 0) + 1

    profile["topics"] = sorted(topics, key=topics.get, reverse=True)[:3]

    return profile


# ---------------- PREFERENCES ----------------
def set_preference(key, value):
    local_cache["preferences"][key] = value
    save_to_cache()

    try:
        firebase_put("lumen_memory/preferences", local_cache["preferences"])
    except:
        pass


def get_preferences():
    load_from_cloud()
    return local_cache.get("preferences", {})


# ---------------- SUMMARY FOR BRAIN ----------------
def get_memory_summary():
    load_from_cloud()

    return {
        "preferences": local_cache.get("preferences", {}),
        "important_memory": [
            f["text"]
            for f in local_cache.get("facts", [])
            if f.get("importance", 1) >= 2
        ][-15:],
        "personality_profile": build_personality_profile()
    }