import multiprocessing
multiprocessing.freeze_support()

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import sounddevice as sd
import wave
if getattr(sys, "frozen", False):
    WhisperModel = None
else:
    from faster_whisper import WhisperModel

import threading
import json
import os
import sys
import hashlib
from datetime import datetime
import asyncio
import edge_tts
import tempfile
import shutil


# ============================================================
# VOICERA
# Your Voice, Your Word.
# Speech-to-Text & Text-to-Speech Application
# ============================================================

APP_NAME = "VOICERA"
TAGLINE = "Your Voice, Your Word."
DESCRIPTION = "Speech-to-Text & Text-to-Speech Application"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Legacy bundled/project data
LEGACY_DATA_DIR = os.path.join(BASE_DIR, "voicera_data")
LEGACY_USERS_FILE = os.path.join(LEGACY_DATA_DIR, "users.json")
LEGACY_HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# Permanent user data on Mac
if sys.platform == "darwin":
    DATA_DIR = os.path.expanduser(
        "~/Library/Application Support/VOICERA"
    )
else:
    DATA_DIR = os.path.join(BASE_DIR, "voicera_data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")


import subprocess
import threading
import json
import os
import sys
import hashlib
from datetime import datetime


# ============================================================
# VOICERA
# Your Voice, Your Word.
# Speech-to-Text & Text-to-Speech Application
# ============================================================


APP_NAME = "VOICERA"
TAGLINE = "Your Voice, Your Word."
DESCRIPTION = "Speech-to-Text & Text-to-Speech Application"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Legacy bundled/project data
LEGACY_DATA_DIR = os.path.join(BASE_DIR, "voicera_data")
LEGACY_USERS_FILE = os.path.join(LEGACY_DATA_DIR, "users.json")
LEGACY_HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# Permanent user data on Mac
if sys.platform == "darwin":
    DATA_DIR = os.path.expanduser(
        "~/Library/Application Support/VOICERA"
    )
else:
    DATA_DIR = os.path.join(BASE_DIR, "voicera_data")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")


# ============================================================
# PERMANENT VOICERA DATA
# ============================================================

LEGACY_DATA_DIR = os.path.join(
    BASE_DIR,
    "voicera_data"
)

LEGACY_USERS_FILE = os.path.join(
    LEGACY_DATA_DIR,
    "users.json"
)

LEGACY_HISTORY_FILE = os.path.join(
    BASE_DIR,
    "history.json"
)

if sys.platform == "darwin":
    DATA_DIR = os.path.expanduser(
        "~/Library/Application Support/VOICERA"
    )
else:
    DATA_DIR = LEGACY_DATA_DIR

USERS_FILE = os.path.join(
    DATA_DIR,
    "users.json"
)

HISTORY_FILE = os.path.join(
    DATA_DIR,
    "history.json"
)

SESSION_FILE = os.path.join(
    DATA_DIR,
    "session.json"
)


# ============================================================
# LANGUAGES
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


# ============================================================
# DATA FUNCTIONS
# ============================================================

def ensure_data_files():

    os.makedirs(DATA_DIR, exist_ok=True)

    # Migrate existing account data once
    if not os.path.exists(USERS_FILE):

        if os.path.exists(LEGACY_USERS_FILE):

            try:
                shutil.copy2(
                    LEGACY_USERS_FILE,
                    USERS_FILE
                )
            except Exception:
                with open(
                    USERS_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        {},
                        file,
                        indent=4
                    )

        else:

            with open(
                USERS_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {},
                    file,
                    indent=4
                )

    # Migrate existing history once
    if not os.path.exists(HISTORY_FILE):

        if os.path.exists(LEGACY_HISTORY_FILE):

            try:
                shutil.copy2(
                    LEGACY_HISTORY_FILE,
                    HISTORY_FILE
                )
            except Exception:
                with open(
                    HISTORY_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        [],
                        file,
                        indent=4
                    )

        else:

            with open(
                HISTORY_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    [],
                    file,
                    indent=4
                )


def load_users():

    ensure_data_files()

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return {}


def save_users(users):

    ensure_data_files()

    with open(
        USERS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4
        )


