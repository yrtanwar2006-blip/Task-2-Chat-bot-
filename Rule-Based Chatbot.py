Rule-Based Chatbot
"""
Rule-Based Chatbot
==================
A simple chatbot that answers using predefined rules and keywords.
HOW THE CHATBOT DECIDES ITS REPLY (big picture)----------------------------------------------
1. The user's message is cleaned (lower-case, punctuation removed) and split
   into a set of words.
2. The message is checked against a list of RULES, from top to bottom.
3. The FIRST rule that matches wins, and its reply is returned.
   (So the order of the rules matters!)
4. If no rule matches, a FALLBACK reply is returned.
Two matching techniques are used:
  * Keyword matching  -> "is any of these words in the message?"
  * Pattern matching  -> regular expressions (re) for phrases such as
                         "my name is ..." or "what is your name".
Run:  python chatbot.py
"""
import random
import re
from datetime import datetime
BOT_NAME = "Rulo"
# The bot can remember the user's name once it is told (see the name rule).
memory = {"user_name": None}
# -------------------------------------------------------------------------
# STEP 1: Clean the input
# -------------------------------------------------------------------------
def clean_text(text):
    """Make the message easy to match: lower-case and trim spaces.
    'Hello!!  ' -> 'hello!!'"""
    return text.lower().strip()
def get_words(text):
    """Return the set of words in the message, ignoring punctuation.
    'Hi, how are you?' -> {'hi', 'how', 'are', 'you'}"""
    return set(re.findall(r"[a-z']+", text))
def has_any(words, keywords):
    """True if the message contains at least one of the keywords.
    This is the basic keyword-matching tool used by most rules."""
    return not words.isdisjoint(keywords)
# -------------------------------------------------------------------------
# STEP 2: Predefined replies (several choices make the bot feel less robotic)
# -------------------------------------------------------------------------
GREETING_REPLIES = [
    "Hello! How can I help you today?",
    "Hi there! Nice to see you.",
    "Hey! What would you like to talk about?",
]
HOW_ARE_YOU_REPLIES = [
]
    "I'm doing great, thanks for asking! How about you?",
    "I'm just a program, but I'm running perfectly. How are you?",
