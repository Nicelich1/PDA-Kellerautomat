import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Tuple, Dict
import time


class KellerautomatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kellerautomat (PDA) - Interaktive Visualisierung")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Kellerautomat Zustand
        self.stack = []
        self.current_state = "q0"
        self.input_string = ""
        self.input_position = 0
        self.step_history = []
        self.is_running = False
        self.animation_speed = 500  # ms
        
        # Automaten-Modi
        self.automaton_mode = "anbn"  # Default: a^n b^n
        
        # Sprache
        self.language = "en"  # Default: English
        
        # Wird in load_automaton gesetzt
        self.transitions = {}
        self.accepting_states = []
        self.initial_stack_symbol = "Z"
        
        # Lade Standard-Automaten
        self.load_automaton("anbn")
        
        self.create_widgets()
        self.load_automaton(self.automaton_mode)
        self.setup_example()
        
    def load_automaton(self, mode):
        """Lädt verschiedene Automaten-Definitionen"""
        self.automaton_mode = mode
        
        if mode == "anbn":
            # Automat für a^n b^n (gleich viele a wie b)
            self.transitions = {
                # a lesen: pushe A auf Stack
                ("q0", "a", "Z"): ("q0", ["A", "Z"]),
                ("q0", "a", "A"): ("q0", ["A", "A"]),
                # b lesen: pop A vom Stack
                ("q0", "b", "A"): ("q1", []),
                ("q1", "b", "A"): ("q1", []),
                # Epsilon-Übergang zum Endzustand
                ("q1", "", "Z"): ("qf", ["Z"]),
            }
            self.accepting_states = ["qf"]
            
            if self.language == "de":
                self.info_text = """
Ein Kellerautomat (PDA) besteht aus:

• Zuständen (q0, q1, ...)
• Eingabealphabet (Symbole)
• Stack-Alphabet
• Übergangsfunktion
• Startzustand
• Anfangsstacksymbol

Aktueller Automat: a^n b^n
Erkennt Strings mit gleich vielen
a's gefolgt von b's:
• aabb ✓
• aaabbb ✓
• ab ✓
• aab ✗
• abab ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Funktionsweise:

1. Start in Zustand q0 mit Stack [Z]

2. Für jedes 'a':
   • Lese 'a' aus Eingabe
   • Pushe 'A' auf den Stack
   • Bleibe in q0
   → Zähle die a's auf dem Stack

3. Beim ersten 'b':
   • Lese 'b' aus Eingabe
   • Pop 'A' vom Stack
   • Wechsel zu q1
   
4. Für jedes weitere 'b':
   • Lese 'b' aus Eingabe
   • Pop 'A' vom Stack
   • Bleibe in q1
   → Entferne a's für jedes b

5. Am Ende (ε-Übergang):
   • Wenn nur noch [Z] auf Stack
   • Wechsel zu qf (Akzeptieren!)
   
Beispiel "aabb":
a → Stack: [Z,A]
a → Stack: [Z,A,A]
b → Stack: [Z,A]
b → Stack: [Z]
ε → Akzeptiert ✓
                """
            else:  # English
                self.info_text = """
A Pushdown Automaton (PDA) consists of:

• States (q0, q1, ...)
• Input alphabet (symbols)
• Stack alphabet
• Transition function
• Start state
• Initial stack symbol

Current Automaton: a^n b^n
Recognizes strings with equal
number of a's followed by b's:
• aabb ✓
• aaabbb ✓
• ab ✓
• aab ✗
• abab ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 How it works:

1. Start in state q0 with stack [Z]

2. For each 'a':
   • Read 'a' from input
   • Push 'A' onto stack
   • Stay in q0
   → Count a's on stack

3. At first 'b':
   • Read 'b' from input
   • Pop 'A' from stack
   • Move to q1
   
4. For each additional 'b':
   • Read 'b' from input
   • Pop 'A' from stack
   • Stay in q1
   → Remove a's for each b

5. At the end (ε-transition):
   • If only [Z] remains on stack
   • Move to qf (Accept!)
   
Example "aabb":
a → Stack: [Z,A]
a → Stack: [Z,A,A]
b → Stack: [Z,A]
b → Stack: [Z]
ε → Accepted ✓
                """
            
        elif mode == "klammern":
            # Automat für ausgeglichene Klammern
            self.transitions = {
                # Öffnende Klammer: pushe auf Stack
                ("q0", "(", "Z"): ("q0", ["(", "Z"]),
                ("q0", "(", "("): ("q0", ["(", "("]),
                # Schließende Klammer: pop vom Stack
                ("q0", ")", "("): ("q0", []),
                # Leere Eingabe mit leerem Stack -> Akzeptieren
                ("q0", "", "Z"): ("qf", ["Z"]),
            }
            self.accepting_states = ["qf"]
            
            if self.language == "de":
                self.info_text = """
Ein Kellerautomat (PDA) besteht aus:

• Zuständen (q0, q1, ...)
• Eingabealphabet (Symbole)
• Stack-Alphabet
• Übergangsfunktion
• Startzustand
• Anfangsstacksymbol

Aktueller Automat: Klammern
Erkennt ausgeglichene Klammern:
• (()) ✓
• ((()))  ✓
• ()() ✓
• ()) ✗
• (() ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Funktionsweise:

1. Start in Zustand q0 mit Stack [Z]

2. Für jede öffnende Klammer '(':
   • Lese '(' aus Eingabe
   • Pushe '(' auf den Stack
   • Bleibe in q0
   → Merke jede öffnende Klammer

3. Für jede schließende Klammer ')':
   • Lese ')' aus Eingabe
   • Pop '(' vom Stack
   • Bleibe in q0
   → Entferne passende öffnende Klammer

4. Am Ende (ε-Übergang):
   • Wenn nur noch [Z] auf Stack
   • Wechsel zu qf (Akzeptieren!)
   • Alle Klammern waren ausgeglichen

Beispiel "(())":
( → Stack: [Z,(]
( → Stack: [Z,(,(]
) → Stack: [Z,(]
) → Stack: [Z]
ε → Akzeptiert ✓
                """
            else:  # English
                self.info_text = """
A Pushdown Automaton (PDA) consists of:

• States (q0, q1, ...)
• Input alphabet (symbols)
• Stack alphabet
• Transition function
• Start state
• Initial stack symbol

Current Automaton: Parentheses
Recognizes balanced parentheses:
• (()) ✓
• ((()))  ✓
• ()() ✓
• ()) ✗
• (() ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 How it works:

1. Start in state q0 with stack [Z]

2. For each opening parenthesis '(':
   • Read '(' from input
   • Push '(' onto stack
   • Stay in q0
   → Remember each opening parenthesis

3. For each closing parenthesis ')':
   • Read ')' from input
   • Pop '(' from stack
   • Stay in q0
   → Remove matching opening parenthesis

4. At the end (ε-transition):
   • If only [Z] remains on stack
   • Move to qf (Accept!)
   • All parentheses were balanced

Example "(())":
( → Stack: [Z,(]
( → Stack: [Z,(,(]
) → Stack: [Z,(]
) → Stack: [Z]
ε → Accepted ✓
                """
            
        elif mode == "palindrom":
            # Automat für Palindrome (vereinfacht mit Mittelmarkierung #)
            self.transitions = {
                # Phase 1: Symbole auf Stack pushen
                ("q0", "a", "Z"): ("q0", ["a", "Z"]),
                ("q0", "b", "Z"): ("q0", ["b", "Z"]),
                ("q0", "a", "a"): ("q0", ["a", "a"]),
                ("q0", "a", "b"): ("q0", ["a", "b"]),
                ("q0", "b", "a"): ("q0", ["b", "a"]),
                ("q0", "b", "b"): ("q0", ["b", "b"]),
                # Mitte erkannt (#)
                ("q0", "#", "Z"): ("q1", ["Z"]),
                ("q0", "#", "a"): ("q1", ["a"]),
                ("q0", "#", "b"): ("q1", ["b"]),
                # Phase 2: Symbole vom Stack matchen
                ("q1", "a", "a"): ("q1", []),
                ("q1", "b", "b"): ("q1", []),
                # Epsilon zum Ende
                ("q1", "", "Z"): ("qf", ["Z"]),
            }
            self.accepting_states = ["qf"]
            
            if self.language == "de":
                self.info_text = """
Ein Kellerautomat (PDA) besteht aus:

• Zuständen (q0, q1, ...)
• Eingabealphabet (Symbole)
• Stack-Alphabet
• Übergangsfunktion
• Startzustand
• Anfangsstacksymbol

Aktueller Automat: Palindrome
Erkennt Palindrome mit # in der Mitte:
• aba#aba ✓
• aa#aa ✓
• ab#ba ✓
• abc#cba ✓
• ab#ab ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Funktionsweise:

1. Start in Zustand q0 mit Stack [Z]

2. Phase 1 - Erste Hälfte lesen:
   • Lese Symbole (a oder b)
   • Pushe jedes Symbol auf Stack
   • Bleibe in q0
   → Speichere erste Hälfte

3. Mitte erreicht (#):
   • Lese '#' aus Eingabe
   • Wechsel zu q1
   → Beginne Vergleichsphase

4. Phase 2 - Zweite Hälfte prüfen:
   • Lese Symbol aus Eingabe
   • Pop gleiches Symbol vom Stack
   • Bleibe in q1
   → Prüfe ob gespiegelt

5. Am Ende (ε-Übergang):
   • Wenn nur noch [Z] auf Stack
   • Wechsel zu qf (Akzeptieren!)

Beispiel "aba#aba":
a → Stack: [Z,a]
b → Stack: [Z,a,b]
a → Stack: [Z,a,b,a]
# → Wechsel zu q1
a → Stack: [Z,a,b] (match!)
b → Stack: [Z,a] (match!)
a → Stack: [Z] (match!)
ε → Akzeptiert ✓
                """
            else:  # English
                self.info_text = """
A Pushdown Automaton (PDA) consists of:

• States (q0, q1, ...)
• Input alphabet (symbols)
• Stack alphabet
• Transition function
• Start state
• Initial stack symbol

Current Automaton: Palindromes
Recognizes palindromes with # in middle:
• aba#aba ✓
• aa#aa ✓
• ab#ba ✓
• abc#cba ✓
• ab#ab ✗

━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 How it works:

1. Start in state q0 with stack [Z]

2. Phase 1 - Read first half:
   • Read symbols (a or b)
   • Push each symbol onto stack
   • Stay in q0
   → Store first half

3. Middle reached (#):
   • Read '#' from input
   • Move to q1
   → Begin comparison phase

4. Phase 2 - Check second half:
   • Read symbol from input
   • Pop same symbol from stack
   • Stay in q1
   → Check if mirrored

5. At the end (ε-transition):
   • If only [Z] remains on stack
   • Move to qf (Accept!)

Example "aba#aba":
a → Stack: [Z,a]
b → Stack: [Z,a,b]
a → Stack: [Z,a,b,a]
# → Move to q1
a → Stack: [Z,a,b] (match!)
b → Stack: [Z,a] (match!)
a → Stack: [Z] (match!)
ε → Accepted ✓
                """
        
        self.initial_stack_symbol = "Z"
        
    def create_widgets(self):
        # Titel
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        # Titel mit Sprach-Button
        title_container = tk.Frame(title_frame, bg='#2c3e50')
        title_container.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            title_container, 
            text="🔄 Pushdown Automaton - Learning Tool",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Language toggle button
        self.lang_btn = tk.Button(
            title_container,
            text="🌐 Deutsch",
            command=self.toggle_language,
            bg='#34495e',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2',
            relief=tk.RAISED
        )
        self.lang_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Hauptcontainer
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Linke Seite - Steuerung und Eingabe
        left_frame = tk.Frame(main_container, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Eingabe-Frame
        input_frame = tk.LabelFrame(left_frame, text="📝 Input", font=('Arial', 12, 'bold'), 
                                     bg='white', padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_label = tk.Label(input_frame, text="Input string:", bg='white', font=('Arial', 10))
        self.input_label.pack(anchor=tk.W)
        
        self.input_entry = tk.Entry(input_frame, font=('Courier', 14), width=30)
        self.input_entry.pack(fill=tk.X, pady=5)
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg='white')
        button_frame.pack(fill=tk.X, pady=5)
        
        self.start_btn = tk.Button(button_frame, text="▶ Start", command=self.start_automaton,
                                    bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                                    padx=10, pady=5, cursor='hand2')
        self.start_btn.pack(side=tk.LEFT, padx=2)
        
        self.step_btn = tk.Button(button_frame, text="⏩ Step", command=self.step_automaton,
                                   bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                   padx=10, pady=5, cursor='hand2')
        self.step_btn.pack(side=tk.LEFT, padx=2)
        
        self.reset_btn = tk.Button(button_frame, text="🔄 Reset", command=self.reset_automaton,
                                    bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'),
                                    padx=10, pady=5, cursor='hand2')
        self.reset_btn.pack(side=tk.LEFT, padx=2)
        
        self.example_btn = tk.Button(button_frame, text="💡 Example", command=self.setup_example,
                                      bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                                      padx=10, pady=5, cursor='hand2')
        self.example_btn.pack(side=tk.LEFT, padx=2)
        
        # Automaten-Auswahl
        mode_frame = tk.Frame(input_frame, bg='white')
        mode_frame.pack(fill=tk.X, pady=5)
        
        self.mode_label = tk.Label(mode_frame, text="Automaton Type:", bg='white', font=('Arial', 10, 'bold'))
        self.mode_label.pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="anbn")
        
        mode_anbn = tk.Radiobutton(mode_frame, text="a^n b^n", variable=self.mode_var, 
                                    value="anbn", command=self.change_automaton,
                                    bg='white', font=('Arial', 9))
        mode_anbn.pack(side=tk.LEFT, padx=5)
        
        mode_klammern = tk.Radiobutton(mode_frame, text="Parentheses", variable=self.mode_var,
                                        value="klammern", command=self.change_automaton,
                                        bg='white', font=('Arial', 9))
        mode_klammern.pack(side=tk.LEFT, padx=5)
        
        mode_palindrom = tk.Radiobutton(mode_frame, text="Palindrome", variable=self.mode_var,
                                         value="palindrom", command=self.change_automaton,
                                         bg='white', font=('Arial', 9))
        mode_palindrom.pack(side=tk.LEFT, padx=5)
        
        # Geschwindigkeit
        speed_frame = tk.Frame(input_frame, bg='white')
        speed_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(speed_frame, text="Animation Speed:", bg='white', font=('Arial', 9)).pack(side=tk.LEFT)
        self.speed_scale = tk.Scale(speed_frame, from_=100, to=2000, orient=tk.HORIZONTAL,
                                     command=self.update_speed, bg='white', length=150)
        self.speed_scale.set(500)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Visualisierung-Frame
        self.vis_frame = tk.LabelFrame(left_frame, text="🎨 Visualization", font=('Arial', 12, 'bold'),
                                  bg='white', padx=10, pady=10)
        self.vis_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas für Visualisierung
        self.canvas = tk.Canvas(self.vis_frame, bg='white', height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status-Frame
        self.status_frame_label = tk.LabelFrame(left_frame, text="📊 Status", font=('Arial', 12, 'bold'),
                                     bg='white', padx=10, pady=10)
        self.status_frame_label.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(self.status_frame_label, text="Ready", bg='white',
                                      font=('Arial', 11, 'bold'), fg='#2c3e50')
        self.status_label.pack()
        
        # Rechte Seite - Information und Stack
        right_frame = tk.Frame(main_container, bg='#f0f0f0', width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # Stack-Visualisierung
        self.stack_frame_label = tk.LabelFrame(right_frame, text="📚 Stack", font=('Arial', 12, 'bold'),
                                    bg='white', padx=10, pady=10)
        self.stack_frame_label.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.stack_canvas = tk.Canvas(self.stack_frame_label, bg='#ecf0f1', width=350, height=250)
        self.stack_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Verlauf
        self.history_frame_label = tk.LabelFrame(right_frame, text="📜 Step History", font=('Arial', 12, 'bold'),
                                      bg='white', padx=10, pady=10)
        self.history_frame_label.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.history_text = scrolledtext.ScrolledText(self.history_frame_label, height=10, width=40,
                                                       font=('Courier', 9), bg='#fdfefe')
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # Erklärung
        self.info_frame_label = tk.LabelFrame(right_frame, text="ℹ️ Information", font=('Arial', 12, 'bold'),
                                   bg='white', padx=10, pady=10)
        self.info_frame_label.pack(fill=tk.BOTH, expand=True)
        
        self.info_label = tk.Label(self.info_frame_label, text="", bg='white',
                             font=('Arial', 9), justify=tk.LEFT)
        self.info_label.pack(anchor=tk.W)
        
    def toggle_language(self):
        """Wechselt zwischen Englisch und Deutsch"""
        if self.language == "en":
            self.language = "de"
            self.lang_btn.config(text="🌐 English")
            self.update_ui_language_de()
        else:
            self.language = "en"
            self.lang_btn.config(text="🌐 Deutsch")
            self.update_ui_language_en()
        
        # Lade Automaten neu mit neuer Sprache
        self.load_automaton(self.automaton_mode)
        self.info_label.config(text=self.info_text)
        self.reset_automaton()
        
    def update_ui_language_en(self):
        """Aktualisiert UI-Texte auf Englisch"""
        self.root.title("Pushdown Automaton (PDA) - Interactive Visualization")
        self.input_label.config(text="Input string:")
        self.step_btn.config(text="⏩ Step")
        self.example_btn.config(text="💡 Example")
        self.mode_label.config(text="Automaton Type:")
        self.vis_frame.config(text="🎨 Visualization")
        self.status_frame_label.config(text="📊 Status")
        self.status_label.config(text="Ready")
        self.stack_frame_label.config(text="📚 Stack")
        self.history_frame_label.config(text="📜 Step History")
        self.info_frame_label.config(text="ℹ️ Information")
        
    def update_ui_language_de(self):
        """Aktualisiert UI-Texte auf Deutsch"""
        self.root.title("Kellerautomat (PDA) - Interaktive Visualisierung")
        self.input_label.config(text="Eingabestring:")
        self.step_btn.config(text="⏩ Schritt")
        self.example_btn.config(text="💡 Beispiel")
        self.mode_label.config(text="Automat-Typ:")
        self.vis_frame.config(text="🎨 Visualisierung")
        self.status_frame_label.config(text="📊 Status")
        self.status_label.config(text="Bereit")
        self.stack_frame_label.config(text="📚 Stack (Keller)")
        self.history_frame_label.config(text="📜 Schritt-Verlauf")
        self.info_frame_label.config(text="ℹ️ Information")
        
    def change_automaton(self):
        """Wechselt den Automaten-Typ"""
        mode = self.mode_var.get()
        self.load_automaton(mode)
        self.info_label.config(text=self.info_text)
        self.reset_automaton()
        self.setup_example()
        
    def setup_example(self):
        """Lädt ein Beispiel"""
        if self.automaton_mode == "anbn":
            examples = ["aabb", "aaabbb", "ab", "aaaabbbb"]
        elif self.automaton_mode == "klammern":
            examples = ["(())", "((()))", "()()", "(()(()))"]
        elif self.automaton_mode == "palindrom":
            examples = ["aba#aba", "aa#aa", "ab#ba", "abc#cba"]
        else:
            examples = ["aabb"]
            
        import random
        example = random.choice(examples)
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, example)
        self.reset_automaton()
        
    def update_speed(self, value):
        """Aktualisiert die Animationsgeschwindigkeit"""
        self.animation_speed = int(value)
        
    def reset_automaton(self):
        """Setzt den Automaten zurück"""
        self.stack = [self.initial_stack_symbol]
        self.current_state = "q0"
        self.input_position = 0
        self.step_history = []
        self.is_running = False
        
        self.history_text.delete(1.0, tk.END)
        if self.language == "de":
            self.history_text.insert(tk.END, "Automat zurückgesetzt.\n")
            self.history_text.insert(tk.END, f"Startzustand: {self.current_state}\n")
            self.history_text.insert(tk.END, f"Stack initialisiert: {self.stack}\n\n")
            self.status_label.config(text="Bereit", fg='#2c3e50')
        else:
            self.history_text.insert(tk.END, "Automaton reset.\n")
            self.history_text.insert(tk.END, f"Start state: {self.current_state}\n")
            self.history_text.insert(tk.END, f"Stack initialized: {self.stack}\n\n")
            self.status_label.config(text="Ready", fg='#2c3e50')
        
        self.update_visualization()
        
    def start_automaton(self):
        """Startet die automatische Ausführung"""
        if self.is_running:
            return
            
        self.input_string = self.input_entry.get()
        if not self.input_string and self.input_position == 0:
            if self.language == "de":
                messagebox.showwarning("Warnung", "Bitte geben Sie einen String ein!")
            else:
                messagebox.showwarning("Warning", "Please enter a string!")
            return
            
        self.reset_automaton()
        self.is_running = True
        self.run_automatic()
        
    def run_automatic(self):
        """Führt Schritte automatisch aus"""
        if not self.is_running:
            return
            
        if self.input_position <= len(self.input_string):
            result = self.step_automaton()
            if result:
                self.root.after(self.animation_speed, self.run_automatic)
            else:
                self.is_running = False
        else:
            self.is_running = False
            
    def step_automaton(self):
        """Führt einen Schritt aus"""
        self.input_string = self.input_entry.get()
        
        # Prüfe ob fertig
        if self.input_position > len(self.input_string):
            if self.language == "de":
                self.status_label.config(text="Fertig", fg='#95a5a6')
            else:
                self.status_label.config(text="Finished", fg='#95a5a6')
            return False
            
        # Aktuelles Symbol (oder epsilon)
        if self.input_position < len(self.input_string):
            symbol = self.input_string[self.input_position]
        else:
            symbol = ""  # Epsilon-Übergang
            
        # Stack-Top
        if len(self.stack) > 0:
            stack_top = self.stack[-1]
        else:
            if self.language == "de":
                self.status_label.config(text="❌ Fehler: Stack leer!", fg='#e74c3c')
                self.history_text.insert(tk.END, "FEHLER: Stack ist leer!\n")
            else:
                self.status_label.config(text="❌ Error: Stack empty!", fg='#e74c3c')
                self.history_text.insert(tk.END, "ERROR: Stack is empty!\n")
            return False
            
        # Suche passende Transition
        transition_key = (self.current_state, symbol, stack_top)
        
        if transition_key in self.transitions:
            new_state, stack_action = self.transitions[transition_key]
            
            # Log
            if self.language == "de":
                log_msg = f"Schritt {len(self.step_history) + 1}:\n"
                log_msg += f"  Zustand: {self.current_state} → {new_state}\n"
                log_msg += f"  Symbol: '{symbol if symbol else 'ε'}'\n"
                log_msg += f"  Stack vorher: {self.stack}\n"
            else:
                log_msg = f"Step {len(self.step_history) + 1}:\n"
                log_msg += f"  State: {self.current_state} → {new_state}\n"
                log_msg += f"  Symbol: '{symbol if symbol else 'ε'}'\n"
                log_msg += f"  Stack before: {self.stack}\n"
            
            # Stack aktualisieren
            self.stack.pop()  # Entferne Top
            if stack_action:
                self.stack.extend(reversed(stack_action))  # Füge neue Symbole hinzu
            
            if self.language == "de":
                log_msg += f"  Stack nachher: {self.stack}\n\n"
            else:
                log_msg += f"  Stack after: {self.stack}\n\n"
            
            self.history_text.insert(tk.END, log_msg)
            self.history_text.see(tk.END)
            
            # Update
            self.current_state = new_state
            if symbol:  # Nur weitergehen wenn nicht epsilon
                self.input_position += 1
            elif self.current_state in self.accepting_states:
                # Bei epsilon-Übergang in Endzustand
                self.input_position = len(self.input_string) + 1
                
            self.step_history.append((transition_key, new_state, list(self.stack)))
            
            # Prüfe Akzeptanz
            if self.current_state in self.accepting_states and self.input_position >= len(self.input_string):
                if len(self.stack) == 1 and self.stack[0] == self.initial_stack_symbol:
                    if self.language == "de":
                        self.status_label.config(text="✅ AKZEPTIERT!", fg='#27ae60')
                        messagebox.showinfo("Erfolg", "Der String wurde akzeptiert!")
                    else:
                        self.status_label.config(text="✅ ACCEPTED!", fg='#27ae60')
                        messagebox.showinfo("Success", "The string was accepted!")
                    self.update_visualization()
                    return False
                    
            self.update_visualization()
            return True
            
        else:
            # Keine Transition gefunden
            if self.current_state in self.accepting_states and self.input_position == len(self.input_string):
                if self.language == "de":
                    self.status_label.config(text="✅ AKZEPTIERT!", fg='#27ae60')
                else:
                    self.status_label.config(text="✅ ACCEPTED!", fg='#27ae60')
            else:
                if self.language == "de":
                    self.status_label.config(text="❌ ABGELEHNT", fg='#e74c3c')
                    messagebox.showerror("Fehler", f"Keine Transition für:\nZustand: {self.current_state}\nSymbol: '{symbol if symbol else 'ε'}'\nStack-Top: {stack_top}")
                else:
                    self.status_label.config(text="❌ REJECTED", fg='#e74c3c')
                    messagebox.showerror("Error", f"No transition for:\nState: {self.current_state}\nSymbol: '{symbol if symbol else 'ε'}'\nStack-Top: {stack_top}")
            
            self.update_visualization()
            return False
            
    def update_visualization(self):
        """Aktualisiert die Visualisierung"""
        # Canvas leeren
        self.canvas.delete("all")
        
        # Eingabestring visualisieren
        canvas_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 600
        canvas_height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 300
        
        # Titel
        if self.language == "de":
            title_text = "Eingabestring mit Leseposition"
            state_text = f"Aktueller Zustand: {self.current_state}"
        else:
            title_text = "Input String with Read Position"
            state_text = f"Current State: {self.current_state}"
        
        self.canvas.create_text(canvas_width // 2, 30, text=title_text,
                               font=('Arial', 12, 'bold'), fill='#2c3e50')
        
        # Eingabestring
        if self.input_string:
            x_start = 50
            y_pos = 80
            box_size = 40
            
            for i, char in enumerate(self.input_string):
                x = x_start + i * (box_size + 5)
                
                # Farbe basierend auf Position
                if i < self.input_position:
                    color = '#bdc3c7'  # Bereits gelesen
                elif i == self.input_position:
                    color = '#f39c12'  # Aktuell
                else:
                    color = '#ecf0f1'  # Noch nicht gelesen
                    
                self.canvas.create_rectangle(x, y_pos, x + box_size, y_pos + box_size,
                                            fill=color, outline='#34495e', width=2)
                self.canvas.create_text(x + box_size // 2, y_pos + box_size // 2,
                                       text=char, font=('Courier', 16, 'bold'))
                                       
            # Zeiger
            if self.input_position < len(self.input_string):
                x_pointer = x_start + self.input_position * (box_size + 5) + box_size // 2
                self.canvas.create_text(x_pointer, y_pos - 20, text="▼",
                                       font=('Arial', 20), fill='#e74c3c')
                                       
        # Zustand visualisieren
        state_y = 180
        self.canvas.create_text(canvas_width // 2, state_y, 
                               text=state_text,
                               font=('Arial', 16, 'bold'), 
                               fill='#e74c3c' if self.current_state in self.accepting_states else '#3498db')
        
        # Zustandskreis
        cx = canvas_width // 2
        cy = state_y + 50
        radius = 40
        
        color = '#2ecc71' if self.current_state in self.accepting_states else '#3498db'
        self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                               fill=color, outline='#2c3e50', width=3)
        self.canvas.create_text(cx, cy, text=self.current_state,
                               font=('Arial', 18, 'bold'), fill='white')
        
        # Doppelkreis für Endzustand
        if self.current_state in self.accepting_states:
            self.canvas.create_oval(cx - radius + 5, cy - radius + 5, 
                                   cx + radius - 5, cy + radius - 5,
                                   outline='#2c3e50', width=2)
                                   
        # Stack visualisieren
        self.draw_stack()
        
    def draw_stack(self):
        """Zeichnet den Stack"""
        self.stack_canvas.delete("all")
        
        if not self.stack:
            if self.language == "de":
                empty_text = "Stack ist leer"
            else:
                empty_text = "Stack is empty"
            self.stack_canvas.create_text(175, 125, text=empty_text,
                                         font=('Arial', 14, 'italic'), fill='#95a5a6')
            return
            
        canvas_width = self.stack_canvas.winfo_width() if self.stack_canvas.winfo_width() > 1 else 350
        canvas_height = self.stack_canvas.winfo_height() if self.stack_canvas.winfo_height() > 1 else 250
        
        box_height = 40
        box_width = 100
        x_center = canvas_width // 2
        
        # Von oben nach unten zeichnen (Top ist oben)
        for i, symbol in enumerate(reversed(self.stack)):
            y = 20 + i * (box_height + 5)
            
            # Hervorhebung des obersten Elements
            if i == 0:
                color = '#f39c12'
                outline_width = 3
            else:
                color = '#3498db'
                outline_width = 2
                
            # Box
            self.stack_canvas.create_rectangle(x_center - box_width // 2, y,
                                               x_center + box_width // 2, y + box_height,
                                               fill=color, outline='#2c3e50', width=outline_width)
            
            # Symbol
            self.stack_canvas.create_text(x_center, y + box_height // 2,
                                         text=str(symbol), font=('Courier', 16, 'bold'),
                                         fill='white')
            
            # Label für Top
            if i == 0:
                self.stack_canvas.create_text(x_center + box_width // 2 + 30, y + box_height // 2,
                                             text="← TOP", font=('Arial', 10, 'bold'),
                                             fill='#e74c3c')


def main():
    root = tk.Tk()
    app = KellerautomatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
