"""
KKR Mind — Demo 2: Word-by-word streaming
Run: python examples/demo_stream.py
"""

from kkrmind import KKRMind


def main():
    ai = KKRMind()

    print("=== KKR Mind — streaming ===\n")

    print("You: Tell me a short story about a cat astronaut.\n")
    print("KKR Mind: ", end="", flush=True)

    for chunk in ai.chat_stream("Tell me a short story about a cat astronaut"):
        print(chunk, end="", flush=True)

    print("\n\nDone.")


if __name__ == "__main__":
    main()
