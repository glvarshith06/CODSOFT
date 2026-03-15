# ============================================================
# TASK 1 - CHATBOT WITH RULE-BASED RESPONSES
# CodSoft AI Internship
# ============================================================

import re

# ── Predefined rules: (pattern, response) ──────────────────
RULES = [
    # Greetings
    (r"\b(hi|hello|hey|howdy)\b", "Hello! 👋 How can I help you today?"),
    (r"\bgood (morning|afternoon|evening)\b", "Good {1} to you too! Hope you're having a great day."),

    # Farewells
    (r"\b(bye|goodbye|see you|take care)\b", "Goodbye! Have a wonderful day! 😊"),

    # How are you
    (r"\bhow are you\b", "I'm just a bot, but I'm doing great! Thanks for asking. 😄"),
    (r"\bwhat('s| is) up\b", "Not much, just here to chat! What's on your mind?"),

    # Name
    (r"\bwhat('s| is) your name\b", "I'm RuleBot 🤖, your friendly rule-based assistant!"),
    (r"\bwho are you\b", "I'm RuleBot, a simple AI chatbot built with rule-based responses."),

    # Help
    (r"\b(help|assist|support)\b", "Sure! You can ask me about:\n  - Greetings\n  - My name\n  - The weather\n  - Jokes\n  - General questions"),

    # Weather
    (r"\bweather\b", "I can't check live weather, but I hope it's sunny wherever you are! ☀️"),

    # Jokes
    (r"\b(joke|funny|laugh)\b", "Why don't scientists trust atoms? Because they make up everything! 😂"),

    # Age
    (r"\bhow old are you\b", "I was just created, so I'm practically a newborn in bot years! 🍼"),

    # Capabilities
    (r"\bwhat can you do\b", "I can chat, answer basic questions, tell jokes, and keep you company! 😊"),

    # Thanks
    (r"\b(thanks|thank you|thx)\b", "You're welcome! 😊 Let me know if you need anything else."),

    # Affirmations
    (r"\b(yes|yeah|yep|sure|okay|ok)\b", "Got it! Is there anything else I can help you with?"),
    (r"\b(no|nope|nah)\b", "Alright! Feel free to ask me anything anytime."),

    # Creator
    (r"\bwho (made|created|built) you\b", "I was built as part of the CodSoft AI Internship — Task 1! 🎓"),

    # Time
    (r"\bwhat time is it\b", "I don't have access to a clock, but your device can tell you! ⏰"),

    # Default fallback (must be last)
    (r".*", "Hmm, I'm not sure I understand that. Could you rephrase? 🤔"),
]


def get_response(user_input: str) -> str:
    """Match user input against rules and return a response."""
    text = user_input.lower().strip()
    for pattern, response in RULES:
        match = re.search(pattern, text)
        if match:
            # Support back-references like {1} in response
            try:
                return response.format(*match.groups())
            except (IndexError, KeyError):
                return response
    return "I didn't quite catch that. Can you try again?"


def chat():
    """Main chat loop."""
    print("=" * 50)
    print("       Welcome to RuleBot 🤖")
    print("  Type 'quit' or 'exit' to end the chat.")
    print("=" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("RuleBot: Goodbye! It was nice chatting with you. 👋")
            break
        response = get_response(user_input)
        print(f"RuleBot: {response}")


if __name__ == "__main__":
    chat()