def load_history():

    ensure_data_files()

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_history_data(history):

    ensure_data_files()

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_session_user():

    try:

        if not os.path.exists(SESSION_FILE):
            return None

        with open(
            SESSION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        username = data.get("username")

        return username if username else None

    except Exception:

        return None


def save_session_user(username):

    ensure_data_files()

    with open(
        SESSION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {"username": username},
            file,
            indent=4
        )


def clear_session_user():

    try:

        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    except Exception:

        pass


def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# MAIN APPLICATION
# ============================================================

class VoiceraApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "VOICERA — Your Voice, Your Word."
        )

        self.root.geometry(
            "1200x760"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.configure(
            bg="#F6F3FB"
        )

        self.current_user = None
        self.current_name = None

        self.process = None
        self.recording = False

        self.session_text = ""
        self.record_start_time = None

        self.tts_text = None
        self.transcript_text = None

        self.setup_styles()

        ensure_data_files()

        self.show_splash()

        self.play_startup_sound()


    # ========================================================
    # MAGICAL STARTUP SPLASH
    # ========================================================

    def show_splash(self):

        self.clear_root()

        self.splash = tk.Frame(
            self.root,
            bg="#F6F3FB"
        )

        self.splash.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # MAGIC CANVAS
        # ----------------------------------------------------

        canvas = tk.Canvas(
            self.splash,
            bg="#F6F3FB",
            highlightthickness=0,
            bd=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        self.splash_canvas = canvas

        # ----------------------------------------------------
        # SPARKLES
        # ----------------------------------------------------

        sparkle_positions = [
            (150, 150),
            (1030, 140),
            (210, 520),
            (980, 500),
            (330, 220),
            (880, 230),
            (450, 560),
            (760, 540),
            (570, 120),
            (650, 620)
        ]

        self.splash_sparkles = []

        for x, y in sparkle_positions:

            item = canvas.create_text(
                x,
                y,
                text="✦",
                font=("Helvetica", 12),
                fill="#C8BCEB",
                state="hidden"
            )

            self.splash_sparkles.append(item)

        # ----------------------------------------------------
        # START COMPLETELY BLANK
        # ----------------------------------------------------

        # ----------------------------------------------------
        # MAGICAL VOICERA BRANDING
        # ----------------------------------------------------

        self.splash_logo = canvas.create_text(
            600,
            330,
            text="VOICERA",
            font=("Helvetica", 52, "bold"),
            fill="#6656A3",
            state="hidden"
        )

        self.splash_description = canvas.create_text(
            600,
            405,
            text="Speech-to-Text & Text-to-Speech Application",
            font=("Helvetica", 15),
            fill="#777180",
            state="hidden"
        )

        self.splash_tagline = canvas.create_text(
            600,
            455,
            text="Your Voice, Your Word.",
            font=("Helvetica", 15, "italic"),
            fill="#8B78B8",
            state="hidden"
        )

        # ----------------------------------------------------
        # CONTINUE BUTTON
        # ----------------------------------------------------

        self.splash_continue = self.rounded_button(
            self.splash,
            "CONTINUE",
            self.show_intro,
            width=300,
            height=50,
            bg="#5B4B91",
            hover="#463878",
            fg="white",
            font=("Helvetica", 11, "bold")
        )

        self.splash_continue.place(
            relx=0.5,
            rely=0.72,
            anchor="center"
        )

        self.splash_continue.place_forget()

        # Start sound and visual animation together
        self.start_magical_animation()


    # ========================================================
    # MAGICAL SPLASH ANIMATION
    # ========================================================

    def start_magical_animation(self):

        canvas = self.splash_canvas

        canvas.itemconfigure(
            self.splash_logo,
            state="normal"
        )

        canvas.itemconfigure(
            self.splash_logo,
            font=("Helvetica", 42, "bold")
        )

        self.animate_logo(0)


    def animate_logo(self, step):

        canvas = self.splash_canvas
        total = 25

        if step <= total:

            progress = step / total
            eased = 1 - (1 - progress) ** 3
            size = int(42 + (52 - 42) * eased)

            canvas.itemconfigure(
                self.splash_logo,
                font=("Helvetica", size, "bold")
            )

            self.root.after(
                25,
                lambda: self.animate_logo(step + 1)
            )

            return

        canvas.itemconfigure(
            self.splash_description,
            state="normal"
        )

        self.root.after(
            350,
            self.show_splash_tagline
        )


    def show_splash_tagline(self):

        canvas = self.splash_canvas

        canvas.itemconfigure(
            self.splash_tagline,
            state="normal"
        )

        self.show_splash_sparkles(0)

        self.root.after(
            800,
            self.show_splash_continue
        )


    # ========================================================
    # SUBTLE SPARKLES
    # ========================================================

    def show_splash_sparkles(self, index):

        if index >= len(self.splash_sparkles):
            return

        item = self.splash_sparkles[index]

        self.splash_canvas.itemconfigure(
            item,
            state="normal"
        )

        self.root.after(
            120,
            lambda: self.show_splash_sparkles(index + 1)
        )


    # ========================================================
    # CONTINUE
    # ========================================================

    def show_splash_continue(self):

        self.splash_continue.place(
            relx=0.5,
            rely=0.72,
            anchor="center"
        )

    # ========================================================
    # APPLICATION INTRO
    # ========================================================

    def show_intro(self):

        self.clear_root()

        intro = tk.Frame(
            self.root,
            bg="#F6F3FB"
        )

        intro.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            intro,
            bg="white",
            width=650,
            height=390
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text="Welcome to VOICERA",
            font=("Helvetica", 30, "bold"),
            fg="#5B4B91",
            bg="white"
        ).pack(
            pady=(55, 12)
        )

        tk.Label(
            card,
            text="Your intelligent voice companion",
            font=("Helvetica", 15, "bold"),
            fg="#29243A",
            bg="white"
        ).pack(
            pady=5
        )

        tk.Label(
            card,
            text=(
                "Convert your voice into text and transform "
                "written text into natural speech."
            ),
            font=("Helvetica", 12),
            fg="#777180",
            bg="white",
            justify="center"
        ).pack(
            pady=(14, 8)
        )

        tk.Label(
            card,
            text=(
                "Supports multilingual communication with "
                "a simple, modern and professional experience."
            ),
            font=("Helvetica", 11),
            fg="#8A8492",
            bg="white",
            justify="center"
        ).pack(
            pady=4
        )

        tk.Label(
            card,
            text="Getting everything ready...",
            font=("Helvetica", 10, "italic"),
            fg="#8B78B8",
            bg="white"
        ).pack(
            pady=(25, 0)
        )

        self.root.after(
            2200,
            self.finish_intro
        )


    def finish_intro(self):

        saved_username = load_session_user()

        if saved_username:

            users = load_users()

            saved_user = users.get(
                saved_username
            )

            if saved_user:

                self.current_user = saved_username

                self.current_name = saved_user.get(
                    "name",
                    saved_username
                )

                self.show_dashboard()

                return

            clear_session_user()

        self.show_login()



    # ========================================================
    # VOICERA STARTUP SOUND
    # ========================================================

    def play_startup_sound(self):

        try:
            sound_file = "/System/Library/Sounds/Glass.aiff"

            if os.path.exists(sound_file):
                subprocess.Popen(
                    ["afplay", sound_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

        except Exception:
            pass

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "TCombobox",
            padding=8,
            font=("Helvetica", 10)
        )

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Helvetica", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Helvetica", 10, "bold")
        )


    # ========================================================
    # CLEAR MAIN AREA
    # ========================================================

    def clear_root(self):

        for widget in self.root.winfo_children():

            widget.destroy()


    def clear_main(self):

        if hasattr(self, "main_area"):

            for widget in self.main_area.winfo_children():

                widget.destroy()


    # ========================================================
    # PREMIUM ROUNDED BUTTON
    # ========================================================

    def rounded_button(self, parent, text, command,
                       width=320, height=48,
                       bg="#6656A3", hover="#55468F",
                       fg="white", font=("Helvetica", 11, "bold")):

        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0
        )

        radius = height // 2

        def draw(color):
            canvas.delete("all")

            canvas.create_arc(
                0, 0, radius * 2, height,
                start=90, extent=180,
                fill=color, outline=color
            )

            canvas.create_arc(
                width - radius * 2, 0, width, height,
                start=270, extent=180,
                fill=color, outline=color
            )

            canvas.create_rectangle(
                radius, 0,
                width - radius, height,
                fill=color, outline=color
            )

            canvas.create_text(
                width // 2,
                height // 2,
                text=text,
                fill=fg,
                font=font
            )

        draw(bg)

        canvas.bind(
            "<Enter>",
            lambda e: draw(hover)
        )

        canvas.bind(
            "<Leave>",
            lambda e: draw(bg)
        )

        canvas.bind(
            "<Button-1>",
            lambda e: command()
        )

        return canvas


    # ========================================================
    # LOGIN PAGE
    # ========================================================

    def show_login(self):

        self.clear_root()

        container = tk.Frame(
            self.root,
            bg="#F6F3FB"
        )

        container.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            container,
            bg="white",
            width=470,
            height=580
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text="VOICERA",
            font=("Helvetica", 32, "bold"),
            fg="#7667A8",
            bg="white"
        ).pack(
            pady=(55, 5)
        )

        tk.Label(
            card,
            text=TAGLINE,
            font=("Helvetica", 12),
            fg="#777180",
            bg="white"
        ).pack(
            pady=(0, 35)
        )

        tk.Label(
            card,
            text="Username or Email",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="white"
        ).pack(
            anchor="w",
            padx=55
        )

        self.login_user = tk.Entry(
            card,
            font=("Helvetica", 12),
            relief="flat",
            bg="#F4F1F8",
            fg="#29243A"
        )

        self.login_user.pack(
            fill="x",
            padx=55,
            ipady=10,
            pady=(8, 18)
        )

        tk.Label(
            card,
            text="Password",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="white"
        ).pack(
            anchor="w",
            padx=55
        )

        self.login_password = tk.Entry(
            card,
            font=("Helvetica", 12),
            relief="flat",
            bg="#F4F1F8",
            fg="#29243A",
            show="•"
        )

        self.login_password.pack(
            fill="x",
            padx=55,
            ipady=10,
            pady=(8, 25)
        )

        login_btn = self.rounded_button(
            card,
            "LOGIN",
            self.login,
            width=360,
            height=52,
            bg="#5B4B91",
            hover="#463878",
            fg="white",
            font=("Helvetica", 11, "bold")
        )

        login_btn.pack(
            padx=55,
            pady=(0, 2)
        )

        tk.Button(
            card,
            text="Create New Account",
            command=self.show_register,
            font=("Helvetica", 10, "bold"),
            fg="#7667A8",
            bg="white",
            activebackground="white",
            relief="flat",
            cursor="hand2"
        ).pack(
            pady=20
        )

        self.login_password.bind(
            "<Return>",
            lambda event: self.login()
        )


    # ========================================================
    # REGISTER PAGE
    # ========================================================

    def show_register(self):

        self.clear_root()

        container = tk.Frame(
            self.root,
            bg="#F6F3FB"
        )

        container.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            container,
            bg="white",
            width=500,
            height=650
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text="Create Account",
            font=("Helvetica", 25, "bold"),
            fg="#29243A",
            bg="white"
        ).pack(
            pady=(35, 5)
        )

        tk.Label(
            card,
            text="Join VOICERA",
            font=("Helvetica", 11),
            fg="#777180",
            bg="white"
        ).pack(
            pady=(0, 20)
        )

        # NAME

        tk.Label(
            card,
            text="Name",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="white"
        ).pack(
            anchor="w",
            padx=55
        )

        self.reg_name = tk.Entry(
            card,
            font=("Helvetica", 11),
            relief="flat",
            bg="#F4F1F8"
        )

        self.reg_name.pack(
            fill="x",
            padx=55,
            ipady=8,
            pady=(5, 12)
        )

        # USERNAME

        tk.Label(
            card,
            text="Username",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="white"
        ).pack(
            anchor="w",
            padx=55
        )

        self.reg_username = tk.Entry(
            card,
            font=("Helvetica", 11),
            relief="flat",
            bg="#F4F1F8"
        )

        self.reg_username.pack(
            fill="x",
            padx=55,
            ipady=8,
            pady=(5, 12)
        )

        # EMAIL

        tk.Label(
            card,
            text="Email",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="white"
        ).pack(
            anchor="w",
            padx=55
        )

        self.reg_email = tk.Entry(
            card,
            font=("Helvetica", 11),
            relief="flat",
            bg="#F4F1F8"
        )

        self.reg_email.pack(
            fill="x",
            padx=55,
            ipady=8,
            pady=(5, 12)
        )

        # PASSWORD

        tk.Label(
            card,
            text="Password",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="white"
        ).pack(
            anchor="w",
            padx=55
        )

        self.reg_password = tk.Entry(
            card,
            font=("Helvetica", 11),
            relief="flat",
            bg="#F4F1F8",
            show="•"
        )

        self.reg_password.pack(
            fill="x",
            padx=55,
            ipady=8,
            pady=(5, 20)
        )

        tk.Button(
            card,
            text="CREATE ACCOUNT",
            command=self.register,
            font=("Helvetica", 11, "bold"),
            fg="white",
            bg="#7667A8",
            activebackground="#62558F",
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=55,
            ipady=10
        )

        tk.Button(
            card,
            text="Back to Login",
            command=self.show_login,
            font=("Helvetica", 10, "bold"),
            fg="#7667A8",
            bg="white",
            relief="flat",
            cursor="hand2"
        ).pack(
            pady=15
        )


    # ========================================================
    # REGISTER
    # ========================================================

    def register(self):

        name = self.reg_name.get().strip()
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get()

        if not name or not username or not email or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )

            return

        users = load_users()

        if username in users:

            messagebox.showerror(
                "Registration Error",
                "Username already exists."
            )

            return

        for data in users.values():

            if data.get("email", "").lower() == email.lower():

                messagebox.showerror(
                    "Registration Error",
                    "Email already exists."
                )

                return

        users[username] = {
            "name": name,
            "email": email,
            "password": hash_password(password)
        }

        save_users(users)

        messagebox.showinfo(
            "Success",
            "Account created successfully."
        )

        self.show_login()


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self):

        login_value = self.login_user.get().strip()
        password = self.login_password.get()

        if not login_value or not password:

            messagebox.showwarning(
                "Login",
                "Please enter username/email and password."
            )

            return

        users = load_users()

        found_username = None
        found_user = None

        for username, data in users.items():

            if (
                username.lower() == login_value.lower()
                or
                data.get("email", "").lower() == login_value.lower()
            ):

                found_username = username
                found_user = data
                break

        if found_user is None:

            messagebox.showerror(
                "Login Failed",
                "Account not found."
            )

            return

        if found_user.get("password") != hash_password(password):

            messagebox.showerror(
                "Login Failed",
                "Incorrect password."
            )

            return

        self.current_user = found_username
        self.current_name = found_user.get(
            "name",
            found_username
        )

        save_session_user(
            found_username
        )

        self.show_dashboard()


    # ========================================================
    # DASHBOARD
    # ========================================================

    def show_dashboard(self):

        self.clear_root()

        # SIDEBAR

        self.sidebar = tk.Frame(
            self.root,
            bg="#29243A",
            width=240
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="VOICERA",
            font=("Helvetica", 25, "bold"),
            fg="white",
            bg="#29243A"
        ).pack(
            pady=(35, 3)
        )

        tk.Label(
            self.sidebar,
            text=TAGLINE,
            font=("Helvetica", 9),
            fg="#CFC8DE",
            bg="#29243A"
        ).pack(
            pady=(0, 40)
        )

        self.create_sidebar_button(
            "⌂  Dashboard",
            self.show_dashboard_home
        )

        self.create_sidebar_button(
            "🎤  Speech → Text",
            self.show_speech_page
        )

        self.create_sidebar_button(
            "🔊  Text → Speech",
            self.show_tts_page
        )

        self.create_sidebar_button(
            "📜  History",
            self.show_history_page
        )

        self.create_sidebar_button(
            "ℹ  About",
            self.show_about
        )

        tk.Frame(
            self.sidebar,
            bg="#29243A"
        ).pack(
            fill="both",
            expand=True
        )

        logout_button = self.rounded_button(
            self.sidebar,
            "↪  Logout",
            self.logout,
            width=190,
            height=42,
            bg="#29243A",
            hover="#3A344D",
            fg="white",
            font=("Helvetica", 10, "bold")
        )

        logout_button.pack(
            fill="x",
            padx=20,
            pady=(0, 25)
        )

        # MAIN AREA

        self.main_area = tk.Frame(
            self.root,
            bg="#F6F3FB"
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.show_dashboard_home()


    # ========================================================
    # SIDEBAR BUTTON
    # ========================================================

    def create_sidebar_button(
        self,
        text,
        command
    ):

        btn = self.rounded_button(
            self.sidebar,
            text,
            command,
            width=245,
            height=48,
            bg="#7667A8",
            hover="#62558F",
            fg="white",
            font=("Helvetica", 11, "bold")
        )

        btn.pack(
            fill="x",
            padx=12,
            pady=5
        )

    # ========================================================
    # DASHBOARD HOME
    # ========================================================

    def show_dashboard_home(self):

        self.clear_main()

        tk.Label(
            self.main_area,
            text=f"Welcome back, {self.current_name}",
            font=("Helvetica", 27, "bold"),
            fg="#29243A",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35,
            pady=(35, 5)
        )

        tk.Label(
            self.main_area,
            text="What would you like to do today?",
            font=("Helvetica", 11),
            fg="#777180",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35
        )

        cards = tk.Frame(
            self.main_area,
            bg="#F6F3FB"
        )

        cards.pack(
            fill="x",
            padx=35,
            pady=40
        )

        self.create_dashboard_card(
            cards,
            "🎤",
            "Speech → Text",
            "Convert your voice into text.",
            self.show_speech_page
        )

        self.create_dashboard_card(
            cards,
            "🔊",
            "Text → Speech",
            "Convert written text into voice.",
            self.show_tts_page
        )

        self.create_dashboard_card(
            cards,
            "📜",
            "History",
            "View your previous conversions.",
            self.show_history_page
        )

        # INFO

        info = tk.Frame(
            self.main_area,
            bg="white"
        )

        info.pack(
            fill="x",
            padx=35,
            pady=10
        )

        tk.Label(
            info,
            text="VOICERA",
            font=("Helvetica", 18, "bold"),
            fg="#7667A8",
            bg="white"
        ).pack(
            anchor="w",
            padx=25,
            pady=(22, 5)
        )

        tk.Label(
            info,
            text=DESCRIPTION,
            font=("Helvetica", 11),
            fg="#777180",
            bg="white"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 22)
        )


    # ========================================================
    # DASHBOARD CARD
    # ========================================================

    def create_dashboard_card(
        self,
        parent,
        icon,
        title,
        description,
        command
    ):

        card = tk.Frame(
            parent,
            bg="white",
            width=260,
            height=180
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            font=("Helvetica", 30),
            bg="white",
            fg="#7667A8"
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            card,
            text=title,
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#29243A"
        ).pack()

        tk.Label(
            card,
            text=description,
            font=("Helvetica", 9),
            bg="white",
            fg="#777180"
        ).pack(
            pady=5
        )

        tk.Button(
            card,
            text="Open",
            command=command,
            font=("Helvetica", 9, "bold"),
            fg="#7667A8",
            bg="#F1EDF7",
            activebackground="#E4DDEF",
            relief="flat",
            cursor="hand2"
        ).pack(
            pady=8,
            ipadx=15,
            ipady=4
        )


    # ========================================================
    # SPEECH TO TEXT PAGE
    # ========================================================

    def show_speech_page(self):

        self.clear_main()

        tk.Label(
            self.main_area,
            text="Speech → Text",
            font=("Helvetica", 26, "bold"),
            fg="#29243A",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            self.main_area,
            text="Speak naturally and VOICERA will convert your voice into text.",
            font=("Helvetica", 11),
            fg="#777180",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35
        )

        # CONTROLS

        controls = tk.Frame(
            self.main_area,
            bg="#F6F3FB"
        )

        controls.pack(
            fill="x",
            padx=35,
            pady=20
        )

        tk.Label(
            controls,
            text="Language",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="#F6F3FB"
        ).pack(
            side="left"
        )

        self.stt_language = ttk.Combobox(
            controls,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=18
        )

        self.stt_language.set("English")

        self.stt_language.pack(
            side="left",
            padx=10
        )

        tk.Label(
            controls,
            text="Mode",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="#F6F3FB"
        ).pack(
            side="left",
            padx=(15, 0)
        )

        self.stt_mode = ttk.Combobox(
            controls,
            values=[
                "Actual Language",
                "Translated Language"
            ],
            state="readonly",
            width=20
        )

        self.stt_mode.set(
            "Actual Language"
        )

        self.stt_mode.pack(
            side="left",
            padx=10
        )

        self.record_button = tk.Button(
            controls,
            text="🎤  START RECORDING",
            command=self.start_recording,
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#7667A8",
            activebackground="#62558F",
            relief="flat",
            cursor="hand2"
        )

        self.record_button.pack(
            side="left",
            padx=10,
            ipady=7,
            ipadx=8
        )

        self.stop_button = tk.Button(
            controls,
            text="⏹  STOP",
            command=self.stop_recording,
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#B85C72",
            activebackground="#9F4B60",
            relief="flat",
            cursor="hand2",
            state="disabled"
        )

        self.stop_button.pack(
            side="left",
            padx=5,
            ipady=7,
            ipadx=12
        )

        # STATUS

        self.status_label = tk.Label(
            self.main_area,
            text="Ready to listen",
            font=("Helvetica", 10),
            fg="#7667A8",
            bg="#F6F3FB"
        )

        self.status_label.pack(
            anchor="w",
            padx=35
        )

        # TRANSCRIPT BOX

        transcript_container = tk.Frame(
            self.main_area,
            bg="white",
            highlightbackground="#E2DDED",
            highlightthickness=1
        )

        transcript_container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=15
        )

        tk.Label(
            transcript_container,
            text="Transcript",
            font=("Helvetica", 12, "bold"),
            fg="#29243A",
            bg="white"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8)
        )

        self.transcript_text = tk.Text(
            transcript_container,
            font=("Helvetica", 14),
            bg="white",
            fg="#29243A",
            insertbackground="#7667A8",
            relief="flat",
            wrap="word",
            padx=20,
            pady=10
        )

        self.transcript_text.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # BOTTOM BUTTONS

        bottom = tk.Frame(
            self.main_area,
            bg="#F6F3FB"
        )

        bottom.pack(
            fill="x",
            padx=35,
            pady=(0, 20)
        )

        tk.Button(
            bottom,
            text="Clear",
            command=self.clear_transcript,
            font=("Helvetica", 10, "bold"),
            fg="#625A70",
            bg="#E8E3F1",
            activebackground="#DCD5E8",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=5,
            ipady=6,
            ipadx=10
        )

        tk.Button(
            bottom,
            text="Copy",
            command=self.copy_transcript,
            font=("Helvetica", 10, "bold"),
            fg="#625A70",
            bg="#E8E3F1",
            activebackground="#DCD5E8",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=5,
            ipady=6,
            ipadx=10
        )

        tk.Button(
            bottom,
            text="Save",
            command=self.save_transcript,
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#7667A8",
            activebackground="#62558F",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=5,
            ipady=6,
            ipadx=10
        )


    # ========================================================
    # START RECORDING
    # ========================================================

    def start_recording(self):

        if self.recording:
            return

        language = self.stt_language.get()

        language_code = LANGUAGES.get(
            language,
            "en"
        )

        self.recording = True
        self.stop_requested = False
        self.session_text = ""
        self.record_start_time = datetime.now()

        self.record_button.config(
            state="disabled"
        )

        self.stop_button.config(
            state="normal"
        )

        self.status_label.config(
            text="🎤 Listening... Speak now"
        )

        # ====================================================
        # FROZEN MAC APP
        # Use the same working venv312 Whisper backend.
        # No console window is opened.
        # ====================================================

        if getattr(
            sys,
            "frozen",
            False
        ):

            project_dir = os.path.expanduser(
                "~/Documents/realtime-speech-to-text"
            )

            python_exec = os.path.join(
                project_dir,
                "venv312",
                "bin",
                "python"
            )

            backend_script = os.path.join(
                project_dir,
                "voicera_external_stt.py"
            )

            if not os.path.exists(
                python_exec
            ) or not os.path.exists(
                backend_script
            ):

                self.recording = False

                self.record_button.config(
                    state="normal"
                )

                self.stop_button.config(
                    state="disabled"
                )

                messagebox.showerror(
                    "VOICERA",
                    "Speech engine could not be found."
                )

                return

            try:

                if self.stt_mode.get() == "Translated Language":

                    command = [
                        python_exec,
                        "-u",
                        backend_script,
                        "--auto-detect"
                    ]

                else:

                    command = [
                        python_exec,
                        "-u",
                        backend_script,
                        "--language",
                        language_code
                    ]

                self.process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    cwd=project_dir
                )

                threading.Thread(
                    target=self.read_speech_output,
                    daemon=True
                ).start()

            except Exception as error:

                self.recording = False

                self.record_button.config(
                    state="normal"
                )

                self.stop_button.config(
                    state="disabled"
                )

                messagebox.showerror(
                    "Speech Recognition Error",
                    str(error)
                )

            return

        # ====================================================
        # SOURCE VERSION
        # Current working direct Whisper path.
        # ====================================================

        threading.Thread(
            target=self.direct_stt_worker,
            args=(language_code,),
            daemon=True
        ).start()


    # ========================================================
    # DIRECT WHISPER STT
    # ========================================================

    def direct_stt_worker(self, language_code):

        wav_path = None
        error_message = None

        try:

            # Load Whisper only when STT is actually used
            if getattr(
                self,
                "whisper_model",
                None
            ) is None:

                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text="Loading speech engine..."
                    )
                )

                self.whisper_model = WhisperModel(
                    "small",
                    device="cpu",
                    compute_type="int8"
                )

            if self.stop_requested:

                return

            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="🎤 Listening... Speak now"
                )
            )

            RATE = 16000
            DURATION = 8

            # Use macOS default input microphone.
            # Do not hard-code device index because packaged apps
            # can see audio devices in a different order.
            audio = sd.rec(
                int(DURATION * RATE),
                samplerate=RATE,
                channels=1,
                dtype="int16",
                device=0
            )

            sd.wait()

            wav_path = os.path.join(
                DATA_DIR,
                "speech_input.wav"
            )

            with wave.open(
                wav_path,
                "wb"
            ) as wf:

                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(RATE)
                wf.writeframes(
                    audio.tobytes()
                )

            self.root.after(
                0,
                lambda: self.status_label.config(
                    text="Processing speech..."
                )
            )

            # Actual Language mode:
            # force Whisper to use the selected language.
            # Translated Language mode:
            # allow Whisper to auto-detect the spoken language.
            current_mode = self.stt_mode.get()

            source_language = None

            if current_mode == "Actual Language":
                source_language = language_code

            segments, info = self.whisper_model.transcribe(
                wav_path,
                beam_size=5,
                vad_filter=False,
                language=source_language
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
                if segment.text.strip()
            ).strip()

            if text:

                self.detected_stt_language = info.language

                mode = self.stt_mode.get()
                selected_language = self.stt_language.get()

                if mode == "Translated Language":

                    threading.Thread(
                        target=self.translate_stt_text,
                        args=(
                            text,
                            selected_language,
                            info.language
                        ),
                        daemon=True
                    ).start()

                else:

                    self.root.after(
                        0,
                        self.add_transcript,
                        text
                    )

            else:

                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text="No speech detected"
                    )
                )

        except Exception as error:

            error_message = str(error)

        finally:

            if wav_path and os.path.exists(wav_path):

                try:
                    os.remove(wav_path)
                except Exception:
                    pass

            if error_message:

                self.root.after(
                    0,
                    self._handle_stt_error,
                    error_message
                )

            else:

                self.root.after(
                    0,
                    self.finish_recording
                )


    def _handle_stt_error(self, error):

        self.finish_recording()

        messagebox.showerror(
            "Speech Recognition Error",
            error
        )


    def read_speech_output(self):

            if not self.process:

                return

            try:

                for line in iter(
                    self.process.stdout.readline,
                    ""
                ):

                    if not line:

                        break

                    line = line.strip()

                    if line.startswith("LANGUAGE:"):

                        self.detected_stt_language = line.split(
                            "LANGUAGE:",
                            1
                        )[1].strip()

                    elif line.startswith(">>>"):

                        text = line[3:].strip()

                        if text:

                            mode = self.stt_mode.get()
                            selected_language = self.stt_language.get()

                            if mode == "Translated Language":

                                detected_language = getattr(
                                    self,
                                    "detected_stt_language",
                                    "en"
                                )

                                threading.Thread(
                                    target=self.translate_stt_text,
                                    args=(
                                        text,
                                        selected_language,
                                        detected_language
                                    ),
                                    daemon=True
                                ).start()

                            else:

                                self.root.after(
                                    0,
                                    self.add_transcript,
                                    text
                                )

            except Exception:
                pass

            finally:

                if self.recording:

                    self.root.after(
                        0,
                        self.finish_recording
                    )


        # ========================================================
        # ADD TRANSCRIPT
        # ========================================================

    def translate_stt_text(
        self,
        text,
        selected_language,
        detected_language
    ):

        try:

            import requests

            target_code = LANGUAGES.get(
                selected_language,
                "en"
            )

            source_code = detected_language

            if source_code == target_code:

                self.root.after(
                    0,
                    self.add_transcript,
                    text
                )

                return

            response = requests.get(
                "https://api.mymemory.translated.net/get",
                params={
                    "q": text,
                    "langpair": source_code + "|" + target_code
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            translated = data.get(
                "responseData",
                {}
            ).get(
                "translatedText",
                ""
            ).strip()

            if not translated:

                raise Exception(
                    "Translation service returned empty text."
                )

            self.root.after(
                0,
                self.add_transcript,
                translated
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "Translation Error",
                    str(error)
                )
            )


    def add_transcript(self, text):

        if not text:

            return

        self.session_text += text + " "

        if self.transcript_text:

            self.transcript_text.insert(
                "end",
                text + "\n"
            )

            self.transcript_text.see(
                "end"
            )


    # ========================================================
    # STOP RECORDING
    # ========================================================

    def stop_recording(self):

        if not self.recording:
            return

        self.stop_requested = True

        try:
            sd.stop()
        except Exception:
            pass

        if hasattr(
            self,
            "status_label"
        ):

            self.status_label.config(
                text="Stopping recording..."
            )



    def finish_recording(self):

        self.recording = False

        if hasattr(self, "record_button"):

            self.record_button.config(
                state="normal"
            )

        if hasattr(self, "stop_button"):

            self.stop_button.config(
                state="disabled"
            )

        if hasattr(self, "status_label"):

            self.status_label.config(
                text="Recording stopped"
            )

        if self.session_text.strip():

            self.add_history(
                "Speech → Text",
                self.stt_language.get(),
                self.session_text.strip()
            )


    # ========================================================
    # CLEAR TRANSCRIPT
    # ========================================================

    def clear_transcript(self):

        if self.transcript_text:

            self.transcript_text.delete(
                "1.0",
                "end"
            )

        self.session_text = ""

        if hasattr(self, "status_label"):

            self.status_label.config(
                text="Transcript cleared"
            )


    # ========================================================
    # COPY TRANSCRIPT
    # ========================================================

    def copy_transcript(self):

        if not self.transcript_text:

            return

        text = self.transcript_text.get(
            "1.0",
            "end-1c"
        ).strip()

        if not text:

            messagebox.showwarning(
                "Copy",
                "There is no text to copy."
            )

            return

        self.root.clipboard_clear()

        self.root.clipboard_append(
            text
        )

        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Transcript copied to clipboard."
        )


    # ========================================================
    # SAVE TRANSCRIPT
    # ========================================================

    def save_transcript(self):

        if not self.transcript_text:

            return

        text = self.transcript_text.get(
            "1.0",
            "end-1c"
        ).strip()

        if not text:

            messagebox.showwarning(
                "Save",
                "There is no transcript to save."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Save Transcript",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )

        if not filename:

            return

        try:

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(text)

            messagebox.showinfo(
                "Saved",
                "Transcript saved successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Save Error",
                str(error)
            )


    # ========================================================
    # TEXT TO SPEECH PAGE
    # ========================================================

    def show_tts_page(self):

        self.clear_main()

        tk.Label(
            self.main_area,
            text="Text → Speech",
            font=("Helvetica", 26, "bold"),
            fg="#29243A",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            self.main_area,
            text="Type your text and let VOICERA speak it aloud.",
            font=("Helvetica", 11),
            fg="#777180",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        # CONTROLS

        controls = tk.Frame(
            self.main_area,
            bg="#F6F3FB"
        )

        controls.pack(
            fill="x",
            padx=35,
            pady=(0, 10)
        )

        tk.Label(
            controls,
            text="Language",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="#F6F3FB"
        ).pack(
            side="left"
        )

        self.tts_language = ttk.Combobox(
            controls,
            values=list(LANGUAGES.keys()),
            state="readonly",
            width=18
        )

        self.tts_language.set(
            "English"
        )

        self.tts_language.pack(
            side="left",
            padx=(10, 0)
        )

        tk.Label(
            controls,
            text="Mode",
            font=("Helvetica", 10, "bold"),
            fg="#4B4559",
            bg="#F6F3FB"
        ).pack(
            side="left",
            padx=(25, 0)
        )

        self.tts_mode = ttk.Combobox(
            controls,
            values=[
                "Actual Language",
                "Translated Language"
            ],
            state="readonly",
            width=20
        )

        self.tts_mode.set(
            "Actual Language"
        )

        self.tts_mode.pack(
            side="left",
            padx=(10, 0)
        )

        # EDITOR

        editor_container = tk.Frame(
            self.main_area,
            bg="white",
            highlightbackground="#E2DDED",
            highlightthickness=1
        )

        editor_container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        tk.Label(
            editor_container,
            text="Enter text to speak",
            font=("Helvetica", 12, "bold"),
            fg="#29243A",
            bg="white"
        ).pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        self.tts_text = tk.Text(
            editor_container,
            font=("Helvetica", 14),
            bg="white",
            fg="#29243A",
            insertbackground="#7667A8",
            relief="flat",
            wrap="word",
            padx=25,
            pady=20
        )

        self.tts_text.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # BOTTOM

        bottom = tk.Frame(
            self.main_area,
            bg="#F6F3FB"
        )

        bottom.pack(
            fill="x",
            padx=35,
            pady=(10, 25)
        )

        clear_button = self.rounded_button(
            bottom,
            "Clear",
            self.clear_tts,
            width=100,
            height=42,
            bg="#E8E3F1",
            hover="#DCD5E8",
            fg="#625A70",
            font=("Helvetica", 10, "bold")
        )

        clear_button.pack(
            side="right",
            padx=5
        )

        speak_button = self.rounded_button(
            bottom,
            "🔊  SPEAK",
            self.speak_text,
            width=150,
            height=42,
            bg="#7667A8",
            hover="#62558F",
            fg="white",
            font=("Helvetica", 11, "bold")
        )

        speak_button.pack(
            side="right",
            padx=5
        )


    # ========================================================
    # SPEAK TEXT
    # ========================================================

    def speak_text(self):

        if not self.tts_text:
            return

        text = self.tts_text.get(
            "1.0",
            "end-1c"
        ).strip()

        if not text:
            messagebox.showwarning(
                "Text to Speech",
                "Please enter some text first."
            )
            return

        language = self.tts_language.get()

        mode = getattr(
            self,
            "tts_mode",
            None
        )

        selected_mode = (
            mode.get()
            if mode
            else "Actual Language"
        )

        threading.Thread(
            target=self.run_tts,
            args=(
                text,
                language,
                selected_mode
            ),
            daemon=True
        ).start()


    # ========================================================
    # EDGE TTS
    # ========================================================

    def run_tts(
        self,
        text,
        language,
        selected_mode
    ):

        try:

            import asyncio
            import tempfile
            import os
            import subprocess
            import requests
            from langdetect import detect

            language_settings = {
                "English": {
                    "code": "en",
                    "voice": "en-US-AriaNeural"
                },
                "Hindi": {
                    "code": "hi",
                    "voice": "hi-IN-SwaraNeural"
                },
                "Marathi": {
                    "code": "mr",
                    "voice": "mr-IN-AarohiNeural"
                },
                "Gujarati": {
                    "code": "gu",
                    "voice": "gu-IN-DhwaniNeural"
                },
                "Bengali": {
                    "code": "bn",
                    "voice": "bn-IN-TanishaaNeural"
                },
                "Tamil": {
                    "code": "ta",
                    "voice": "ta-IN-PallaviNeural"
                },
                "Telugu": {
                    "code": "te",
                    "voice": "te-IN-ShrutiNeural"
                },
                "Kannada": {
                    "code": "kn",
                    "voice": "kn-IN-SapnaNeural"
                },
                "Malayalam": {
                    "code": "ml",
                    "voice": "ml-IN-SobhanaNeural"
                },
                "Punjabi": {
                    "code": "pa",
                    "voice": "pa-IN-VaaniNeural"
                }
            }

            # Detect the language of the entered text
            detected_code = detect(text)

            # Map langdetect codes to supported VOICERA codes
            detected_map = {
                "en": "en",
                "hi": "hi",
                "mr": "mr",
                "gu": "gu",
                "bn": "bn",
                "ta": "ta",
                "te": "te",
                "kn": "kn",
                "ml": "ml",
                "pa": "pa"
            }

            detected_code = detected_map.get(
                detected_code,
                "en"
            )

            if selected_mode == "Translated Language":

                target = language_settings.get(
                    language,
                    language_settings["English"]
                )

                target_code = target["code"]

                if detected_code == target_code:

                    final_text = text

                else:

                    response = requests.get(
                        "https://api.mymemory.translated.net/get",
                        params={
                            "q": text,
                            "langpair": detected_code + "|" + target_code
                        },
                        timeout=15
                    )

                    response.raise_for_status()

                    data = response.json()

                    final_text = data.get(
                        "responseData",
                        {}
                    ).get(
                        "translatedText",
                        ""
                    ).strip()

                    if not final_text:
                        raise Exception(
                            "Translation returned empty text."
                        )

                voice = target["voice"]

            else:

                # ACTUAL LANGUAGE:
                # speak the text in the language it was written in

                actual_settings = None

                for settings in language_settings.values():

                    if settings["code"] == detected_code:
                        actual_settings = settings
                        break

                if actual_settings is None:
                    actual_settings = language_settings["English"]

                final_text = text
                voice = actual_settings["voice"]

            # Generate natural neural speech
            import edge_tts

            temp_file = tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            )

            temp_file.close()

            async def generate_voice():

                communicate = edge_tts.Communicate(
                    final_text,
                    voice
                )

                await communicate.save(
                    temp_file.name
                )

            asyncio.run(
                generate_voice()
            )

            subprocess.run(
                [
                    "/usr/bin/afplay",
                    temp_file.name
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            try:
                os.remove(temp_file.name)
            except Exception:
                pass

            self.root.after(
                0,
                lambda: self.add_history(
                    "Text → Speech",
                    language,
                    final_text
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: messagebox.showerror(
                    "TTS Error",
                    str(error)
                )
            )


    # ========================================================
    # CLEAR TTS
    # ========================================================

    def clear_tts(self):

        if self.tts_text:

            self.tts_text.delete(
                "1.0",
                "end"
            )


    # ========================================================
    # HISTORY
    # ========================================================

    def add_history(
        self,
        mode,
        language,
        text
    ):

        history = load_history()

        history.append(
            {
                "username": self.current_user,
                "mode": mode,
                "language": language,
                "text": text,
                "time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }
        )

        save_history_data(
            history
        )


    # ========================================================
    # HISTORY PAGE
    # ========================================================

    def show_history_page(self):

        self.clear_main()

        tk.Label(
            self.main_area,
            text="History",
            font=("Helvetica", 26, "bold"),
            fg="#29243A",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            self.main_area,
            text="Your previous speech conversions.",
            font=("Helvetica", 11),
            fg="#777180",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35,
            pady=(0, 20)
        )

        container = tk.Frame(
            self.main_area,
            bg="white"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        columns = (
            "mode",
            "language",
            "text",
            "time"
        )

        self.history_tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings"
        )

        self.history_tree.heading(
            "mode",
            text="Mode"
        )

        self.history_tree.heading(
            "language",
            text="Language"
        )

        self.history_tree.heading(
            "text",
            text="Text"
        )

        self.history_tree.heading(
            "time",
            text="Date / Time"
        )

        self.history_tree.column(
            "mode",
            width=150
        )

        self.history_tree.column(
            "language",
            width=100
        )

        self.history_tree.column(
            "text",
            width=450
        )

        self.history_tree.column(
            "time",
            width=170
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.history_tree.yview
        )

        self.history_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.history_tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=15
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=15,
            padx=(0, 15)
        )

        history = load_history()

        user_history = [
            item
            for item in history
            if item.get("username") == self.current_user
        ]

        for item in reversed(user_history):

            self.history_tree.insert(
                "",
                "end",
                values=(
                    item.get("mode", ""),
                    item.get("language", ""),
                    item.get("text", ""),
                    item.get("time", "")
                )
            )

        bottom = tk.Frame(
            self.main_area,
            bg="#F6F3FB"
        )

        bottom.pack(
            fill="x",
            padx=35,
            pady=15
        )

        tk.Button(
            bottom,
            text="Refresh",
            command=self.show_history_page,
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#7667A8",
            activebackground="#62558F",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            ipadx=12,
            ipady=6
        )


    # ========================================================
    # ABOUT
    # ========================================================

    def show_about(self):

        self.clear_main()

        tk.Label(
            self.main_area,
            text="About VOICERA",
            font=("Helvetica", 26, "bold"),
            fg="#29243A",
            bg="#F6F3FB"
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 20)
        )

        card = tk.Frame(
            self.main_area,
            bg="white"
        )

        card.pack(
            fill="x",
            padx=35,
            pady=10
        )

        tk.Label(
            card,
            text="VOICERA",
            font=("Helvetica", 30, "bold"),
            fg="#7667A8",
            bg="white"
        ).pack(
            pady=(35, 5)
        )

        tk.Label(
            card,
            text=TAGLINE,
            font=("Helvetica", 13),
            fg="#777180",
            bg="white"
        ).pack(
            pady=(0, 20)
        )

        tk.Label(
            card,
            text=DESCRIPTION,
            font=("Helvetica", 12, "bold"),
            fg="#29243A",
            bg="white"
        ).pack(
            pady=5
        )

        tk.Label(
            card,
            text=(
                "VOICERA provides speech recognition and "
                "text-to-speech features through a simple "
                "and professional desktop interface."
            ),
            font=("Helvetica", 11),
            fg="#777180",
            bg="white",
            justify="center"
        ).pack(
            pady=(5, 40)
        )


    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        if self.recording:

            self.stop_recording()

        self.current_user = None
        self.current_name = None

        clear_session_user()

        self.show_login()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = VoiceraApp(
        root
    )

    root.mainloop()
