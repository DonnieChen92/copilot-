from formal_manager import FormalManager
import sys

def main():
    print("Initializing SACA v0.1 System Restart...")
    print("Loading Personal Statement Identity Protocol...")

    try:
        manager = FormalManager()
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to initialize Formal Manager: {e}")
        sys.exit(1)

    print("System Initialized Successfully.")
    print("Mode: Deep Planning & Formal Execution")
    print("="*60)

    # Simulate the specific scenario mentioned by the user:
    # "manager today, Formal attitude is my part of missing... not just simple quick answer"

    issue = "Request for review of team performance and data access rights."
    author = "Architect_Chen"

    print(f"\n[INPUT] Simulating Issue Submission by {author}: '{issue}'")
    print("="*60)

    response = manager.review_issue(issue, author)

    print("\n[OUTPUT] Formal Manager Response:")
    print(response)
    print("="*60)

if __name__ == "__main__":
    main()
