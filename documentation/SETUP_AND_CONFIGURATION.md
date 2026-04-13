# L.U.M.E.N. AI - Setup & Configuration Guide

## Prerequisites

Before running L.U.M.E.N, ensure you have:

1. **Python 3.8+** installed
2. **Ollama** running locally (`http://localhost:11434`)
3. **Internet connection** (for some cloud features)
4. **Microphone** (for potential voice features in future)

## Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `ollama` - Local LLM inference
- `gtts` - Google Text-to-Speech
- `playsound` - Audio playback
- `faster-whisper` - Speech recognition
- `sounddevice` - Audio device access
- `scipy` - Signal processing
- `numpy` - Numerical operations
- `requests` - HTTP requests (Firebase)
- `speech_recognition` - Speech-to-text
- `edge_tts` - Microsoft Text-to-Speech
- `cryptography` - Encryption for security

### Step 2: Install and Run Ollama

Download Ollama from: https://ollama.ai

After installation, pull the required models:

```bash
ollama pull mistral
ollama pull phi3
```

Run Ollama in the background:
```bash
ollama serve
```

Verify it's running:
```bash
curl http://localhost:11434/api/tags
```

### Step 3: Configure Firebase (Optional)

L.U.M.E.N includes cloud sync for persistent memory across devices.

**Already configured with default Firebase project:**
- Project ID: `lumen-fe055`
- Database: Firebase Realtime Database

To customize, edit `memory.py`:
```python
FIREBASE_PROJECT_ID = "your-project-id"
FIREBASE_API_KEY = "your-api-key"
```

## Running L.U.M.E.N

### Start the AI Assistant

```bash
python main.py
```

You should see:
```
L.U.M.E.N ONLINE — CORE SYSTEM ACTIVE

Neural systems online. Awaiting input...

You: 
```

### Basic Usage

```
You: Hello L.U.M.E.N!
L.U.M.E.N: Hello! I'm here to help. What can I assist you with today?

You: What's your name?
L.U.M.E.N: I'm L.U.M.E.N, an intelligent adaptive assistant designed to learn and grow with you.

You: exit
L.U.M.E.N: Shutting down...
```

To exit at any time, type: `exit` or `quit`

## System Architecture

```
main.py (Entry Point)
  ↓
lumen_core.py (Core Processing)
  ├─ brain.py (Response Generation)
  │   └─ llm.py (Ollama LLM Interface)
  ├─ memory.py (Memory Management)
  │   └─ Firebase Cloud Sync
  └─ router.py (Model Selection)
      └─ learn_best_model() (Adaptive Routing)
  
tools.py (File Operations)
  └─ security.py (Security Scanning)

assistant.py (Alternative Interface)
  └─ ask_lumen() (Advanced Features)

memory_cache.json (Local Persistent Memory)
router_learning.json (Model Learning Data)
```

## File Structure

| File | Purpose |
|------|---------|
| `main.py` | Main application loop |
| `lumen_core.py` | Core autonomous processing |
| `brain.py` | LLM response generation |
| `llm.py` | Locoll interface (Ollama) |
| `memory.py` | Long-term memory system |
| `router.py` | Intelligent model selection |
| `tools.py` | System tools (file I/O, apps) |
| `security.py` | Security scanning & monitoring |
| `assistant.py` | Advanced interface |
| `cloud_sync_manager.py` | Cloud sync batching |
| `security_dashboard.py` | Security monitoring UI |
| `memory_cache.json` | Local cached memories |
| `router_learning.json` | Model selection history |
| `lumen.key` | Encryption key (auto-generated) |

## Configuration Options

### Model Selection

L.U.M.E.N automatically selects the best model based on query complexity.

**Available Models:**
- `phi3` (Fast, lightweight)
- `mistral` (Balanced, recommended)

**Force a specific model by adding to your prompt:**
- "Use fast mode" → Uses phi3
- "Use balanced mode" → Uses mistral

### Memory Configuration

Edit values in `memory.py`:

```python
LOCAL_CACHE_SIZE = 25  # Max facts to cache locally
FIREBASE_PROJECT_ID = "lumen-fe055"  # Your Firebase project
```

### Security Configuration

File operations require confirmation:
- Low level (read, open) - Single confirmation
- High level (delete) - Double confirmation with "YES"

## Troubleshooting

### "Error: Ollama not running on localhost:11434"

**Solution:** Ensure Ollama is running
```bash
ollama serve
```

### Memory not persisting

**Solution:** Check that `memory_cache.json` is writable in the working directory

### Cloud sync not working

**Solution:** Check internet connection and Firebase project configuration

### Slow responses

**Solution:** You're likely using `mistral`. Switch to faster mode:
```
You: Use fast mode for the next response
```

## Performance Tips

1. **Use Balanced Mode (Default)** - Good quality/speed tradeoff
2. **Enable Cloud Sync** - Distribute memory across devices
3. **Regular Memory Cleanup** - System does this automatically
4. **Monitor Memory Size** - Check `memory_cache.json` file size

## Advanced Features

### Autonomous Learning

L.U.M.E.N learns from every interaction:
- Tracks emotional tone
- Learns preferred communication style
- Consolidates important memories
- Adapts personality over time

### Memory System

**Local Memory:**
- Facts (user statements, insights)
- Preferences (user preferences)
- Emotions (tracked emotional states)
- Identity (who the user is)

**Cloud Memory:**
- Synced to Firebase every 30 seconds
- Accessible across devices
- Automatic deduplication
- Memory decay (weak memories fade)

### Security Features

- **File System Scanning** - Detects risky patterns
- **Behavior Monitoring** - Tracks anomalous actions
- **Encryption** - Uses Fernet symmetric encryption
- **Permission System** - Confirms file operations

## API Reference

### Core Functions

**main.py**
- `initialize_system()` - Initialize memory on startup
- `main()` - Main application loop

**lumen_core.py**
- `process_user_input(user_input)` - Main processing function

**brain.py**
- `think(user_input, model="mistral")` - Generate response

**memory.py**
- `add_fact(text, importance=1, tags=None)` - Store memory
- `get_memory_summary()` - Get memory summary
- `build_personality_profile()` - Build current personality profile
- `sync_to_cloud()` - Sync memory to Firebase
- `load_from_cloud()` - Load memory from Firebase

**router.py**
- `choose_model(user_input)` - Select best model for query
- `detect_user_override(text)` - Detect model preference in text

**tools.py**
- `open_app(app)` - Open system application
- `create_file(path, content)` - Create file safely
- `read_file(path)` - Read file safely
- `delete_file(path)` - Delete file safely

## Updates & Maintenance

The system is designed to be maintenance-free with automatic:
- Memory consolidation
- Memory decay for old facts
- Cloud synchronization
- Model learning and optimization

Manual maintenance (optional):
- Clear `memory_cache.json` to reset local memory
- Clear `router_learning.json` to reset model learning
- Delete `lumen.key` to reset encryption key

## Support & Documentation

- **Configuration**: See this file
- **Usage Manual**: See USER_MANUAL.md
- **Architecture**: See README.md
- **Firebase Setup**: See FIREBASE_SETUP.md

---

**Last Updated:** April 13, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
