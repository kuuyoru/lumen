import os
import time

# ----------------------------
# THREAT PATTERNS (STATIC RULES)
# ----------------------------
SUSPICIOUS_PATTERNS = [
    "rm -rf",
    "del /f /s /q",
    "os.system",
    "subprocess",
    "exec(",
    "eval(",
    "base64.b64decode",
    "socket",
    "while True",
    "chmod 777",
    "pickle.load",
    "input(",
]


# ----------------------------
# MEMORY (BEHAVIOR TRACKING)
# ----------------------------
USER_BEHAVIOR_LOG = []


def log_behavior(action):
    USER_BEHAVIOR_LOG.append({
        "action": action,
        "time": time.time()
    })

    if len(USER_BEHAVIOR_LOG) > 300:
        USER_BEHAVIOR_LOG.pop(0)


def detect_anomaly(action):
    """
    Detect unusual behavior patterns
    """

    recent = USER_BEHAVIOR_LOG[-25:]
    same = sum(1 for x in recent if x["action"] == action)

    if len(recent) < 5:
        return {"anomaly": False}

    if same == 0:
        return {"anomaly": True, "reason": "new/unseen action type"}

    if same > 18:
        return {"anomaly": True, "reason": "repeated behavior spike"}

    return {"anomaly": False}


# ----------------------------
# FILE SCANNER (RISK ENGINE)
# ----------------------------
def analyze_file(file_path):
    try:
        if not os.path.exists(file_path):
            return {"status": "not_found"}

        with open(file_path, "r", errors="ignore") as f:
            content = f.read()

        risk = 0
        triggers = []

        for pattern in SUSPICIOUS_PATTERNS:
            if pattern in content:
                risk += 20
                triggers.append(pattern)

        # heuristics
        if len(content) > 150000:
            risk += 10
            triggers.append("large_file")

        if "import os" in content and "remove" in content:
            risk += 15
            triggers.append("file_system_access")

        return {
            "file": file_path,
            "risk_score": risk,
            "triggers": triggers,
            "status": "scanned"
        }

    except Exception as e:
        return {"error": str(e)}


# ----------------------------
# DIRECTORY SCANNER
# ----------------------------
def scan_directory(folder):
    results = []

    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)

            if file.endswith((".py", ".txt", ".json")):
                res = analyze_file(path)

                if res.get("risk_score", 0) > 25:
                    results.append(res)

    return results


# ----------------------------
# LIVE MONITORING
# ----------------------------
def monitor_folder(folder, interval=10):
    print(f"[SECURITY] Monitoring: {folder}")

    previous = {}

    while True:
        try:
            current = {}

            for root, _, files in os.walk(folder):
                for f in files:
                    path = os.path.join(root, f)
                    current[path] = os.path.getmtime(path)

            # detect new files
            for path in current:
                if path not in previous:
                    print(f"[NEW FILE] {path}")

            # detect deleted files
            for path in previous:
                if path not in current:
                    print(f"[DELETED] {path}")

            previous = current
            time.sleep(interval)

        except KeyboardInterrupt:
            print("[SECURITY] Monitoring stopped.")
            break

        except Exception as e:
            print(f"[ERROR] {e}")
            break


# ----------------------------
# GLOBAL SECURITY STATE
# ----------------------------
SECURITY_STATE = {
    "threats_detected": 0,
    "files_scanned": 0,
    "last_scan": None,
    "anomalies": 0
}


# ----------------------------
# SECURITY UPDATE ENGINE
# ----------------------------
def update_security_state(scan_results):
    if isinstance(scan_results, list):
        SECURITY_STATE["threats_detected"] += len(scan_results)
    else:
        SECURITY_STATE["threats_detected"] += 1

    SECURITY_STATE["last_scan"] = time.time()


# ----------------------------
# SECURITY ALERT SYSTEM
# ----------------------------
def security_alert(result):

    if not result:
        return

    if isinstance(result, dict) and result.get("risk_score", 0) >= 50:
        print(f"\n🚨 CRITICAL THREAT: {result.get('file')}")
        print(f"Triggers: {result.get('triggers')}\n")

    elif isinstance(result, dict) and result.get("risk_score", 0) >= 25:
        print(f"\n⚠️ WARNING: {result.get('file')}")


# ----------------------------
# ANOMALY REPORT
# ----------------------------
def get_anomaly_report():
    recent = USER_BEHAVIOR_LOG[-50:]

    actions = {}

    for a in recent:
        act = a["action"]
        actions[act] = actions.get(act, 0) + 1

    return {
        "total_actions": len(recent),
        "distribution": actions,
        "anomaly_score": len(set(actions.keys()))
    }