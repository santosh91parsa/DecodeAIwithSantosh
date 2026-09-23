import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

def main():
    # step 1: read tickets in folder /root/tickets
    file = Path("/root/tickets")
    outdir = Path("/root/traiged")
    outdir.mkdir(parents=True, exist_ok=True)
    for f in file.glob("*"):
        t = f.read_text()
        messages=[
            {"role":"system","content":"classify it and return JSON with at least these two fields: category - one of billing, technical, account, or other priority - one of low, medium, or high"},
            {"role":"user","content": t}
        ]

        response=client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0,
        )
        result = response.choices[0].message.content
        (outdir / f.name).write_text(result)
        print(f"Saved classification for {f.name} ---> {outdir/f.name}")


if __name__ == "__main__":
    main()
