import hashlib
import hmac
import json
import os
import urllib.request
from datetime import datetime, timezone


def main() -> None:
    server_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repository = os.environ["GITHUB_REPOSITORY"]
    run_id = os.environ["GITHUB_RUN_ID"]

    payload = {
        "action_run_link": f"{server_url}/{repository}/actions/runs/{run_id}",
        "email": "akshayvanaparthy@outlook.com",
        "name": "Akshay Vanaparthi",
        "repository_link": f"{server_url}/{repository}",
        "resume_link": "https://www.linkedin.com/in/akshay-v-ai",  # replace if you'd rather link a PDF
        "timestamp": datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z"),
    }

    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    signature = hmac.new(b"hello-there-from-b12", body, hashlib.sha256).hexdigest()

    req = urllib.request.Request(
        "https://b12.io/apply/submission",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Signature-256": f"sha256={signature}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        print("Response:", response_body)
        data = json.loads(response_body)
        print("RECEIPT:", data["receipt"])


if __name__ == "__main__":
    main()