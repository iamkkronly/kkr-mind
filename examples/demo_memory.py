"""
KKR Mind — Demo 3: Multi-turn memory
Run: python examples/demo_memory.py
"""

from kkrmind import KKRMind


def main():
    ai = KKRMind(memory=True, max_history=20)

    print("=== KKR Mind — memory ===\n")

    print("You: My name is Rahul and I live in Kolkata.")
    print(f"KKR Mind: {ai.chat('My name is Rahul and I live in Kolkata.')}")

    print("\nYou: What is my name?")
    print(f"KKR Mind: {ai.chat('What is my name?')}")

    print("\nYou: What city am I in?")
    print(f"KKR Mind: {ai.chat('What city am I in?')}")

    print("\n--- Memory contents ---")
    for msg in ai.get_memory():
        print(f"  {msg['role']}: {msg['content']}")

    ai.clear_memory()
    print("\nMemory cleared.")


if __name__ == "__main__":
    main()
