"""
KKR Mind — Demo 6: Health check
Run: python examples/demo_ping.py
"""

from kkrmind import KKRMind


def main():
    ai = KKRMind()

    print("=== KKR Mind — health check ===\n")

    report = ai.ping()

    print(f"Status:   {report['status']}")
    print(f"Latency:  {report.get('latency_ms')} ms")
    print(f"Developer: {report.get('developer')}")
    if report.get("sample"):
        print(f"Sample:   {report['sample']}")


if __name__ == "__main__":
    main()
