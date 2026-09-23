import argparse
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser(description="Explain log file using an LLM as an SRE")
parser.add_argument("--logfile", required=True, help="Path to input log file")
parser.add_argument("--output", default="/root/explanation.txt", help="Path to save explanation output")
args = parser.parse_args()

# 1. Read the input log file
log_content = Path(args.logfile).read_text()

client = OpenAI()

# 2. Ask model as an experienced SRE for summary and most likely cause
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": (
                "You are an experienced site reliability engineer. "
                "Analyze the provided log and explain it in plain English with two things:\n"
                "1. A one or two sentence summary of what happened.\n"
                "2. The most likely cause."
            ),
        },
        {
            "role": "user",
            "content": f"Log file content:\n\n{log_content}",
        },
    ],
)

explanation = response.choices[0].message.content

# 3. Print the result
print(explanation)

# 4. Save the explanation to file
output_path = Path(args.output)
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(explanation)
print(f"\nSaved explanation to: {output_path}")
