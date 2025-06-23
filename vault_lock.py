import getpass
import os
import sys

VAULT_PATH = "vault"
PASSWORD = "charan"  # Change this to a strong password you prefer

def unlock_vault():
    print("🔒 Welcome to ShadowSentinel Vault")
    for attempt in range(3):
        pwd = getpass.getpass("Enter vault password: ")
        if pwd == PASSWORD:
            print("✅ Access granted!")
            # List files in vault folder
            files = os.listdir(VAULT_PATH)
            if not files:
                print("Vault is empty.")
            else:
                print("Vault contents:")
                for f in files:
                    print(f" - {f}")
            return
        else:
            print("❌ Wrong password. Try again.")
    print("🚫 Too many failed attempts. Exiting.")
    sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists(VAULT_PATH):
        os.mkdir(VAULT_PATH)
    unlock_vault()
