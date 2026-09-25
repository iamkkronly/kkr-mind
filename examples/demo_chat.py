"""
KKR Mind — Demo 1: Basic chat
Run: python examples/demo_chat.py
"""

from kkrmind import KKRMind


def main():
    ai = KKRMind()

    print("=== KKR Mind — basic chat ===\n")

    print("You: Hello!")
    reply = ai.chat("Hello!")
    print(f"KKR Mind: {reply}\n")

    print("You: তুমি কে? (Who are you?)")
    reply = ai.chat("তুমি কে?")
    print(f"KKR Mind: {reply}\n")

    print("You: Write a haiku about Kolkata")
    reply = ai.chat("Write a haiku about Kolkata")
    print(f"KKR Mind: {reply}")


if __name__ == "__main__":
    main()