THANKS_REPLIES = [
    "You're welcome!",
    "Happy to help!",
    "Anytime!",
]
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the developer go broke? He used up all his cache!",
    "There are 10 kinds of people: those who understand binary and those who don't.",
]
# Used when NO rule matches (the fallback).
FALLBACK_REPLIES = [
    "Sorry, I didn't understand that. Type 'help' to see what I can do.",
    "Hmm, I don't know how to answer that yet. Try asking in a different way.",
    "I'm a simple bot and I couldn't understand that. Type 'help' for ideas.",
]
HELP_TEXT = (
    "I can help with these things:\n"
    "  - Say hello / good morning\n"
    "  - Ask 'how are you?'\n"
    "  - Tell me your name ('my name is ...') and ask 'what is my name?'\n"
    "  - Ask 'what is your name?' or 'who made you?'\n"
    "  - Ask for the time or today's date\n"
    "  - Ask for a joke\n"
    "  - Say 'bye' to exit"
)
# -------------------------------------------------------------------------
# STEP 3: The decision logic (if-else rules, checked from top to bottom)
# -------------------------------------------------------------------------
def get_response(user_input):
    """Decide the bot's reply. Returns (reply_text, should_exit)."""
    text = clean_text(user_input)
    words = get_words(text)
    # Rule 0: Empty input -> ask the user to type something.
    if text == "":
        return "Please type something and I'll try to answer.", False
    # Rule 1: Name introduction (PATTERN MATCHING).
    # The regex captures the word after "my name is" or "call me".
    # This rule is placed first so that "Hi, my name is Rahul" saves the
    # name instead of only being treated as a greeting.
    match = re.search(r"\b(?:my name is|call me)\s+([a-z]+)", text)
    if match:
        memory["user_name"] = match.group(1).capitalize()
        return f"Nice to meet you, {memory['user_name']}!", False
    # Rule 2: Ask the bot to recall the user's name (PATTERN MATCHING).
    if re.search(r"\bwhat(?:'s| is)? my name\b", text):
        if memory["user_name"]:
            return f"Your name is {memory['user_name']}.", False
        return "I don't know your name yet. Tell me: 'my name is ...'", False
    # Rule 3: Goodbye (KEYWORD MATCHING) -> the only rule that exits the loop.
    if has_any(words, {"bye", "goodbye", "exit", "quit", "goodnight"}) \
            or "see you" in text:
        return "Goodbye! Have a great day!", True
    # Rule 4: Greetings (KEYWORD + PATTERN).
    # We compare whole WORDS, so 'this' does not wrongly match 'hi'.
    if has_any(words, {"hi", "hello", "hey", "hii", "hola", "namaste"}) \
            or re.search(r"\bgood (morning|afternoon|evening)\b", text):
        # Use the user's name in the greeting if we know it.
        if memory["user_name"]:
            return f"Hello {memory['user_name']}! How can I help you?", False
        return random.choice(GREETING_REPLIES), False
    # Rule 5: "How are you?" question (PATTERN MATCHING).
    if re.search(r"\bhow (are you|r u|do you do)\b|\bhow's it going\b", text):
        return random.choice(HOW_ARE_YOU_REPLIES), False
    # Rule 6: User says how they feel (KEYWORD MATCHING).
    if has_any(words, {"fine", "good", "great", "okay", "ok", "well"}) \
            and has_any(words, {"i", "i'm", "am", "feeling"}):
        return "Glad to hear that!", False
    if has_any(words, {"sad", "tired", "bored", "upset", "angry"}) \
            and has_any(words, {"i", "i'm", "am", "feeling"}):
        return "Sorry to hear that. I hope your day gets better soon!", False
    # Rule 7: Bot's name / identity questions (PATTERN MATCHING).
    if re.search(r"\b(your name|who are you)\b", text):
        return f"I'm {BOT_NAME}, a simple rule-based chatbot.", False
    # Rule 8: Who created the bot (PATTERN MATCHING).
    if re.search(r"\bwho (made|created|built|developed) you\b", text):
        return "I was built in Python as a rule-based chatbot project.", False
    # Rule 9: Ask what the bot can do (KEYWORD MATCHING).
    if "help" in words or re.search(r"\bwhat can you do\b", text):
        return HELP_TEXT, False
    # Rule 10: Current time (KEYWORD MATCHING).
    # Both a topic word ('time') and a question word must be present.
    if "time" in words and has_any(words, {"what", "current", "tell", "now"}):
        return "The time is " + datetime.now().strftime("%I:%M %p") + ".", False
    # Rule 11: Today's date / day.
    if "date" in words or ("today" in words and has_any(words, {"day", "date"})):
        return "Today is " + datetime.now().strftime("%A, %d %B %Y") + ".", False
    # Rule 12: Jokes.
    if has_any(words, {"joke", "funny", "laugh"}):
        return random.choice(JOKES), False
    # Rule 13: Thanks.
    if has_any(words, {"thanks", "thank", "thx"}):
        return random.choice(THANKS_REPLIES), False
    # Rule 14: Weather - the bot is honest that it cannot check it.
    if "weather" in words:
        return "I can't check the weather, but I hope it's nice outside!", False
    # FALLBACK: none of the rules matched, so give a default reply.
    return random.choice(FALLBACK_REPLIES), False
# -------------------------------------------------------------------------
# STEP 4: The chat loop
# -------------------------------------------------------------------------
def main():
    print("=" * 40)
    print(f"  {BOT_NAME} - Rule-Based Chatbot")
    print("=" * 40)
    print("Type 'help' to see what I can do, or 'bye' to exit.\n")
    while True:
        user_input = input("You : ")
        reply, should_exit = get_response(user_input)
        print(f"{BOT_NAME}: {reply}\n")
        if should_exit:
            break
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{BOT_NAME}: Goodbye!")