#!/usr/bin/env python3
"""
Mail Intelligence - AI-Powered Email Classification

This script classifies emails from a Postfix Maildir using an LLM.
It automatically routes emails to specific folders based on their classification.
Project by Santosh Parsa for LinkedIn.

4-Step Mental Formula for AI Email Processing:
1. Ingest: Read raw email files from Postfix Maildir.
2. Parse: Extract essential metadata (From, To, Subject) and text body.
3. Classify: Send prompt with email data to an LLM (OpenAI or Ollama).
4. Act: Route the email to the appropriate folder (Inbox, Junk, Marketing).
"""

import os
import sys
import json
import time
import email
import mailbox
import argparse
import shutil
from dataclasses import dataclass, asdict
from email.policy import default
from openai import OpenAI

@dataclass
class EmailRecord:
    id: str
    sender: str
    recipient: str
    subject: str
    date: str
    body_snippet: str
    classification: str = ""
    reason: str = ""
    original_path: str = ""

def generate_sample_maildir(maildir_path: str):
    """Generates a sample Maildir with 10 realistic emails for testing."""
    print(f"Creating sample maildir at {maildir_path}...")
    
    # Create standard Maildir structure
    for subdir in ['new', 'cur', 'tmp']:
        os.makedirs(os.path.join(maildir_path, subdir), exist_ok=True)
        
    emails = [
        # Spam
        ("Win a free iPhone!", "winner@scam.com", "You have been selected to win a free iPhone 15! Click here now to claim your prize before it expires."),
        ("Enlarge your bank account", "rich@wealthy.com", "Invest just $10 and make $10,000 in 24 hours. Guaranteed returns!"),
        ("Your account has been suspended", "security@fake-bank.com", "Please login immediately to verify your identity or your account will be deleted."),
        # Marketing
        ("50% off all shoes this weekend", "sales@shoes.com", "Don't miss our biggest sale of the year. 50% off all sneakers, boots, and sandals."),
        ("Your weekly newsletter", "newsletter@techcrunch.com", "Here are the top tech stories of the week: AI is taking over, new startups, and more."),
        ("Join our upcoming webinar", "events@software.com", "Learn how to optimize your workflow in our free 1-hour webinar next Tuesday."),
        # Legitimate (Work/Vendor)
        ("Project update meeting", "boss@company.com", "Hi team, let's meet at 2 PM to discuss the Q3 roadmap. Please review the attached slides."),
        ("Invoice #12345 attached", "billing@vendor.com", "Please find attached the invoice for last month's cloud hosting services. Due in 30 days."),
        ("Code review request", "colleague@company.com", "I just opened a PR for the new caching layer. Could you take a look when you have a moment?"),
        # System Alert
        ("Server disk space critical", "alerts@monitoring.com", "Warning: Production database server disk space is at 95%. Immediate action required.")
    ]
    
    for i, (subject, sender, body) in enumerate(emails):
        msg = email.message.EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = "santosh@example.com"
        msg['Date'] = email.utils.formatdate(localtime=True)
        msg.set_content(body)
        
        filepath = os.path.join(maildir_path, 'new', f'msg_{i}.eml')
        with open(filepath, 'w') as f:
            f.write(msg.as_string())

def extract_body(msg) -> str:
    """Extracts the plain text body from an email message."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body += part.get_payload(decode=True).decode()
                except Exception:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode()
        except Exception:
            body = str(msg.get_payload())
    
    return body[:1500].strip()

def setup_llm_client(model_override: str):
    """Sets up the OpenAI client, defaulting to Ollama if no API key is found."""
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if api_key:
        print("Using OpenAI for classification.")
        client = OpenAI(api_key=api_key)
        model = model_override or "gpt-4o-mini"
        is_openai = True
    else:
        print("OPENAI_API_KEY not found. Using local Ollama for classification.")
        # Point OpenAI client to local Ollama instance
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        model = model_override or "llama3.2:1b"
        is_openai = False
        
    return client, model, is_openai

def classify_email(client, model: str, email_record: EmailRecord) -> tuple[str, str]:
    """Uses LLM to classify an email into spam, marketing, or legitimate."""
    
    prompt = f"""
You are an intelligent email classification assistant.
Analyze the following email and classify it into EXACTLY ONE of these three categories:
1. spam
2. marketing
3. legitimate

Email Details:
From: {email_record.sender}
Subject: {email_record.subject}
Body: {email_record.body_snippet}

Respond in the following JSON format ONLY:
{{
  "category": "<spam|marketing|legitimate>",
  "reason": "<short 1-sentence reason>"
}}
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful email assistant that outputs valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        
        category = result_json.get("category", "legitimate").lower()
        if category not in ["spam", "marketing", "legitimate"]:
            category = "legitimate"
            
        reason = result_json.get("reason", "No reason provided.")
        return category, reason
        
    except Exception as e:
        print(f"Error classifying email {email_record.id}: {e}")
        return "legitimate", "Error during classification, defaulted to legitimate."

