"""
==============================================================================
Decode AI with Santosh — AI Mail Analysis (Directory & Triage)
==============================================================================
A beginner-friendly script that reads incoming emails from a directory,
sends each email to an LLM for triage & analysis (intent, urgency, sentiment, 
summary, and action), and outputs clean JSON.

🧠 THE 4-STEP MENTAL FORMULA:
1. FIND FILES   --> Path(MAILS_DIR).glob("*")
2. READ FILE    --> file.read_text()
3. ASK AI       --> client.chat.completions.create(...)
4. PARSE JSON   --> json.loads(...)

🔮 FUTURE EXPANSION NOTE:
The EXACT same 4-step logic applies to Ticket Classification (Jira/Zendesk).
See the `mock_ticket_api()` function at the bottom for how to swap file reading
with a mock API or mock ticket data!
==============================================================================
"""

import json
import os
from pathlib import Path
from openai import OpenAI

# 1. Initialize AI Client:
# - If OPENAI_API_KEY is set in environment, uses OpenAI cloud (gpt-4o-mini).
# - If NOT set, automatically defaults to 100% FREE local Ollama (llama3.2:1b)!
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI()
    MODEL_NAME = "gpt-4o-mini"
else:
    # Ollama OpenAI-compatible local endpoint ($0 cost, runs on your Mac!)
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    MODEL_NAME = "llama3.2:1b"

# 2. Directory containing incoming emails/mails
# Defaults to /root/mails/, with fallback to local ./sample_emails for easy testing
DEFAULT_DIR = Path("/root/mails")
LOCAL_TEST_DIR = Path(__file__).parent / "sample_emails"
MAILS_DIR = DEFAULT_DIR if DEFAULT_DIR.exists() else LOCAL_TEST_DIR


def analyze_mail(mail_text: str) -> dict:
    """
    Takes raw email text, sends it to the AI model, and returns a structured JSON dictionary.
    """
    prompt = f"""
    Analyze the following incoming email and classify it for our operations team.
    
    Respond ONLY in valid JSON with these exact keys:
    - "sender_intent": ("Support", "Billing", "Sales", "Bug Report", "Feedback", or "Spam")
    - "urgency": ("Low", "Normal", "High", or "Critical")
    - "sentiment": ("Positive", "Neutral", "Frustrated", or "Angry")
    - "one_sentence_summary": (A 1-sentence summary of the sender's core message)
    - "suggested_action": ("Auto-reply with FAQ", "Route to Tier 2 Engineer", "Forward to Billing", or "Ignore/Spam")
    
    Email Content:
    \"\"\"{mail_text}\"\"\"
    """

    # STEP 3: Ask the AI
    response = client.chat.completions.create(
        model=MODEL_NAME,  # gpt-4o-mini or local llama3.2:1b
        messages=[
            {
                "role": "system",
                "content": "You are an automated email triage system. Output only valid JSON.",
            },
            {"role": "user", "content": prompt},
        ],
        # Forces the model to return strictly valid JSON
        response_format={"type": "json_object"},
    )

    # STEP 4: Convert JSON string into a Python dictionary
    raw_json_str = response.choices[0].message.content
    return json.loads(raw_json_str)


def create_sample_emails_if_needed():
    """Helper: Creates dummy email files so beginners can test instantly."""
    if not LOCAL_TEST_DIR.exists():
        LOCAL_TEST_DIR.mkdir(parents=True, exist_ok=True)
        (LOCAL_TEST_DIR / "email_01_billing.txt").write_text(
            "Subject: Double charged for Pro Plan\nFrom: john@example.com\n\n"
            "Hi, I noticed two charges of $49 on my credit card statement this morning. "
            "Could you please refund the duplicate charge immediately?",
            encoding="utf-8",
        )
        (LOCAL_TEST_DIR / "email_02_tech_down.txt").write_text(
            "Subject: URGENT: Production database connection timed out\nFrom: devops@client.com\n\n"
            "Our whole team is locked out of the dashboard. API returns 504 Gateway Timeout! "
            "Please escalate this ASAP.",
            encoding="utf-8",
        )
        (LOCAL_TEST_DIR / "email_03_sales.txt").write_text(
            "Subject: Enterprise pricing for 200 seats\nFrom: sarah@enterprisecorp.com\n\n"
            "Hello, our organization is evaluating your platform for 200 developers next quarter. "
            "Can we schedule a demo call with your enterprise sales team?",
            encoding="utf-8",
        )


def main():
    print("=" * 60)
    print("📬 AI Mail Intelligence & Directory Analysis — Decode AI with Santosh")
    print("=" * 60)

    # If neither /root/mails nor sample_emails exist, create sample emails
    if not MAILS_DIR.exists():
        print(f"Directory not found: {MAILS_DIR}")
        print(f"Creating sample emails in: {LOCAL_TEST_DIR}")
        create_sample_emails_if_needed()

    # STEP 1: Find all files in the mail directory
    mail_files = [f for f in MAILS_DIR.glob("*") if f.is_file()]

    if not mail_files:
        print(f"No mail files found in: {MAILS_DIR}")
        return

    print(f"📁 Source Directory : {MAILS_DIR}")
    print(f"📊 Mails Found      : {len(mail_files)}")
    print(f"🤖 AI Engine        : {MODEL_NAME} ({'OpenAI Cloud' if os.getenv('OPENAI_API_KEY') else '100% Free Local Ollama'})\n")

    # STEP 2: Loop and process each email file
    for idx, mail_file in enumerate(mail_files, start=1):
        print(f"[{idx}/{len(mail_files)}] 📩 Analyzing: {mail_file.name}")

        try:
            # Read email text
            email_body = mail_file.read_text(encoding="utf-8")

            # Call AI
            analysis = analyze_mail(email_body)

            # Output clean, formatted JSON
            print(json.dumps(analysis, indent=2))
            print("-" * 50)

        except Exception as e:
            print(f"❌ Error processing {mail_file.name}: {e}\n")


# ==============================================================================
# 🔮 FUTURE EXPANSION: REUSING THIS LOGIC FOR A TICKET CLASSIFIER
# (Mocking API / Mocking Data)
# ==============================================================================
def mock_ticket_api():
    """
    Demonstrates how the EXACT same logic works when reading from a ticketing
    API (like Jira, Zendesk, or ServiceNow) instead of files on disk.
    """
    print("\n[Future Expansion Demo: Mock Ticket API]")
    
    # 1. Mock Data (Instead of files on disk, data comes from an API response)
    mock_tickets = [
        {"id": "TICKET-101", "text": "Cannot reset 2FA password via SMS. Error code 403."},
        {"id": "TICKET-102", "text": "Feature request: Add dark mode to mobile app."},
    ]

    # 2. Same 4-step logic applies:
    for ticket in mock_tickets:
        print(f"Processing Ticket ID: {ticket['id']}")
        # We reuse the exact same AI classification call!
        result = analyze_mail(ticket["text"])
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
