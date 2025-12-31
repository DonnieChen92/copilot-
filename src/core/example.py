import json
from src.core.hashing import SignedObject

def run_demo():
    print("=== A-Z Framework: H · Hash Demo ===")

    # 1. Create a data object
    print("\n[Step 1] Creating a new object...")
    data = {
        "user_id": "user_123",
        "action": "generate_image",
        "params": {"style": "cyberpunk", "resolution": "1024x1024"}
    }

    obj = SignedObject(data=data, version=1)
    print(f"Object created.")
    print(f"Data: {json.dumps(obj.data, indent=2)}")
    print(f"Signature (Before Signing): {obj.signature}")

    # 2. Sign the object
    print("\n[Step 2] Signing the object...")
    obj.sign()
    print(f"Signature (After Signing): {obj.signature}")

    # 3. Verify the object
    print("\n[Step 3] Verifying integrity...")
    is_valid = obj.verify()
    print(f"Verification Result: {'PASSED' if is_valid else 'FAILED'}")

    # 4. Simulate Tampering
    print("\n[Step 4] Simulating data tampering attack...")
    print("Attacker modifies 'resolution' to '4k'...")
    obj.data["params"]["resolution"] = "4k"

    # 5. Verify again
    print("\n[Step 5] Verifying integrity after tampering...")
    is_valid_tampered = obj.verify()
    print(f"Verification Result: {'PASSED' if is_valid_tampered else 'FAILED'}")

    if not is_valid_tampered:
        print("\nSUCCESS: Tampering detected correctly.")
    else:
        print("\nFAILURE: Tampering was not detected!")

if __name__ == "__main__":
    run_demo()
