# L.U.M.E.N. AI Assistant - User Manual

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Features](#core-features)
3. [Communication Examples](#communication-examples)
4. [Memory & Learning](#memory--learning)
5. [Advanced Features](#advanced-features)
6. [Tips & Tricks](#tips--tricks)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Installation (5 minutes)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install & run Ollama:**
   - Download from https://ollama.ai
   - Run: `ollama serve`
   - In another terminal:
     ```bash
     ollama pull mistral
     ollama pull phi3


You're ready to go!

---

## Core Features

### 1. Smart Conversations

L.U.M.E.N understands context, remembers your preferences, and adapts communication style.

```
You: My name is Alex and I'm interested in AI
L.U.M.E.N: Nice to meet you, Alex! AI is fascinating. What aspect interests you most?

You: Specifically machine learning
L.U.M.E.N: Machine learning is a powerful subset of AI. Since you're interested in that...
```

**Note:** L.U.M.E.N remembers your name and past interests.

### 2. Adaptive Response Quality

The assistant automatically selects the best model based on question complexity:

- **Simple questions** → Fast model (phi3)
  - "What time is it?"
  - "How's the weather?"
  
- **Balanced questions** → Standard model (mistral) ← Default
  - "Explain how neural networks work"
  - "Help me with this problem"
  
- **Complex questions** → Balanced model (mistral)
  - "Design a system architecture"
  - "Deep analysis of this paper"

### 3. Memory System

L.U.M.E.N remembers important information automatically:

```
You: Remember, I have a meeting tomorrow at 2 PM
L.U.M.E.N: Got it. I'll remember you have a meeting tomorrow at 2 PM.

[Later...]

You: What do I have scheduled?
L.U.M.E.N: You mentioned you have a meeting tomorrow at 2 PM.
```

### 4. Emotional Intelligence

The assistant detects your emotional state and adapts responses:

```
You: I'm really frustrated with this code
L.U.M.E.N: I understand coding can be frustrating. Let's break this down step-by-step...

You: I finally got it working!
L.U.M.E.N: That's awesome! Great job pushing through that challenge!
```

### 5. File Operations

Safely create, read, and manage files:

```
You: Create a file called notes.txt with "My important notes"
L.U.M.E.N: [creates file after confirmation]

You: Read notes.txt
L.U.M.E.N: [displays file contents]

You: Delete notes.txt
L.U.M.E.N: [requires double confirmation for safety]
```

---

## Communication Examples

### Example 1: Getting Explanations

```
You: How do machine learning models learn?
L.U.M.E.N: Machine learning models learn through a process called training. Here's how it works:

1. Data Collection - Gather training examples
2. Feature Selection - Choose what the model learns from
3. Algorithm Training - The model adjusts internal parameters
4. Validation - Test accuracy on new data
5. Optimization - Fine-tune for better performance

Would you like me to explain any of these steps in more detail?
```

### Example 2: Problem Solving

```
You: I have a Python error about NoneType
L.U.M.E.N: NoneType errors usually mean a variable is None when you expected a value.

Can you share the error line? Common causes are:
- Function returning None instead of a value
- Variable not initialized before use
- Dict lookup without checking if key exists

What's the specific error you're getting?
```

### Example 3: Personal Preferences

```
You: I prefer clear, concise answers
L.U.M.E.N: Understood! I'll keep responses brief and focused.

You: What's machine learning?
L.U.M.E.N: ML is when computers learn from data without explicit programming.
```

### Example 4: Mood-Based Responses

```
You: I'm feeling stressed about deadlines
L.U.M.E.N: I understand the pressure. Let's focus on what you can control today. 
Breaking it into smaller pieces helps. What's your top priority right now?

You: Actually, I got everything done! 🎉
L.U.M.E.N: That's fantastic! You should be proud - you crushed those deadlines!
```

---

## Memory & Learning

### What L.U.M.E.N Remembers

**Automatically stored:**
- Your name and personal details
- Your preferences and communication style
- Topics you care about
- Important goals and deadlines
- Past conversations (consolidated)
- Your emotional patterns

**Example memory evolution:**

**Day 1:**
```
You: I'm studying computer science
L.U.M.E.N: [stores: user interested in CS]
```

**Day 5:**
```
You: Another AI question...
L.U.M.E.N: I've noticed you're really interested in AI. What specifically?
```

**Day 30:**
```
You: <any technical question>
L.U.M.E.N: [uses technical tone] [provides detailed explanations] [assumes CS knowledge]
```

### How to Control Memory

**Tell it to remember:**
```
You: Remember: I have a PhD in physics
L.U.M.E.N: Got it. I'll remember you have a PhD in physics.
```

**Check what it knows:**
```
You: What do you know about me?
L.U.M.E.N: [summarizes stored preferences and facts]
```

### Memory Persistence

- **Local Memory**: Stored in `memory_cache.json` on your computer
- **Cloud Memory**: Synced to Firebase (optional, for multi-device sync)
- **Persistence**: Survives across sessions automatically

---

## Advanced Features

### Force a Specific Model

When you need guaranteed response quality:

```
You: Use balanced mode - design a database schema for e-commerce
L.U.M.E.N: [uses balanced model]

You: Quick answer in fast mode - what's 2+2?
L.U.M.E.N: [uses fastest model] 4
```

**Model modes:**
- `fast mode` → phi3 (quick)
- `balanced mode` → mistral (default)

### File Security & Operations

Safe file management with security features:

```
You: Create a configuration file
L.U.M.E.N: [asks for confirmation]
Type YES to confirm deletion? YES confirmed

You: Scan system for security issues  
L.U.M.E.N: Scanning... [shows risk patterns found]
```

### Cloud Synchronization

Multi-device memory sync:

```
You: Remember my API keys for later
L.U.M.E.N: [stores locally and syncs to cloud every 30s]

[On your phone with cloud access...]
Phone: What are my API keys?
L.U.M.E.N: [retrieves from cloud]
```

### Model Learning

The system learns which models work best for your types of questions:

```
[First time you ask a complex question - uses balanced model]
[You type: That could have been better]
[Next time you ask similar complexity - uses balanced model]
```

---

## Tips & Tricks

### 1. Get Better Answers

Add context to questions:

```
❌ Poor: "How do I code?"
✅ Good: "I'm learning Python and want to understand loops"

❌ Poor: "What's this error?"
✅ Good: "I'm getting a TypeError in my Flask app when..."
```

### 2. Teach L.U.M.E.N Your Preferences

```
You: I prefer technical explanations with code examples
L.U.M.E.N: [learns this preference] Got it!

You: Explain decorators
L.U.M.E.N: [provides code examples from now on]
```

### 3. Use for Brainstorming

```
You: I want to build something with AI. Brainstorm ideas with me
L.U.M.E.N: Sure! Here are some ideas:
- Chatbot for customer service
- Image classification app
- Predictive analytics dashboard
- [continues with ideas...]

You: Tell me more about the second one
L.U.M.E.N: [dives deeper]
```

### 4. Get Consistent Tone

```
You: From now on, speak like a pirate
L.U.M.E.N: Aye, I'll adjust me speakin' style! 🏴‍☠️

You: What's an API?
L.U.M.E.N: Arr, 'tis a way fer programs to chat with each other...
```

### 5. Track Progress

```
You: I'm learning web development. Can you track my progress?
L.U.M.E.N: Absolutely! Tell me your milestones.

You: I completed JavaScript basics
L.U.M.E.N: [stores milestone] Great progress!

You: How far have I progressed?
L.U.M.E.N: You've completed: JavaScript basics. Next: React...
```

---

## Troubleshooting

### "I don't think you remembered that..."

**Solution:** The system only stores information explicitly marked important or mentioned in specific keywords.

```
You: Remember: I have 3 cats named Fluffy, Whiskers, and Mittens
L.U.M.E.N: Got it! I'll remember your 3 cats.
```

### "The responses seem off..."

**Possible causes:**
1. Ollama crashed - Restart: `ollama serve`
2. Internet timeout - Check connection
3. Model not installed - Run: `ollama pull mistral`

### "Memory keeps resetting..."

**Solution:** Check if `memory_cache.json` is writable:
```bash
# Check file permissions
ls -l memory_cache.json

# On Windows, make sure file isn't read-only
```

### "Response Quality is Low"

**Solutions:**
1. Use balanced mode for complex questions
2. Provide more context to your questions
3. Check if Ollama has enough RAM (8GB minimum recommended)

### "Cloud sync not working"

**Check:**
1. Internet connection is active
2. Firebase credentials are correct (in `memory.py`)
3. Cloud features are enabled

---

## Keyboard Shortcuts

| Command | Action |
|---------|--------|
| `exit` | Exit L.U.M.E.N |
| `quit` | Exit L.U.M.E.N |
| `Ctrl+C` | Emergency exit |

---

## Common Patterns

### Daily Standup

```
You: What did I work on yesterday?
L.U.M.E.N: Based on our conversation, you worked on [lists memories]

You: What should I focus on today?
L.U.M.E.N: Based on your goals...
```

### Learning Partner

```
You: I'm learning calculus
L.U.M.E.N: [remembers context] 

You: Explain limits
L.U.M.E.N: [provides educational explanation with examples]

You: Can you quiz me?
L.U.M.E.N: Sure! [generates questions]
```

### Problem Solver

```
You: I'm debugging a database issue
L.U.M.E.N: [remembers you're a developer]

You: The query is slow
L.U.M.E.N: Let's optimize it. Can you share the query?
```

---

## Performance Expectations

| Query Type | Response Time | Model Used |
|------------|---------------|-----------|
| Simple facts | 1-3 seconds | phi3 |
| Explanations | 3-8 seconds | mistral |

**Optimize for speed:**
- Use "fast mode" for quick answers
- Shorter questions are faster
- Local Ollama is faster than cloud LLMs

---

## Privacy & Security

**Your data:**
- Local memories stored in `memory_cache.json` (encrypted optional)
- Cloud synced to Firebase only if enabled
- File operations require confirmation for safety
- No data sent to external servers except Firebase
- Encryption key stored in `lumen.key`

---

## Getting Help

If something doesn't work:

1. **Check logs** - Look for error messages in terminal
2. **Restart** - Basic troubleshooting step
3. **Check configuration** - See `SETUP_AND_CONFIGURATION.md`
4. **Review memory** - Check `memory_cache.json` contents

---

## Next Steps

1. **Run L.U.M.E.N** - `python main.py`
2. **Introduce yourself** - Tell it about you
3. **Use it daily** - It learns from interaction
4. **Give feedback** - Help it improve responses
5. **Explore features** - Try different model modes

---

**Version:** 1.0.0  
**Last Updated:** April 13, 2026  
**Status:** Ready to Use
