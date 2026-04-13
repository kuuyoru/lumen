import json

from lumen_core import process_user_input
from memory import add_fact, load_from_cache, save_to_cache
from tools import open_app, create_file, read_file, delete_file


# ----------------------------
# INITIALIZATION
# ----------------------------
def initialize_system():
    """Initialize memory and caches at startup"""
    try:
        load_from_cache()
        print("Memory system initialized.")
    except Exception as e:
        print(f"Warning: Memory init failed: {e}")


# ----------------------------
# TOOL EXECUTION (SAFE + LIGHTWEIGHT)
# ----------------------------
def execute(action):

    if not isinstance(action, dict):
        return None

    action_type = action.get("type")

    try:
        if action_type == "open_app":
            return open_app(action.get("target", ""))

        if action_type == "create_file":
            return create_file(
                action.get("path", "file.txt"),
                action.get("content", "")
            )

        if action_type == "read_file":
            return read_file(action.get("path", ""))

        if action_type == "delete_file":
            return delete_file(action.get("path", ""))

        if action_type == "chat":
            return action.get("content", "")

    except Exception as e:
        return f"Tool error: {str(e)}"

    return None


# ----------------------------
# MEMORY STORAGE (LIGHTWEIGHT)
# ----------------------------
def store_memory(user_input):
    """
    Only stores explicitly meaningful info.
    Core system handles everything else.
    """

    text = user_input.strip().lower()

    if not text:
        return

    keywords = [
        "remember", "important", "my name",
        "i am", "i want", "i like"
    ]

    if any(k in text for k in keywords) or len(text) > 80:
        add_fact(user_input, importance=2)


# ----------------------------
# OUTPUT HANDLER (RESPONSE SAFE)
# ----------------------------
def handle_output(raw_output):
    """Handle AI response output"""

    if raw_output is None or not isinstance(raw_output, str) or not raw_output.strip():
        return

    # Try to parse as tool action (JSON)
    try:
        action = json.loads(raw_output)
        if isinstance(action, dict) and "type" in action:
            # Ask for confirmation
            action_desc = describe_action(action)
            confirm = input(f"L.U.M.E.N: {action_desc} - Confirm? (y/n): ").strip().lower()
            if confirm == 'y':
                result = execute(action)
                if result:
                    print(f"L.U.M.E.N: {result}")
            else:
                print("L.U.M.E.N: Action cancelled.")
            return
    except (json.JSONDecodeError, ValueError):
        # Not JSON, treat as normal response
        pass

    print(f"L.U.M.E.N: {raw_output}")


def describe_action(action):
    """Describe the action for confirmation"""
    action_type = action.get("type")
    if action_type == "create_file":
        return f"Create file at {action.get('path', 'unknown')} with content '{action.get('content', '')[:50]}...'"
    elif action_type == "read_file":
        return f"Read file at {action.get('path', 'unknown')}"
    elif action_type == "delete_file":
        return f"Delete file at {action.get('path', 'unknown')}"
    elif action_type == "open_app":
        return f"Open app: {action.get('target', 'unknown')}"
    else:
        return f"Execute action: {action_type}"


def handle_output_stream(stream_output):
    """Progressively print response chunks as they arrive."""
    if stream_output is None:
        return

    print("L.U.M.E.N: ", end="", flush=True)
    try:
        for chunk in stream_output:
            print(chunk, end="", flush=True)
            # Small yield to allow UI responsiveness
            import time
            time.sleep(0.01)  # Minimal delay for smoother typing effect
    except Exception as e:
        print(f"\nL.U.M.E.N: Streaming error: {e}")
    finally:
        print()


# ----------------------------
# MAIN LOOP (OPTIMIZED)
# ----------------------------
def main():

    print("\nL.U.M.E.N ONLINE — CORE SYSTEM ACTIVE\n")
    print("Neural systems online. Awaiting input...\n")

    # Initialize memory on startup
    initialize_system()

    while True:

        try:
            user_input = input("You: ")
        except KeyboardInterrupt:
            print("\nL.U.M.E.N: Shutting down...")
            break
        except EOFError:
            break

        # exit
        if user_input.lower() in ["exit", "quit"]:
            print("L.U.M.E.N: Shutting down...")
            break

        if not user_input.strip():
            continue

        # Dev function: show last model
        if user_input.strip() == ".model":
            try:
                with open("last_model.txt", "r") as f:
                    model = f.read().strip()
                print(f"L.U.M.E.N: Last used model: {model}")
            except FileNotFoundError:
                print("L.U.M.E.N: No model used yet.")
            continue

        # Store memory
        store_memory(user_input)

        # Core processing (autonomous engine)
        try:
            raw_output = process_user_input(user_input, stream=True)
        except Exception as e:
            print(f"L.U.M.E.N: Processing error: {e}")
            continue

        # Output handling
        if hasattr(raw_output, "__iter__") and not isinstance(raw_output, str):
            handle_output_stream(raw_output)
        else:
            handle_output(raw_output)


if __name__ == "__main__":
    main()