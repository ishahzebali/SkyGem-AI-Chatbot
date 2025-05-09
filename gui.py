import tkinter as tk
from tkinter import Text, Scrollbar, Toplevel, ttk, messagebox
from datetime import datetime
import os
import glob
from api import search_web
from utils import resource_path, parse_markdown, get_response
from voice import capture_voice_input

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyGem - AI Chatbot")
        self.root.geometry("600x700")
        self.root.withdraw()  # Hide the main window initially

        # API keys
        self.weather_api_key = "008da70b8b9ab024d7cbcec8d058b7b3"
        self.gemini_api_key = "AIzaSyCJNmRPn0oOam-k4uOgkt3ArsDJMi0Rz4I"

        # Configure ttk style for rounded buttons
        self.style = ttk.Style()
        self.style.configure(
            "RoundedButton.TButton",
            borderwidth=2,
            relief="raised",
            padding=(10, 5),
            background="#6A5ACD",  # Solid purplish background
            foreground="#000000",  # Black text
            anchor="center"
        )
        self.style.map(
            "RoundedButton.TButton",
            background=[("active", "#7B68EE")],  # Lighter purple on hover
            foreground=[("active", "#000000")]
        )
        self.style.configure(
            "DisabledRoundedButton.TButton",
            background="#A9A9A9",  # Muted purplish-gray for disabled state
            foreground="#000000"
        )

        # Configure scrollbar style
        self.style.configure(
            "Custom.Vertical.TScrollbar",
            troughcolor="#4B0082",  # Indigo trough
            background="#6A5ACD",   # Purplish bar
            arrowcolor="#FFFFFF"
        )

        # Show splash screen
        self.show_splash_screen()

        # Set the window icon
        try:
            icon_path = resource_path("skygem_icon.png")
            icon_image = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(True, icon_image)
        except tk.TclError as e:
            print(f"Error loading icon: {e}. Make sure 'skygem_icon.png' is in the project directory or bundled correctly.")

    def show_splash_screen(self):
        # Create splash screen window
        self.splash = Toplevel(self.root)
        self.splash.title("Loading SkyGem")
        self.splash.geometry("300x150")
        self.splash.configure(bg="#4B0082")  # Indigo background
        self.splash.overrideredirect(True)  # Remove window borders

        # Center the splash screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (300 // 2)
        y = (screen_height // 2) - (150 // 2)
        self.splash.geometry(f"300x150+{x}+{y}")

        # Splash screen content
        tk.Label(
            self.splash,
            text="SkyGem",
            font=("Segoe UI", 24, "bold"),
            bg="#4B0082",
            fg="#FFFFFF"
        ).pack(pady=30)
        tk.Label(
            self.splash,
            text="Loading...",
            font=("Segoe UI", 14),
            bg="#4B0082",
            fg="#FFFFFF"
        ).pack()

        # Close splash screen and show main window after 3 seconds
        self.root.after(3000, self.close_splash_and_show_main)

    def close_splash_and_show_main(self):
        self.splash.destroy()
        self.root.deiconify()  # Show the main window
        self.setup_main_window()

    def setup_main_window(self):
        # Create sessions directory
        self.sessions_dir = "chat_sessions"
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)

        # Migrate old conversation_history.txt if it exists
        self.migrate_old_history()

        # Start a new session
        session_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.current_session_file = os.path.join(self.sessions_dir, f"session_{session_timestamp}.txt")
        self.conversation_history = []
        self.load_current_session()

        # Apply custom theme
        self.root.configure(bg="#4B0082")  # Deeper indigo background

        # Title label with background
        title_frame = tk.Frame(self.root, bg="#6A5ACD")  # Purplish background for title
        title_frame.pack(pady=10, fill=tk.X)
        self.title_label = tk.Label(
            title_frame, 
            text="SkyGem - Your AI Assistant", 
            font=("Segoe UI", 18, "bold"), 
            bg="#6A5ACD", 
            fg="#FFFFFF"
        )
        self.title_label.pack(pady=8)

        # Create tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Chat Tab
        self.chat_tab = tk.Frame(self.notebook, bg="#E6E6FA")
        self.notebook.add(self.chat_tab, text="Chat")

        # History Tab
        self.history_tab = tk.Frame(self.notebook, bg="#E6E6FA")
        self.notebook.add(self.history_tab, text="History")

        # Setup Chat Tab
        self.setup_chat_tab()

        # Setup History Tab
        self.setup_history_tab()

    def setup_chat_tab(self):
        # Chat window frame
        self.chat_frame = tk.Frame(self.chat_tab, bg="#E6E6FA")
        self.chat_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Chat window (Text widget with scrollbar)
        self.chat_window = Text(
            self.chat_frame, 
            wrap=tk.WORD, 
            height=25, 
            width=50, 
            state='disabled',
            font=("Segoe UI", 12),
            bg="#F5F5FA",  # Slightly darker background
            fg="#4B0082",  # Indigo text
            bd=4, 
            relief="groove",
            spacing1=8,
            spacing3=8
        )
        self.chat_window.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Scrollbar for chat window
        self.chat_scrollbar = ttk.Scrollbar(self.chat_frame, orient=tk.VERTICAL, command=self.chat_window.yview, style="Custom.Vertical.TScrollbar")
        self.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_window['yscrollcommand'] = self.chat_scrollbar.set

        # Configure tags for message bubbles and formatting
        self.chat_window.tag_configure("user", 
            background="#C4A1D4",  # Darker thistle for user messages
            foreground="#4B0082",  # Indigo text
            justify="right",
            lmargin1=100,
            rmargin=10,
            wrap="word",
            relief="raised",
            borderwidth=1,
            font=("Segoe UI", 12)
        )
        self.chat_window.tag_configure("bot", 
            background="#D8D8FA",  # Softer lavender for bot messages
            foreground="#4B0082",  # Indigo text
            justify="left",
            lmargin1=10,
            rmargin=100,
            wrap="word",
            relief="raised",
            borderwidth=1,
            font=("Segoe UI", 12)
        )
        self.chat_window.tag_configure("timestamp", 
            foreground="#888888", 
            font=("Segoe UI", 10), 
            justify="center",
            lmargin1=0,
            rmargin=0
        )
        self.chat_window.tag_configure("bold", font=("Segoe UI", 12, "bold"))
        self.chat_window.tag_configure("italic", font=("Segoe UI", 12, "italic"))
        self.chat_window.tag_configure("bullet", font=("Segoe UI", 12), lmargin1=20)
        self.chat_window.tag_configure("button_align", lmargin1=10)

        # Input frame
        self.input_frame = tk.Frame(self.chat_tab, bg="#E6E6FA")
        self.input_frame.pack(padx=10, pady=5, fill=tk.X)

        # Input field
        self.input_field = tk.Entry(
            self.input_frame, 
            width=40, 
            font=("Segoe UI", 16),
            bg="#E0E0FA",  # Slightly darker shade
            fg="#333333",
            bd=4, 
            relief="groove",
            insertbackground="#333333",
            highlightthickness=2,
            highlightcolor="#4B0082",  # Indigo highlight
            highlightbackground="#4B0082"
        )
        self.input_field.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Placeholder label
        self.placeholder_label = tk.Label(
            self.input_frame,
            text="Type your message here...",
            font=("Segoe UI", 16),
            fg="#666666",  # Darker gray for better visibility
            bg="#E0E0FA"
        )
        self.placeholder_label.place(in_=self.input_field, x=10, y=10)

        # Bind events to manage placeholder
        self.input_field.bind("<FocusIn>", self.hide_placeholder)
        self.input_field.bind("<FocusOut>", self.show_placeholder)
        self.input_field.bind("<KeyRelease>", self.handle_input_change)
        self.input_field.bind("<Return>", self.send_message)

        # Mic button (Rounded, Purplish, with Icon)
        try:
            mic_icon_path = resource_path("mic_icon.png")
            self.mic_icon = tk.PhotoImage(file=mic_icon_path).subsample(2, 2)  # Resize icon
        except tk.TclError as e:
            print(f"Error loading mic icon: {e}. Using text instead.")
            self.mic_icon = None

        self.mic_button = ttk.Button(
            self.input_frame,
            image=self.mic_icon if self.mic_icon else None,
            text="Mic" if not self.mic_icon else "",
            command=self.capture_voice_input_wrapper,
            style="RoundedButton.TButton"
        )
        self.mic_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Send button (Rounded, Purplish, Black Text)
        self.send_button = ttk.Button(
            self.input_frame, 
            text="Send", 
            command=self.send_message, 
            style="RoundedButton.TButton",
            state='disabled'
        )
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Clear button (Rounded, Purplish, Black Text)
        self.clear_button = ttk.Button(
            self.chat_tab, 
            text="Clear Chat", 
            command=self.clear_chat,
            style="RoundedButton.TButton"
        )
        self.clear_button.pack(pady=10)

        # Display initial message if no history was loaded
        if not self.conversation_history:
            initial_message = "Hi! I'm SkyGem, your AI assistant. I can answer questions or fetch info from the web. Try asking about the weather or a simple fact! You can also speak your query using the Mic button."
            self.add_message(initial_message, "bot")

    def setup_history_tab(self):
        # History tab layout
        self.history_frame = tk.Frame(self.history_tab, bg="#E6E6FA")
        self.history_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Left panel: List of sessions
        self.session_list_frame = tk.Frame(self.history_frame, bg="#E6E6FA")
        self.session_list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        tk.Label(
            self.session_list_frame,
            text="Previous Sessions",
            font=("Segoe UI", 12, "bold"),
            bg="#E6E6FA",
            fg="#333333"
        ).pack(pady=5)

        self.session_listbox = tk.Listbox(
            self.session_list_frame,
            width=25,
            height=25,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg="#333333",
            bd=2,
            relief="groove",
            selectbackground="#4B0082",  # Indigo selection
            selectforeground="#FFFFFF"
        )
        self.session_listbox.pack(side=tk.LEFT, fill=tk.Y)
        self.session_listbox.bind("<<ListboxSelect>>", self.display_selected_session)

        # Scrollbar for session list
        self.session_scrollbar = ttk.Scrollbar(self.session_list_frame, orient=tk.VERTICAL, command=self.session_listbox.yview, style="Custom.Vertical.TScrollbar")
        self.session_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.session_listbox['yscrollcommand'] = self.session_scrollbar.set

        # Right panel: Session messages
        self.session_display_frame = tk.Frame(self.history_frame, bg="#E6E6FA")
        self.session_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.session_display = Text(
            self.session_display_frame,
            wrap=tk.WORD,
            height=25,
            width=50,
            state='disabled',
            font=("Segoe UI", 12),
            bg="#F5F5FA",  # Slightly darker background
            fg="#4B0082",  # Indigo text
            bd=4,
            relief="groove",
            spacing1=8,
            spacing3=8
        )
        self.session_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for session display
        self.display_scrollbar = ttk.Scrollbar(self.session_display_frame, orient=tk.VERTICAL, command=self.session_display.yview, style="Custom.Vertical.TScrollbar")
        self.display_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.session_display['yscrollcommand'] = self.display_scrollbar.set

        # Configure tags for session display (similar to chat window)
        self.session_display.tag_configure("user", 
            background="#C4A1D4",  # Darker thistle for user messages
            foreground="#4B0082",  # Indigo text
            justify="right",
            lmargin1=100,
            rmargin=10,
            wrap="word",
            relief="raised",
            borderwidth=1,
            font=("Segoe UI", 12)
        )
        self.session_display.tag_configure("bot", 
            background="#D8D8FA",  # Softer lavender for bot messages
            foreground="#4B0082",  # Indigo text
            justify="left",
            lmargin1=10,
            rmargin=100,
            wrap="word",
            relief="raised",
            borderwidth=1,
            font=("Segoe UI", 12)
        )
        self.session_display.tag_configure("timestamp", 
            foreground="#888888", 
            font=("Segoe UI", 10), 
            justify="center",
            lmargin1=0,
            rmargin=0
        )
        self.session_display.tag_configure("bold", font=("Segoe UI", 12, "bold"))
        self.session_display.tag_configure("italic", font=("Segoe UI", 12, "italic"))
        self.session_display.tag_configure("bullet", font=("Segoe UI", 12), lmargin1=20)

        # Delete session button (Rounded, Purplish, Black Text)
        self.delete_button = ttk.Button(
            self.history_tab,
            text="Delete Session",
            command=self.delete_selected_session,
            style="RoundedButton.TButton"
        )
        self.delete_button.pack(pady=10)

        # Load sessions into the listbox
        self.load_session_list()

    def migrate_old_history(self):
        """Migrate old conversation_history.txt to a session file"""
        old_file = "conversation_history.txt"
        if os.path.exists(old_file):
            session_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_session_file = os.path.join(self.sessions_dir, f"session_{session_timestamp}_migrated.txt")
            try:
                with open(old_file, 'r') as f, open(new_session_file, 'w') as new_f:
                    for line in f:
                        if line.strip():
                            new_f.write(line)
                os.remove(old_file)
                print(f"Migrated old history to {new_session_file}")
            except Exception as e:
                print(f"Error migrating old history: {e}")

    def load_session_list(self):
        """Load the list of session files into the Listbox"""
        self.session_listbox.delete(0, tk.END)
        self.session_files = sorted(glob.glob(os.path.join(self.sessions_dir, "session_*.txt")), key=os.path.getmtime, reverse=True)
        for session_file in self.session_files:
            # Extract timestamp from filename
            filename = os.path.basename(session_file)
            timestamp = filename.replace("session_", "").replace(".txt", "")
            if "_migrated" in timestamp:
                timestamp = timestamp.replace("_migrated", " (Migrated)")
            self.session_listbox.insert(tk.END, timestamp)

    def display_selected_session(self, event):
        """Display the selected session's messages in the Text widget"""
        selection = self.session_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        session_file = self.session_files[index]

        self.session_display.config(state='normal')
        self.session_display.delete(1.0, tk.END)

        try:
            with open(session_file, 'r') as f:
                for line in f:
                    if line.strip():
                        timestamp, role, message = line.strip().split("|", 2)
                        prefix = "You: " if role == "user" else "SkyGem: "
                        self.session_display.insert(tk.END, f"[{timestamp}]\n", "timestamp")
                        if role == "bot":
                            segments = parse_markdown(message)
                            self.session_display.insert(tk.END, prefix, role)
                            for style, text in segments:
                                self.session_display.insert(tk.END, text, (role, style))
                            self.session_display.insert(tk.END, "\n", role)
                        else:
                            self.session_display.insert(tk.END, prefix + message, role)
                        self.session_display.insert(tk.END, "\n\n")
        except Exception as e:
            print(f"Error loading session: {e}")
            self.session_display.insert(tk.END, "Error loading session.\n")

        self.session_display.config(state='disabled')
        self.session_display.see(tk.END)

    def delete_selected_session(self):
        """Delete the selected session file and refresh the list"""
        selection = self.session_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        session_file = self.session_files[index]

        try:
            os.remove(session_file)
            self.load_session_list()
            self.session_display.config(state='normal')
            self.session_display.delete(1.0, tk.END)
            self.session_display.config(state='disabled')
        except Exception as e:
            print(f"Error deleting session: {e}")

    def load_current_session(self):
        """Load the current session's history"""
        try:
            with open(self.current_session_file, 'r') as f:
                for line in f:
                    if line.strip():
                        timestamp, role, message = line.strip().split("|", 2)
                        self.conversation_history.append({"role": role, "message": message})
                        self.add_message_to_window_only(message, role, timestamp)
        except FileNotFoundError:
            # File will be created on first save
            pass
        except Exception as e:
            print(f"Error loading current session: {e}")

    def save_conversation_history(self, timestamp, role, message):
        """Save a single message to the current session file"""
        try:
            with open(self.current_session_file, 'a') as f:
                f.write(f"{timestamp}|{role}|{message}\n")
        except Exception as e:
            print(f"Error saving conversation history: {e}")

    def add_message_to_window_only(self, message, sender, timestamp):
        """Add message to the chat window without saving to history (used for loading)"""
        self.chat_window.config(state='normal')
        self.chat_window.insert(tk.END, f"[{timestamp}]\n", "timestamp")
        prefix = "You: " if sender == "user" else "SkyGem: "
        
        if sender == "bot":
            segments = parse_markdown(message)
            self.chat_window.insert(tk.END, prefix, sender)
            for style, text in segments:
                self.chat_window.insert(tk.END, text, (sender, style))
            self.chat_window.insert(tk.END, "\n", "bot")
            # Copy button (Elevated, Rounded, Purplish, Black Text)
            copy_button = tk.Label(
                self.chat_window,
                text="Copy",
                font=("Segoe UI", 9, "bold"),
                bg="#6A5ACD",  # Purplish background
                fg="#000000",  # Black text
                bd=0,  # No outline
                relief="raised",
                padx=8,
                pady=4,
                cursor="hand2"
            )
            copy_button.bind("<Enter>", self.on_enter)
            copy_button.bind("<Leave>", self.on_leave)
            copy_button.bind("<Button-1>", lambda e: self.copy_to_clipboard(message))
            self.chat_window.window_create(tk.END, window=copy_button, padx=0, pady=2)
            self.chat_window.insert(tk.END, "", "button_align")
        else:
            self.chat_window.insert(tk.END, prefix + message, sender)

        self.chat_window.insert(tk.END, "\n\n")
        self.chat_window.config(state='disabled')
        self.chat_window.see(tk.END)
        self.root.update()

    def capture_voice_input_wrapper(self):
        """Wrapper to pass instance methods to voice input function"""
        capture_voice_input(self)

    def hide_placeholder(self, event):
        if not self.input_field.get().strip():
            self.placeholder_label.place_forget()

    def show_placeholder(self, event):
        if not self.input_field.get().strip():
            self.placeholder_label.place(in_=self.input_field, x=10, y=10)

    def handle_input_change(self, event):
        text = self.input_field.get().strip()
        if text:
            self.send_button.config(state='normal', style="RoundedButton.TButton")
        else:
            self.send_button.config(state='disabled', style="DisabledRoundedButton.TButton")
            self.placeholder_label.place(in_=self.input_field, x=10, y=10)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def on_enter(self, event):
        event.widget.config(bg="#7B68EE")  # Lighter purple on hover

    def on_leave(self, event):
        event.widget.config(bg="#6A5ACD")  # Purplish background

    def add_message(self, message, sender="user"):
        self.chat_window.config(state='normal')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_window.insert(tk.END, f"[{timestamp}]\n", "timestamp")
        prefix = "You: " if sender == "user" else "SkyGem: "
        
        if sender == "bot":
            segments = parse_markdown(message)
            self.chat_window.insert(tk.END, prefix, sender)
            for style, text in segments:
                self.chat_window.insert(tk.END, text, (sender, style))
            self.chat_window.insert(tk.END, "\n", "bot")
            # Copy button (Elevated, Rounded, Purplish, Black Text)
            copy_button = tk.Label(
                self.chat_window,
                text="Copy",
                font=("Segoe UI", 9, "bold"),
                bg="#6A5ACD",  # Purplish background
                fg="#ffffff",  # white text
                bd=0,  # No outline
                relief="raised",
                padx=8,
                pady=4,
                cursor="hand2"
            )
            copy_button.bind("<Enter>", self.on_enter)
            copy_button.bind("<Leave>", self.on_leave)
            copy_button.bind("<Button-1>", lambda e: self.copy_to_clipboard(message))
            self.chat_window.window_create(tk.END, window=copy_button, padx=0, pady=2)
            self.chat_window.insert(tk.END, "", "button_align")
        else:
            self.chat_window.insert(tk.END, prefix + message, sender)

        # Add to conversation history and save to file
        self.conversation_history.append({"role": sender, "message": message})
        self.save_conversation_history(timestamp, sender, message)

        self.chat_window.insert(tk.END, "\n\n")
        self.chat_window.config(state='disabled')
        self.chat_window.see(tk.END)
        self.root.update()

    def send_message(self, event=None):
        user_input = self.input_field.get().strip()
        if not user_input:
            self.add_message("Please type or speak a message!", "bot")
            return
        self.add_message(user_input, "user")
        response = get_response(user_input, self.weather_api_key, self.gemini_api_key, self.conversation_history)
        self.add_message(response, "bot")
        # Clear the input field
        self.input_field.delete(0, tk.END)
        self.send_button.config(state='disabled', style="DisabledRoundedButton.TButton")
        self.placeholder_label.place(in_=self.input_field, x=10, y=10)
        self.root.update()

    def clear_chat(self):
        self.chat_window.config(state='normal')
        self.chat_window.delete(1.0, tk.END)
        self.chat_window.config(state='disabled')
        # Clear current session history
        self.conversation_history = []
        try:
            with open(self.current_session_file, 'w') as f:
                f.write("")  # Clear the file
        except Exception as e:
            print(f"Error clearing current session file: {e}")
        initial_message = "Hi! I'm SkyGem, your AI assistant. I can answer questions or fetch info from the web. Try asking about the weather or a simple fact! You can also speak your query using the Mic button."
        self.add_message(initial_message, "bot")