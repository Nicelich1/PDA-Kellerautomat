# 🔄 Pushdown Automaton - Interactive Visualization

An interactive GUI tool for learning and understanding Pushdown Automata (PDA).

## 📋 Features

- **3 Different Automaton Modes:**
  - a^n b^n - Equal number of a's and b's
  - Balanced Parentheses
  - Palindromes with center marker

- **Interactive Visualization:**
  - Step-by-step execution
  - Live stack display
  - Input string tracking
  - Execution history log

- **Learning Mode:**
  - Detailed explanations
  - Example strings
  - Adjustable animation speed

## 🚀 Installation & Usage

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)

### Running the Program
```bash
python Kellerautomat.py
```

## 📖 How to Use

1. **Enter an input string** or load an **Example**
2. **Choose automaton type** (a^n b^n, Parentheses, Palindrome)
3. **Start** for automatic execution or **Step** for step-by-step execution
4. Observe the stack and state transitions

## 🎨 Interface

The program displays:
- Input string with current read position
- Current automaton state
- Real-time stack contents
- Step-by-step execution history
- Detailed explanations of how the automaton works

## 📚 Learning Objectives

- Understand how pushdown automata work
- Visualize stack operations (push/pop)
- Follow state transitions
- Recognize context-free languages

## 🛠️ Creating an EXE (Optional)

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name="Kellerautomat" Kellerautomat.py
```

The EXE will be located in `dist/Kellerautomat.exe`

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Author

Created for educational purposes - November 2025
