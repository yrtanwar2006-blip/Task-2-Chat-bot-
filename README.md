# Rule-Based Chatbot

A simple console chatbot (named **Rulo**) that replies using predefined rules and keywords.

## How to run (VS Code)
1. Save `chatbot.py` in a folder and open that folder in VS Code (File > Open Folder).
2. Open the terminal (Ctrl + `) and run:
   ```
   python chatbot.py
   ```
   (Python 3.8+ required, no extra packages.)
3. Type `help` to see what the bot can do, and `bye` to exit.

## Features
- Handles common **greetings** (hello, hi, good morning, namaste).
- Answers common **questions**: how are you, what is your name, who made you, the time, today's date.
- Tells **jokes** and replies to thanks and feelings (I am fine / I am tired).
- **Remembers your name** ("my name is Asha", then "what is my name?").
- **Fallback response** when it does not understand the input.
- Uses basic **if-else** rules with **keyword matching** and **pattern matching** (regular expressions).
- Comments in the code explain how each reply is chosen.

## How the chatbot decides its reply
1. The message is cleaned (lower-case, punctuation ignored) and split into words.
2. The rules are checked from top to bottom.
3. The first rule that matches gives the reply, so the order of the rules matters.
4. If no rule matches, a random fallback reply is returned.

Whole words are compared, so a word like "this" does not wrongly match "hi".

## Sample chat
```
You : hi
Rulo: Hello! How can I help you today?

You : my name is Asha
Rulo: Nice to meet you, Asha!

You : what is my name
Rulo: Your name is Asha.

You : asdfgh
Rulo: Sorry, I didn't understand that. Type 'help' to see what I can do.

You : bye
Rulo: Goodbye! Have a great day!
```

## How to add a new rule
Add a new `if` block inside `get_response()` in `chatbot.py`, before the fallback line:
```python
if has_any(words, {"python"}):
    return "Python is a great language!", False
```

## Files
- `chatbot.py` - the complete chatbot
