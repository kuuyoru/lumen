from voice import speak

def start_lumen():
    speak("Welcome back sir. LUMEN is now online.", wait=True)

    while True:
        command = input("You: ")

        if command.lower() in ["exit", "quit", "shutdown"]:
            speak("Goodbye sir. Until next time.", wait=True)
            break

        elif command.strip() == "":
            speak("I didn't catch that.")

        else:
            response = "You said " + command
            print(response)
            speak(response)

start_lumen()