def route_email(email_record: EmailRecord, base_maildir: str, dry_run: bool):
    """Routes the email to the appropriate folder based on its classification."""
    if dry_run:
        return
        
    # Define target directory mapping
    folder_mapping = {
        "spam": "Junk",
        "marketing": "Marketing",
        "legitimate": "Inbox"
    }
    
    target_folder = folder_mapping.get(email_record.classification, "Inbox")
    
    # Create target directory if it doesn't exist (using Maildir structure)
    target_dir = os.path.join(os.path.dirname(os.path.abspath(base_maildir)), target_folder, 'new')
    os.makedirs(target_dir, exist_ok=True)
    
    # Move the file
    filename = os.path.basename(email_record.original_path)
    new_path = os.path.join(target_dir, filename)
    
    try:
        shutil.move(email_record.original_path, new_path)
    except Exception as e:
        print(f"Failed to move file {email_record.original_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Email Classification")
    parser.add_argument("--maildir", default="./sample_maildir", help="Path to the Postfix Maildir")
    parser.add_argument("--dry-run", action="store_true", help="Classify but don't move files")
    parser.add_argument("--model", help="Override the LLM model name")
    args = parser.parse_args()

    # Generate sample data if directory doesn't exist
    if not os.path.exists(args.maildir):
        generate_sample_maildir(args.maildir)

    print(f"\\n--- Starting Mail Intelligence ---")
    print(f"Maildir: {args.maildir}")
    print(f"Dry Run: {args.dry_run}")
    
    client, model, is_openai = setup_llm_client(args.model)
    print(f"Model: {model}\\n")

    start_time = time.time()
    
    # We will read directly from the 'new' subdirectory for simplicity
    new_emails_dir = os.path.join(args.maildir, 'new')
    if not os.path.exists(new_emails_dir):
        print(f"No 'new' subdirectory found in {args.maildir}.")
        sys.exit(1)

    email_files = [f for f in os.listdir(new_emails_dir) if os.path.isfile(os.path.join(new_emails_dir, f))]
    total_emails = len(email_files)
    
    if total_emails == 0:
        print("No emails found to process.")
        sys.exit(0)

    results = []
    counts = {"spam": 0, "marketing": 0, "legitimate": 0}
    
    for i, filename in enumerate(email_files):
        filepath = os.path.join(new_emails_dir, filename)
        
        try:
            with open(filepath, 'rb') as f:
                msg = email.message_from_binary_file(f, policy=default)
        except Exception as e:
            print(f"Could not read {filename}: {e}")
            continue
            
        record = EmailRecord(
            id=filename,
            sender=str(msg.get("From", "Unknown")),
            recipient=str(msg.get("To", "Unknown")),
            subject=str(msg.get("Subject", "No Subject")),
            date=str(msg.get("Date", "")),
            body_snippet=extract_body(msg),
            original_path=filepath
        )
        
        print(f"Processing ({i+1}/{total_emails}): {record.subject}")
        
        # Classify using LLM
        category, reason = classify_email(client, model, record)
        record.classification = category
        record.reason = reason
        
        counts[category] += 1
        results.append(record)
        
        # Route the file
        route_email(record, args.maildir, args.dry_run)
        print(f"  -> {category.upper()} | {reason}")
        
    end_time = time.time()
    duration = end_time - start_time
    
    # Calculate estimated cost (very rough estimate for gpt-4o-mini)
    # Assumes ~300 tokens per email at $0.150 / 1M input + $0.600 / 1M output
    estimated_cost = 0.0
    if is_openai:
        estimated_cost = total_emails * (300 / 1_000_000) * 0.30  # Blended avg

    # Save results
    with open("classification_results.json", "w") as f:
        json.dump([asdict(r) for r in results], f, indent=2)

    # Print Beautiful Summary
    print("\\n" + "="*50)
    print(" 📊 MAIL INTELLIGENCE SUMMARY REPORT")
    print("="*50)
    print(f"Total Emails Processed : {total_emails}")
    print(f"Processing Time        : {duration:.2f} seconds")
    print(f"Avg Time Per Email     : {duration/total_emails:.2f} seconds")
    
    if is_openai:
        print(f"Estimated API Cost     : ${estimated_cost:.6f}")
        
    print("\\n--- Classification Breakdown ---")
    for category in ["legitimate", "marketing", "spam"]:
        count = counts[category]
        pct = (count / total_emails) * 100 if total_emails > 0 else 0
        print(f"• {category.capitalize().ljust(12)} : {count} ({pct:.1f}%)")
        
    print("\\nResults saved to 'classification_results.json'.")
    print("="*50 + "\\n")

if __name__ == '__main__':
    main()
