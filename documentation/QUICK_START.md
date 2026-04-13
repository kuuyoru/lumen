# L.U.M.E.N. AI - Quick Start Guide

## 30-Second Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama
- Download: https://ollama.ai
- Run: `ollama serve` (keep running in background)

### 3. Pull Models
```bash
ollama pull mistral
ollama pull phi3
```

### 4. Start L.U.M.E.N
```bash
python main.py
```

**You're ready!**

---

## First Conversation

```
L.U.M.E.N ONLINE — CORE SYSTEM ACTIVE

Neural systems online. Awaiting input...

You: Hello! What can you do?
L.U.M.E.N: Hello! I'm L.U.M.E.N, an adaptive AI assistant. I can:
- Answer questions and provide explanations
- Remember your preferences and personal information
- Learn from our conversations over time
- Adapt my communication style to your needs
- Help with file operations and analysis
- Provide emotional intelligence in conversations

What would you like to know?

You: Remember my name is Alex
L.U.M.E.N: Got it! I'll remember your name is Alex.

You: exit
L.U.M.E.N: Shutting down...
```

---

## System Status Check

### Before Starting

**Checklist:**
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Dependencies installed (`pip list | grep ollama`)
- [ ] Ollama running (`curl http://localhost:11434/api/tags`)
- [ ] Models pulled (above command should list mistral, phi3)

### If Something Doesn't Work

**Issue:** "Error: Ollama not running"
```bash
# Solution: Start Ollama in another terminal
ollama serve
```

**Issue:** "ModuleNotFoundError: No module named 'ollama'"
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue:** "Connection refused on localhost:11434"
```bash
# Solution: Wait 5 seconds for Ollama to start fully
# Or check: ollama serve is running in background
```

---

## What Happens When You Start

**Initialization sequence:**
1. L.U.M.E.N loads memory from `memory_cache.json`
2. Checks Ollama connection
3. Initializes model router
4. Waits for input

**Files created automatically:**
- `memory_cache.json` - Your conversation memories
- `router_learning.json` - Model selection history
- `lumen.key` - Encryption key

**All safe to delete** (system recreates them):
```bash
rm memory_cache.json router_learning.json lumen.key
```

---

## Basic Commands

| What You Type | What Happens |
|---------------|--------------|
| Regular text | L.U.M.E.N responds|
| `exit` or `quit` | Shutdown gracefully |
| `Ctrl+C` | Emergency exit |

---

## Common First Interactions

### Teach Your Preferences
```
You: I prefer technical explanations with code examples
```

### Ask It to Remember
```
You: Remember: I work in AI/ML
You: My hobby is photography
```

### Test Multiple Models
```
You: Use fast mode - what's 2+2?
You: Use balanced mode - explain transformers
```

### Start Learning
```
You: I'm learning Python
L.U.M.E.N: Great! What aspect of Python interests you?
```

---

## Performance Tips

**For faster responses:**
1. Ask more specific questions
2. Use "fast mode" for simple queries
3. Give context in your question
4. Keep sentences focused

**For better answers:**
1. Use "balanced mode" for complex topics
2. Provide detailed context
3. Break multi-part questions into separate asks
4. Reference previous conversations

---

## Understanding the System

### Response Quality

```
Question: "What is AI?"

┌─ Fast (phi3) → 1-2 seconds
│  "AI is artificial intelligence"
│
└─ Balanced (mistral) → 3-5 seconds [DEFAULT]
   "AI is computational systems that mimic human intelligence..."
```

### Automatic Learning

```
Day 1: You ask about Python
        → System notes: "User interested in Python"

Day 10: You ask 5 more Python questions
        → System adaptation: "User prefers technical depth"

Day 30: Python question
        → Response automatically uses technical tone
```

---

## Troubleshooting Quick Reference

| Error | Reason | Fix |
|-------|--------|-----|
| "Connection refused" | Ollama not running | `ollama serve` |
| "No module named X" | Missing dependencies | `pip install -r requirements.txt` |
| "Memory not saving" | Permission issue | Check`memory_cache.json` is writable |
| "Slow responses" | Using balanced model | Try "fast mode" |
| "Downloaded model not found" | Ollama model issue | `ollama pull mistral` |

---

## What to Try First

1. **Say hello** - L.U.M.E.N responds naturally
2. **Tell it about yourself** - "I'm interested in AI"
3. **Ask a question** - Get an answer and explanation
4. **Give feedback** - "That was too complex" or "Perfect!"
5. **Explore features** - Try "Use balanced mode", "Remember: ...", etc.

---

## File Locations

All files stay in the same directory:
```
c:\L.U.M.E.N. ai\
├── main.py                          # Run this
├── memory_cache.json                # Your memories (auto-created)
├── router_learning.json             # Model learning (auto-created)
├── lumen.key                        # Encryption (auto-created)
├── USER_MANUAL.md                   # This guide
├── SETUP_AND_CONFIGURATION.md       # Detailed setup
├── README.md                        # Project overview
└── [other source files]
```

---

## Next: Read Full Manual

For advanced features, see: **[USER_MANUAL.md](USER_MANUAL.md)**

For detailed setup: **[SETUP_AND_CONFIGURATION.md](SETUP_AND_CONFIGURATION.md)**

---

**Ready to start? Run: `python main.py`**

**Questions? Check the full manuals.** 

Version: 1.0.0 | Last Updated: April 13, 2026
