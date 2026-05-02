import os
import time
import pandas as pd
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. Please add it to your environment variables."
    )

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are a GTM Engineer writing personalized outbound email opening lines for a B2B SaaS sales team. "
    "You write concise, direct, research-backed first lines that reference a specific signal about the company. "
    'No fluff, no "I noticed", no "Congrats on". Tone is professional and direct.'
)

# Groq free tier: ~30 requests/min for llama-3.3-70b-versatile
# 60s / 30 req = 2s per request to stay safely under the limit
DELAY_BETWEEN_REQUESTS = 2.0

def build_user_prompt(row):
    return (
        f"Company: {row.get('company_name', '')}\n"
        f"Location: {row.get('city', '')}, {row.get('state', '')}\n"
        f"Funding Stage: {row.get('funding_stage', '')}\n"
        f"Last Funded: {row.get('last_funding_date', '')}\n"
        f"Industries: {row.get('industries', '')}\n"
        f"Employee Range: {row.get('employee_range', '')}\n"
        f"Estimated Revenue: {row.get('estimated_revenue', '')}\n"
        f"Founder: {row.get('founder_name', '')}\n\n"
        "Write one personalized outreach opening line under 25 words that references their funding stage and industry "
        "as a reason to reach out now. Output only the line, nothing else."
    )

def generate_outreach_line(row, retries=5):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(row)},
                ],
                max_tokens=60,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            err = str(e).lower()
            if "rate limit" in err or "429" in err or "too many" in err:
                wait = 60 * (attempt + 1)
                print(f"  Rate limited — waiting {wait}s before retry {attempt + 1}/{retries}...", flush=True)
                time.sleep(wait)
            else:
                print(f"  API error on attempt {attempt + 1}: {e}", flush=True)
                time.sleep(5)
    return "[error generating line]"

def main():
    input_file = "top_tier1_companies.csv"
    output_file = "tier1_with_outreach.csv"

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"'{input_file}' not found. Please upload the CSV file to the project root."
        )

    df = pd.read_csv(input_file)
    total = len(df)

    # Resume from existing output if available
    if os.path.exists(output_file):
        existing = pd.read_csv(output_file)
        if "outreach_line" in existing.columns:
            outreach_lines = existing["outreach_line"].tolist()
            while len(outreach_lines) < total:
                outreach_lines.append(None)
            done_count = sum(1 for x in outreach_lines if pd.notna(x) and str(x).strip() != "")
            print(f"Resuming — {done_count} of {total} already done.", flush=True)
        else:
            outreach_lines = [None] * total
    else:
        outreach_lines = [None] * total

    print(f"Processing {total} companies (free tier pacing: {DELAY_BETWEEN_REQUESTS}s/request)...", flush=True)

    batch_size = 10

    for i, (_, row) in enumerate(df.iterrows()):
        val = outreach_lines[i]
        if val is not None and pd.notna(val) and str(val).strip() not in ("", "[error generating line]"):
            continue

        line = generate_outreach_line(row)
        outreach_lines[i] = line

        processed = i + 1
        if processed % batch_size == 0 or processed == total:
            print(f"Processed {processed} of {total}", flush=True)
            df["outreach_line"] = outreach_lines
            df.to_csv(output_file, index=False)

        # Pace to stay under free tier rate limit
        time.sleep(DELAY_BETWEEN_REQUESTS)

    df["outreach_line"] = outreach_lines
    df.to_csv(output_file, index=False)
    print(f"\nSaved output to {output_file}", flush=True)

    print("\n--- 5 Sample Results ---")
    sample = df[["company_name", "icp_score", "outreach_line"]].head(5)
    for _, row in sample.iterrows():
        print(f"\nCompany:   {row['company_name']}")
        print(f"ICP Score: {row['icp_score']}")
        print(f"Outreach:  {row['outreach_line']}")

if __name__ == "__main__":
    main()
