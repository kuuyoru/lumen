import os
import platform
import subprocess

from cryptography.fernet import Fernet

from security import analyze_file, scan_directory, log_behavior, detect_anomaly


# ----------------------------
# SAFETY
# ----------------------------
ALLOWED_BASE_PATH = os.getcwd()

KEY_FILE = "lumen.key"
_key = None


# ----------------------------
# ENCRYPTION CORE
# ----------------------------
def load_key():
    global _key

    if _key:
        return _key

    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            _key = f.read()
    else:
        _key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(_key)

    return _key


def cipher():
    return Fernet(load_key())


# ----------------------------
# PERMISSION SYSTEM
# ----------------------------
def confirm(action, level="low"):

    print(f"[ACTION] {action}")

    if level == "low":
        return input("Confirm? (y/n): ") == "y"

    if level == "high":
        if input("Type YES: ") != "YES":
            return False
        return input("Confirm again: ") == "YES"

    return False


# ----------------------------
# SAFE PATH
# ----------------------------
def safe_path(path):
    full = os.path.abspath(path)

    if not full.startswith(ALLOWED_BASE_PATH):
        raise PermissionError("Blocked path access")

    return full


# ----------------------------
# SYSTEM TOOLS
# ----------------------------
def open_app(app):
    log_behavior("open_app")

    if detect_anomaly("open_app")["anomaly"]:
        print("⚠️ Anomaly detected")

    try:
        if platform.system() == "Windows":
            os.startfile(app)
        else:
            subprocess.run(["open", app])

        return f"Opened {app}"

    except Exception as e:
        return str(e)


def create_file(path, content):
    log_behavior("create_file")

    try:
        path = safe_path(path)

        if not confirm(f"create {path}"):
            return "cancelled"

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return "created"

    except Exception as e:
        return str(e)


def read_file(path):
    try:
        path = safe_path(path)

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    except Exception as e:
        return str(e)


def delete_file(path):
    log_behavior("delete_file")

    try:
        path = safe_path(path)

        if not confirm(f"DELETE {path}", "high"):
            return "cancelled"

        os.remove(path)

        return "deleted"

    except Exception as e:
        return str(e)


# ----------------------------
# FILE SYSTEM SECURITY
# ----------------------------
def scan_file(path):
    result = analyze_file(path)
    return result


def scan_system(folder="."):
    return scan_directory(folder)


# ----------------------------
# ENCRYPTION SYSTEM
# ----------------------------
def encrypt_file(path):
    try:
        path = safe_path(path)

        if not confirm(f"encrypt {path}", "high"):
            return "cancelled"

        c = cipher()

        with open(path, "rb") as f:
            data = f.read()

        enc = c.encrypt(data)

        out = path + ".lumen"

        with open(out, "wb") as f:
            f.write(enc)

        return f"encrypted -> {out}"

    except Exception as e:
        return str(e)


def decrypt_file(path):
    try:
        path = safe_path(path)

        if not path.endswith(".lumen"):
            return "invalid file"

        if not confirm(f"decrypt {path}", "high"):
            return "cancelled"

        c = cipher()

        with open(path, "rb") as f:
            data = f.read()

        dec = c.decrypt(data)

        out = path.replace(".lumen", "_decrypted")

        with open(out, "wb") as f:
            f.write(dec)

        return f"decrypted -> {out}"

    except Exception as e:
        return str(e)


# ----------------------------
# SYSTEM INFO
# ----------------------------
def system_info():
    return {
        "os": platform.system(),
        "cwd": os.getcwd()
    }