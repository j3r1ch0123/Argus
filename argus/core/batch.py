
import time
import argparse
from pathlib import Path
from argus.modules import breached_credentials_lookup

"""
batch.py — Batch email breached credential lookup

Reads a list of emails from a file and runs the breached_credentials_lookup
module for each, respecting API limits. Outputs results to Argus' normal
results/ folder.
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

    def run(self, interval=15):
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
            time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("email_list")
    parser.add_argument("--interval", type=int, default=15)
    
    args = parser.parse_args()
    
    email_batch = EmailBatchRunner(args.email_list)
    email_batch.run(args.interval)
