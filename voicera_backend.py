import os
import json
import hashlib
from datetime import datetime

# ============================================================
# VOICERA BACKEND
# Shared logic for Desktop + Android + iOS
# ============================================================

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa"
}

TRANSLATED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa"
}


# ============================================================
# DATA DIRECTORY
# ============================================================

DATA_DIR = os.path.join(
    os.path.expanduser("~"),
    ".voicera"
)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
SESSION_FILE = os.path.join(DATA_DIR, "session.json")


# ============================================================
# DATA INITIALIZATION
# ============================================================

def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)


# ============================================================
# USERS
# ============================================================

def load_users():
    ensure_data_files()

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users):
    ensure_data_files()

    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(username, password):
    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    users = load_users()

    if username in users:
        return False, "Account already exists."

    users[username] = {
        "password": hash_password(password),
        "created_at": datetime.now().isoformat()
    }

    save_users(users)

    return True, "Account created successfully."


def login_user(username, password):
    username = username.strip()

    users = load_users()

    if username not in users:
        return False, "Account not found."

    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password."

    save_session_user(username)

    return True, "Login successful."


# ============================================================
# SESSION
# ============================================================

def load_session_user():
    ensure_data_files()

    if not os.path.exists(SESSION_FILE):
        return None

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("username")

    except Exception:
        return None


def save_session_user(username):
    ensure_data_files()

    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"username": username},
            f,
            indent=2
        )


def clear_session_user():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


# ============================================================
# HISTORY
# ============================================================

def load_history():
    ensure_data_files()

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


def save_history_data(history):
    ensure_data_files()

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            history,
            f,
            indent=2,
            ensure_ascii=False
        )


def add_history(
    username,
    feature,
    text,
    language="English"
):
    if not username or not text:
        return

    history = load_history()

    if username not in history:
        history[username] = []

    history[username].insert(
        0,
        {
            "feature": feature,
            "text": text,
            "language": language,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    )

    save_history_data(history)


def get_user_history(username):
    history = load_history()

    return history.get(username, [])


def clear_user_history(username):
    history = load_history()

    if username in history:
        history[username] = []

    save_history_data(history)


# ============================================================
# LANGUAGE HELPERS
# ============================================================

def get_language_code(language_name):
    return LANGUAGES.get(
        language_name,
        "en"
    )


def get_languages():
    return list(LANGUAGES.keys())


# ============================================================
# PASSWORD / ACCOUNT HELPERS
# ============================================================

def account_exists(username):
    return username.strip() in load_users()


# Initialize storage when backend loads
ensure_data_files()
