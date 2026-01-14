import time
from pathlib import Path
from argus.modules import breached_credentials_lookup

"""
batch.py — Batch email breached credential lookup

Reads a list of emails from a file and runs the breached_credentials_lookup
module for each, respecting API limits. Outputs results to Argus' normal
results/ directory.
"""

class EmailBatchRunner:
    def __init__(self, email_file: str):
        self.email_file = Path(email_file)

    def load_emails(self) -> list[str]:
        if not self.email_file.exists():
            raise FileNotFoundError(self.email_file)

        emails = []
        for line in self.email_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                emails.append(line)
        return emails

    def run(self):
        emails = self.load_emails()

        for email in emails:
            print(f"[+] Checking {email} for breaches")

            breached_credentials_lookup.run(
                target=email,
                threads=1,
                opts={}
            )

            # Sleep between API calls to respect HIBP
            print("    Sleeping 15s to avoid hitting API limits...")
            time.sleep(15)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m argus.core.batch <emails.txt>")
        sys.exit(1)

    EmailBatchRunner(sys.argv[1]).run()
